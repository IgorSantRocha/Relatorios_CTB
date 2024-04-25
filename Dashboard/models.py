from django.db import models
from django.contrib.auth.models import Group


class DashboardLink(models.Model):
    class Meta:
        verbose_name = 'Link Dashboard'
        verbose_name_plural = 'Links Dashboards'
        permissions = [
            ("pode_editar_relatorio", "Pode editar relatórios"),
            ("pode_criar_relatorio", "Pode criar relatórios"),
            ("pode_deletar_relatorio", "Pode apagar relatórios"),
        ]

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Contratante'
    )
    nome_relatorio = models.CharField(max_length=50, blank=True)
    link_dashboard = models.URLField(blank=True)
    ativo = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    cod_cliente = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.group.name  # type:ignore


class RelatoriosBi(models.Model):
    class Meta:
        db_table = 'TB_Relatorios_BI'
        verbose_name = 'Base Dashboard'
        verbose_name_plural = 'Bases Dashboards'

    os = models.CharField(max_length=50, blank=True)
    serial_esperado = models.CharField(max_length=50, blank=True)
    serial_chegou = models.CharField(max_length=50, blank=True)
    bordero = models.CharField(max_length=50, blank=True)
    documento = models.CharField(max_length=20, blank=True)
    empresa = models.CharField(max_length=250, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    cidade = models.CharField(max_length=50, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    codacao = models.CharField(max_length=5, blank=True)
    descricao = models.CharField(max_length=100, blank=True)
    status_caso = models.CharField(max_length=25, blank=True)
    mesano = models.CharField(max_length=10, blank=True)
    dtentrada = models.DateField(blank=True)
    motivo = models.TextField(blank=True)
    Data_Limite = models.DateField(blank=True)
    StatusCliente = models.CharField(max_length=50, blank=True)
    cod_cliente = models.CharField(max_length=100, blank=True)
