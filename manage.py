#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import sys

from django.core.management import call_command

from boot_django import boot_django


def main():
    """Run administrative tasks."""
    args = list(sys.argv)[1:]
    boot_django()
    call_command(*args)


if __name__ == "__main__":
    main()
