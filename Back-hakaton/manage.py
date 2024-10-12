#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Detecting_defects_laptops.settings')

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    reports_dir = os.path.join(base_dir, 'reports')
    # media_dir = os.path.join(base_dir, 'media')
    
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        print(f"Created directory: {reports_dir}")

    # if not os.path.exists(media_dir):
    #     os.makedirs(media_dir)
    #     print(f"Created directory: {media_dir}")

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
