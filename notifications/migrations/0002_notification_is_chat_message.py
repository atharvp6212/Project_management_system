# Generated by Django 5.1.1 on 2024-10-13 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_chat_message',
            field=models.BooleanField(default=False),
        ),
    ]
