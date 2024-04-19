# Generated by Django 5.0.4 on 2024-04-19 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_telegramchat_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chat_id', models.BigIntegerField(unique=True)),
                ('from_chat_id', models.BigIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
