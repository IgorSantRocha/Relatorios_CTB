from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from Dashboard.forms import RegisterForm, UserUpdateForm
from django.contrib import messages


def register(request):
    form = RegisterForm()
    title = 'Registrar novo usuário'

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


def logout_usuario(request):
    auth.logout(request)
    messages.info(request, 'Usuário deslogado.')
    return redirect('Dashboard:login')  # type: ignore


def update_usuario(request):
    form = UserUpdateForm(instance=request.user)
    title = 'Altere seu usuário'

    if request.method != 'POST':
        return render(
            request,
            'Dashboard/register.html',
            {
                'form': form,
                'title': title
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
