# Generated by Django 4.2.4 on 2023-08-21 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0002_rename_contratante_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='first_name',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='last_name',
            new_name='user_name',
        ),
    ]
