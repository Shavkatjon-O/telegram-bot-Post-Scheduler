from django.contrib import admin
from . import models

admin.site.register(models.TelegramAdmin)
admin.site.register(models.TelegramChat)
admin.site.register(models.TelegramPost)
