# Generated by Django 5.0.4 on 2024-04-17 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_telegramadmin_first_name_telegramadmin_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chat_id', models.BigIntegerField(unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]