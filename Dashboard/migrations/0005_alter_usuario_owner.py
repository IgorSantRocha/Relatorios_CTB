# Generated by Django 4.2.4 on 2023-08-21 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Dashboard', '0004_nivel_link_dashboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
    ]
