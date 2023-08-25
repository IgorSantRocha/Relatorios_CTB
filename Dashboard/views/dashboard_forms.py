from django.shortcuts import render, redirect, get_object_or_404
from Dashboard.forms import DashboardLinkForm
from django.urls import reverse
from Dashboard.models import DashboardLink
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required


@permission_required('Dashboard.pode_criar_relatorio')
@login_required(login_url='Dashboard:login')
def create(request):
    form_action = reverse('Dashboard:create')
    user = request.user
    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()

    template = 'Dashboard/create.html'

    if not usuario_adm:
        return render(
            request,
            'Dashboard/grupo_nao_encontrado.html',
        )

    if request.method == 'POST':
        form = DashboardLinkForm(request.POST)

        context = {
            'usuario_adm': usuario_adm,
            'usuario_bko': usuario_bko,
            'site_title': 'C-Trends BPO - Relatórios',
            'form': form,
            'form_action': form_action
        }

        if form.is_valid():
            form.save()  # type: ignore
            messages.success(request, 'Novo relatório adicionado com sucesso!')
            return redirect('Dashboard:index')

        return render(
            request,
            template,
            context,
        )

    context = {
        'usuario_adm': usuario_adm,
        'usuario_bko': usuario_bko,
        'site_title': 'Adicionar relatório - C-Trends BPO!',
        # Passa a solicitação para o formulário
        'form': DashboardLinkForm(request=request),
        'form_action': form_action
    }

    return render(
        request,
        template,
        context,
    )


@permission_required('Dashboard.pode_editar_relatorio')
@login_required(login_url='Dashboard:login')
def update(request, link_id):
    relatorio = get_object_or_404(
        DashboardLink, pk=link_id
    )
    form_action = reverse('Dashboard:update', args=(link_id,))
    user = request.user
    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()
    template = 'Dashboard/create.html'

    if not usuario_adm:
        return render(
            request,
            'Dashboard/grupo_nao_encontrado.html',
        )

    if request.method == 'POST':
        form = DashboardLinkForm(request.POST, instance=relatorio)

        context = {
            'usuario_adm': usuario_adm,
            'usuario_bko': usuario_bko,
            'site_title': 'Atualizar relatório - C-Trends BPO!',
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Relatório atualizado com sucesso!')
            return redirect('Dashboard:index')

        return render(
            request,
            template,
            context,
        )

    context = {
        'usuario_adm': usuario_adm,
        'usuario_bko': usuario_bko,
        'site_title': 'C-Trends BPO - Relatórios',
        'form': DashboardLinkForm(instance=relatorio),
        'form_action': form_action
    }

    return render(
        request,
        template,
        context,
    )


@permission_required('Dashboard.pode_deletar_relatorio')
@login_required(login_url='Dashboard:login')
def delete(request, link_id):
    user = request.user
    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()
    editar = True

    if not usuario_adm:
        return redirect('Dashboard:index')

    link = get_object_or_404(
        DashboardLink, pk=link_id
    )
    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        link.delete()
        messages.info(request, '1 relatório foi deletado!')
        return redirect('Dashboard:index')
    else:
        messages.warning(
            request, 'Confirme se realmente deseja deletar o relatório')

    return render(
        request,
        'Dashboard/dashboard.html',
        {
            'link': link,
            'usuario_adm': usuario_adm,
            'usuario_bko': usuario_bko,
            'confirmation': confirmation,
            'editar': editar
        }
    )
    # relatorio.delete()
    # return redirect('Dashboard:index')
