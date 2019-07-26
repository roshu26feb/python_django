"""
This module used to register the models to admin site
"""
from django.contrib import admin
from esmt.delivery_db.models import System, SystemVersion

admin.site.register(System)
admin.site.register(SystemVersion)
