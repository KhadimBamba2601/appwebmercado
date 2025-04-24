#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Inicializar la base de datos si es necesario
    if len(sys.argv) > 1 and sys.argv[1] not in ['help', '--help', '-h']:
        try:
            from init_db import create_database
            if not create_database():
                print("Error: No se pudo inicializar la base de datos.")
                sys.exit(1)
        except ImportError as e:
            print(f"Error al importar init_db: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error inesperado al inicializar la base de datos: {e}")
            sys.exit(1)

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
