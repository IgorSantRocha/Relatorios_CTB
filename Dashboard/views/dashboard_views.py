from django.shortcuts import render, get_object_or_404
from Dashboard.models import DashboardLink
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='Dashboard:login')
def index(request):
    user = request.user
    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()
    usuario_ctb = user.groups.filter(name='C-TRENDS').exists()
    user_groups = user.groups.all()  # Obtém todos os grupos do usuário
    template = 'Dashboard/index.html'

    if usuario_adm:
        links = DashboardLink.objects\
            .all()\
            .order_by('-id')
    elif usuario_ctb:
        links = DashboardLink.objects\
            .filter(ativo=True)\
            .order_by('id')

    else:
        links = DashboardLink.objects\
            .filter(ativo=True, group__in=user_groups)\
            .order_by('id')

    context = {
        'usuario_adm': usuario_adm,
        'usuario_bko': usuario_bko,
        'usuario_ctb': usuario_ctb,
        'links': links,
        'site_title': 'C-Trends BPO - Relatórios'
    }

    return render(
        request,
        template,
        context,
    )


@login_required(login_url='Dashboard:login')
def relatorio(request, link_id):
    user = request.user
    usuario_adm = user.groups.filter(name='C-TRENDS').exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()
    user_groups = user.groups.all()  # Obtém todos os grupos do usuário
    editar = False
    template = 'Dashboard/dashboard.html'

    # link = DashboardLink.objects.filter(pk=link_id).first()
    if not usuario_adm:
        link = get_object_or_404(DashboardLink, pk=link_id,
                                 ativo=True, group__in=user_groups)
    else:
        link = get_object_or_404(DashboardLink, pk=link_id)

        if link.group in user_groups:
            editar = True
        elif usuario_bko and link.group.name != 'SUP-CTB':  # type: ignore
            editar = True

    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()

    context = {
        'usuario_adm': usuario_adm,
        'usuario_bko': usuario_bko,
        'editar': editar,
        'link': link,
        'site_title': 'C-Trends BPO - Dashboard'
    }

    return render(
        request,
        template,
        context,
    )
