# Generated by Django 3.1.3 on 2023-06-12 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='thumnail',
            new_name='thumbnail',
        ),
    ]
