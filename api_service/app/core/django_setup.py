import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from listings.models import Listing  # теперь можно юзать ORM