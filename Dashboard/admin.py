from django.contrib import admin
from Dashboard import models


@admin.register(models.DashboardLink)
class DashboardLinkAdmin(admin.ModelAdmin):
    list_display = 'group', 'link_dashboard', 'ativo'
    list_editable = 'ativo',
    ordering = '-id',
