# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.

import os

import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "miniexplorer"))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=("miniexplorer",),
        TIME_ZONE="UTC",
        USE_TZ=True,
        LOCALE_PATHS=[
            os.path.join(BASE_DIR, "locale"),
        ],
        LANGUAGE_CODE="pt-BR",
        ROOT_URLCONF=os.path.join(BASE_DIR, "../sample_project/sample_project/urls"),
    )

    django.setup()
