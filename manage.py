 #!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Telegram.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# /media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/Automation/telegram_avds/office-work/env/bin/python3.8 /media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/Automation/telegram_avds/office-work/manage.py