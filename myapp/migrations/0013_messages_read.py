# Generated by Django 4.2 on 2023-09-12 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_messages_send_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
