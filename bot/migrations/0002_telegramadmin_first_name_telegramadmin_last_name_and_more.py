# Generated by Django 5.0.4 on 2024-04-16 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramadmin',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='telegramadmin',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='telegramadmin',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]