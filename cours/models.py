from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Filière"
        verbose_name_plural = "Filières"

    def __str__(self):
        return self.nom


class Classe(models.Model):
    NIVEAU_CHOICES = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    ]

    nom = models.CharField(max_length=100)
    filieres = models.ManyToManyField(Filiere, related_name='classes')
    niveau = models.CharField(max_length=2, choices=NIVEAU_CHOICES, db_index=True)
    effectif_max = models.IntegerField(default=50)
    actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['niveau', 'nom']
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

    def __str__(self):
        filieres_str = ", ".join([f.nom for f in self.filieres.all()])
        return f"{self.nom} ({filieres_str})"


class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    specialite = models.CharField(max_length=200, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = "Professeur"
        verbose_name_plural = "Professeurs"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    volume_horaire = models.IntegerField(help_text="Volume horaire total en heures")
    professeur = models.ForeignKey(
        Professeur, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='matieres'
    )
    actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Matière"
        verbose_name_plural = "Matières"

    def __str__(self):
        return self.nom


class Cours(models.Model):
    TYPE_SALLE = [
        ('SENGHOR', 'Salle Leopold Sedar Senghor'),
        ('MANDELA', 'Salle Nelson Mandela'),
        ('KANE', 'Salle Amidou Kane'),
        ('SECK', 'Salle Assane Seck'),
        ('FAYE', 'Salle Bassirou Diomaye Faye'),
    ]

    libelle = models.CharField(max_length=200)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='cours')
    professeur = models.ForeignKey(
        Professeur, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='cours'
    )
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='cours', null=True, blank=True)
    date = models.DateField(db_index=True)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.CharField(max_length=15, choices=TYPE_SALLE, blank=True)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    
    # Champs de suivi
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['date', 'heure_debut']
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        indexes = [
            models.Index(fields=['date', 'heure_debut']),
            models.Index(fields=['classe', 'date']),
        ]

    def __str__(self):
        return f"{self.libelle} - {self.classe.nom} ({self.date} {self.heure_debut}-{self.heure_fin})"

    @property
    def duree(self):
        """Retourne la durée du cours en heures"""
        debut = datetime.combine(self.date, self.heure_debut)
        fin = datetime.combine(self.date, self.heure_fin)
        return (fin - debut).total_seconds() / 3600

    def clean(self):
        """Validations personnalisées"""
        # Valider que l'heure de début est avant l'heure de fin
        if self.heure_debut >= self.heure_fin:
            raise ValidationError("L'heure de début doit être antérieure à l'heure de fin.")

        # Valider la cohérence professeur-matière
        if self.professeur and self.matiere.professeur:
            if self.professeur != self.matiere.professeur:
                raise ValidationError(
                    f"Le professeur du cours ({self.professeur}) doit correspondre "
                    f"à celui de la matière ({self.matiere.professeur})."
                )

        # Empêcher les conflits de planning pour la même classe
        conflits_classe = Cours.objects.filter(
            classe=self.classe,
            date=self.date,
            actif=True
        ).exclude(pk=self.pk).filter(
            heure_debut__lt=self.heure_fin,
            heure_fin__gt=self.heure_debut
        )
        
        if conflits_classe.exists():
            raise ValidationError("Ce créneau horaire est déjà occupé pour cette classe.")

        # Empêcher les conflits de planning pour le même professeur
        if self.professeur:
            conflits_prof = Cours.objects.filter(
                professeur=self.professeur,
                date=self.date,
                actif=True
            ).exclude(pk=self.pk).filter(
                heure_debut__lt=self.heure_fin,
                heure_fin__gt=self.heure_debut
            )
            
            if conflits_prof.exists():
                raise ValidationError(
                    f"Le professeur {self.professeur} a déjà un cours à ce créneau."
                )

        # Empêcher les conflits de salle (si spécifiée)
        if self.salle:
            conflits_salle = Cours.objects.filter(
                salle=self.salle,
                date=self.date,
                actif=True
            ).exclude(pk=self.pk).filter(
                heure_debut__lt=self.heure_fin,
                heure_fin__gt=self.heure_debut
            )
            
            if conflits_salle.exists():
                raise ValidationError(f"La salle {self.salle} est déjà occupée à ce créneau.")

    def save(self, *args, **kwargs):
        """Override save pour valider avant sauvegarde"""
        self.full_clean()
        super().save(*args, **kwargs)
        