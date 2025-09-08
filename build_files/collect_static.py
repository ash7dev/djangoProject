import os
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')

if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
