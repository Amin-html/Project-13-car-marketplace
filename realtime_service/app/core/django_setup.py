import sys
import os
import django

sys.path.insert(0, "/django_core")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()