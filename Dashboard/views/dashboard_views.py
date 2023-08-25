from django.shortcuts import render, get_object_or_404, redirect
from Dashboard.models import DashboardLink
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.


@login_required(login_url='Dashboard:login')
def index(request):
    user = request.user
    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()
    usuario_ctb = user.groups.filter(name='C-TRENDS').exists()
    user_groups = user.groups.all()  # Obtém todos os grupos do usuário
    template = 'Dashboard/index.html'
    mostrar_campo_pesquisa = True

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

    paginator = Paginator(links, 10)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'usuario_adm': usuario_adm,
        'usuario_bko': usuario_bko,
        'usuario_ctb': usuario_ctb,
        'page_obj': page_obj,
        'site_title': 'Relatórios - C-Trends BPO!',
        'mostrar_campo_pesquisa': mostrar_campo_pesquisa
    }

    return render(
        request,
        template,
        context,
    )


@login_required(login_url='Dashboard:login')
def search(request):
    user = request.user
    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()
    usuario_ctb = user.groups.filter(name='C-TRENDS').exists()
    user_groups = user.groups.all()  # Obtém todos os grupos do usuário
    mostrar_campo_pesquisa = True

    search_value = request.GET.get('q', '').strip()
    if search_value == '':
        return redirect('Dashboard:index')

    template = 'Dashboard/index.html'

    if usuario_adm:
        links = DashboardLink.objects\
            .all()\
            .filter(
                Q(group__name__icontains=search_value)
                | Q(nome_relatorio__icontains=search_value)
            )\
            .order_by('-id')

    elif usuario_ctb:
        links = DashboardLink.objects\
            .filter(
                Q(ativo=True),
                Q(group__name__icontains=search_value)
                | Q(nome_relatorio__icontains=search_value)
            )\
            .order_by('id')

    else:
        links = DashboardLink.objects\
            .filter(
                Q(ativo=True),
                Q(group__in=user_groups)
                | Q(nome_relatorio__icontains=search_value)
            )\
            .order_by('id')

    paginator = Paginator(links, 20)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'usuario_adm': usuario_adm,
        'usuario_bko': usuario_bko,
        'usuario_ctb': usuario_ctb,
        'page_obj': page_obj,
        'site_title': 'Relatórios - C-Trends BPO!',
        'mostrar_campo_pesquisa': mostrar_campo_pesquisa
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
        'site_title': link.nome_relatorio + ' - C-Trends BPO!'
    }

    return render(
        request,
        template,
        context,
    )
