# Generated by Django 5.0.4 on 2024-04-19 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_telegramchat'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramchat',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]