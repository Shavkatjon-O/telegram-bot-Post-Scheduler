from django.db import models
from common.models import BaseModel


class TelegramAdmin(BaseModel):
    chat_id = models.PositiveIntegerField(unique=True)

    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.chat_id}"


class TelegramChat(BaseModel):
    chat_id = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.chat_id}"
