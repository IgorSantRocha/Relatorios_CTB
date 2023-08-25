from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from Dashboard.forms import RegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda user: user.has_perm('auth.add_user'))
@login_required(login_url='Dashboard:login')
def register(request):
    # user = request.user
    form = RegisterForm()
    title = 'Registrar novo usuário'

    # if not user.is_authenticated:
    #   print('aaaaaaaaaaaaaaaa')
    # messages.info(request, 'Essa é a tela de registro de usuário')
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado com sucesso!')
            return redirect('Dashboard:index')

    return render(
        request,
        'Dashboard/register.html',
        {
            'form': form,
            'title': title
        },
    )


def login_usuario(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(
                request, f'Olá, {user.first_name}. Seja bem vindo!')
            return redirect('Dashboard:index')

    return render(
        request,
        'Dashboard/login.html',
        {'form': form},
    )


@login_required(login_url='Dashboard:login')
def logout_usuario(request):
    auth.logout(request)
    messages.info(request, 'Usuário deslogado.')
    return redirect('Dashboard:login')  # type: ignore


@login_required(login_url='Dashboard:login')
def update_usuario(request):
    user = request.user
    form = UserUpdateForm(instance=request.user)
    title = 'Altere seu usuário'
    usuario_adm = user.groups.filter(name__in=['SUP-CTB', 'BKO-CTB']).exists()
    usuario_bko = user.groups.filter(name='BKO-CTB').exists()

    if request.method != 'POST':
        return render(
            request,
            'Dashboard/register.html',
            {
                'form': form,
                'title': title,
                'usuario_adm': usuario_adm,
                'usuario_bko': usuario_bko
            },
        )

    form = UserUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'Dashboard/register.html',
            {'form': form},
        )

    form.save()
    messages.success(request, 'Usuário atualizado com sucesso!')
    return redirect('Dashboard:update_usuario')
