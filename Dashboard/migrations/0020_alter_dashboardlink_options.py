# Generated by Django 4.2.4 on 2023-08-25 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0019_alter_dashboardlink_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dashboardlink',
            options={'permissions': [('pode_editar_relatorio', 'Pode editar relatórios'), ('pode_criar_relatorio', 'Pode criar relatórios'), ('pode_deletar_relatorio', 'Pode apagar relatórios')], 'verbose_name': 'Link Dashboard', 'verbose_name_plural': 'Links Dashboards'},
        ),
    ]
