#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config


def main():
    """Run administrative tasks."""
    if config('MODULE_ENVIRONMENT',default='development'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eccomerce_api.settings.development')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eccomerce_api.settings.production')
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
