# settings_dev.py
from .settings import *

MIGRATION_MODULES = {
    'auth': None,  # Desactiva las migraciones para `auth`
    'contenttypes': None,  # Desactiva las migraciones para `contenttypes`
}
