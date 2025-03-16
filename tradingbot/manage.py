#!/usr/bin/env python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def check_virtual_env():
    """Checks if the script is running inside a virtual environment."""
    if sys.prefix == sys.base_prefix:
        logging.warning("Warning: No virtual environment detected. Consider activating one.")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "littlelemon.settings")

    if "DJANGO_SETTINGS_MODULE" not in os.environ:
        logging.error("Error: DJANGO_SETTINGS_MODULE is not set.")
        sys.exit(1)

    check_virtual_env()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logging.critical(
            "Couldn't import Django. Ensure it's installed and available on your PYTHONPATH. "
            "Did you forget to activate a virtual environment?"
        )
        raise ImportError from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
