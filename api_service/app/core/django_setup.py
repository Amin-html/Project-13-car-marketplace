import os
import sys
import django

# путь до django_core внутри контейнера (см. volume в docker-compose)
sys.path.insert(0, "/django_core")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()