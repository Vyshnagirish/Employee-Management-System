# Generated by Django 4.2 on 2023-07-26 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_messages_messagefrom'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='attachment',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
