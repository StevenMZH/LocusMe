from django.contrib import admin
from .models import Device, ForeignDevice

admin.site.register(Device)
admin.site.register(ForeignDevice)
