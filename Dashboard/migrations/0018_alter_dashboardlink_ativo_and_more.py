# Generated by Django 4.2.3 on 2023-08-23 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0017_dashboardlink_nome_relatorio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardlink',
            name='ativo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dashboardlink',
            name='nome_relatorio',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
