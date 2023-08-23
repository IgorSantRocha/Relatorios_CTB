from django.shortcuts import render, get_object_or_404
from Dashboard.models import DashboardLink

# Create your views here.


def index(request):
    user = request.user
    usuario_adm = user.groups.filter(name='BKO-CTB').exists()
    user_groups = user.groups.all()  # Obtém todos os grupos do usuário
    template = 'Dashboard/index.html'

    if usuario_adm:
        links = DashboardLink.objects\
            .all()\
            .order_by('-id')
    else:
        links = DashboardLink.objects\
            .filter(ativo=True, group__in=user_groups)\
            .order_by('id')

    context = {
        'usuario_adm': usuario_adm,
        'links': links,
        'site_title': 'C-Trends BPO - Relatórios'
    }

    return render(
        request,
        template,
        context,
    )


def relatorio(request, link_id):
    user = request.user
    usuario_adm = user.groups.filter(name='ADM-CTB').exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()
    user_groups = user.groups.all()  # Obtém todos os grupos do usuário
    template = 'Dashboard/dashboard.html'
    print(usuario_bko)
    # link = DashboardLink.objects.filter(pk=link_id).first()
    if not usuario_adm and not usuario_bko:
        link = get_object_or_404(DashboardLink, pk=link_id,
                                 ativo=True, group__in=user_groups)
    else:
        link = get_object_or_404(DashboardLink, pk=link_id)

    context = {
        'usuario_adm': usuario_adm,
        'link': link,
        'site_title': 'C-Trends BPO - Dashboard'
    }

    return render(
        request,
        template,
        context,
    )
