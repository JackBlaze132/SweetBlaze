import os
import sys
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sweetblaze_backend.settings')
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:8001']
    execute_from_command_line(sys.argv)