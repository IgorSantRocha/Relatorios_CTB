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

    def __str__(self) -> str:
        return self.group.name  # type:ignore


'''class Usuario(models.Model):
    user = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    created_date = models.DateTimeField(default=timezone.now)  # type: ignore
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    Nivel = models.ForeignKey(
        Nivel,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self) -> str:
        return f'{self.user} {self.user_name}'''
