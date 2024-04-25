from django.shortcuts import render, redirect, get_object_or_404
from Dashboard.forms import DashboardLinkForm
from django.urls import reverse
from Dashboard.models import DashboardLink, RelatoriosBi
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
import csv
from django.http import StreamingHttpResponse
from django.utils.encoding import smart_str


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


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@login_required(login_url='Dashboard:login')
def export(request, link_id):
    user = request.user
    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()
    dashboard_link = get_object_or_404(DashboardLink, pk=link_id)
    cod_cliente = dashboard_link.cod_cliente

    # Realize a consulta à sua tabela e obtenha os dados
    queryset = RelatoriosBi.objects.filter(cod_cliente=cod_cliente)
    """A view that streams a large CSV file."""

    # Define o nome do arquivo CSV e as colunas
    if usuario_adm:
        group = dashboard_link.group.name.replace(' ', '_')
        filename = f"AcompanhamentoCarteira{group}.csv"
    else:
        filename = "AcompanhamentoCarteira.csv"
    '''columns = ['os', 'serial_esperado', 'serial_chegou',
               'bordero', 'documento', 'empresa',
               'cep', 'cidade', 'uf',
               'codacao', 'descricao', 'status_caso',
               'mesano', 'dtentrada', 'motivo']  '''  # Adicione mais colunas conforme necessário
    columns = [
        field.name for field in RelatoriosBi._meta.get_fields() if field.name not in ('id', 'cod_cliente')]

    def generate_rows():
        # Escreve as colunas no arquivo CSV
        yield columns

        # Escreve os dados da consulta no arquivo CSV
        for item in queryset:
            # Use getattr para obter dinamicamente os valores dos campos do modelo
            row = [getattr(item, field) for field in columns]
            yield row

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    response = StreamingHttpResponse(
        (writer.writerow(row) for row in generate_rows()),
        content_type="text/csv"
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
