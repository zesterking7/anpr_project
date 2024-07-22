# camera/admin.py

from django.contrib import admin
from .models import LicensePlate

# Register the LicensePlate model with the admin site
admin.site.register(LicensePlate)
