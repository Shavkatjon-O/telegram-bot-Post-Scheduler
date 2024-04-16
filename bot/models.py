from django.db import models
from common.models import BaseModel


class TelegramAdmin(BaseModel):
    chat_id = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"{self.chat_id}"
