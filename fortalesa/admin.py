from django.contrib import admin
from fortalesa import models
# Register your models here.

admin.site.register(models.Casteller)
admin.site.register(models.EventType)
admin.site.register(models.Event)

