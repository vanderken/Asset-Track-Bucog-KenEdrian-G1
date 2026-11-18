from django.contrib import admin
from .models import Device, Category, Checkout, MaintenanceLog, SystemSettings

admin.site.register(Device)
admin.site.register(Category)
admin.site.register(Checkout)
admin.site.register(MaintenanceLog)
admin.site.register(SystemSettings)
