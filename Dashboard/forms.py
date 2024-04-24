from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from . import models
from django.contrib.auth import password_validation


class DashboardLinkForm(forms.ModelForm):

    link_dashboard = forms.URLField(
        label='Link para o relatório',
    )
    description = forms.CharField(
        label='Descrição do relatório'
    )
    ativo = forms.ChoiceField(
        label='Ativo',
        choices=[(True, 'Ativo'), (False, 'Inativo')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cod_cliente = forms.CharField(
        label='Código do cliente'
    )

    class Meta:
        model = models.DashboardLink
        fields = 'nome_relatorio', 'group', 'link_dashboard', \
            'description', 'ativo', 'cod_cliente'

    def __init__(self, *args, **kwargs):
        # Pega a solicitação dos argumentos
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['ativo'].initial = str(self.instance.ativo)
        elif request and request.method == 'GET':
            # Define o valor padrão para GET
            self.fields['ativo'].initial = str(False)

    def clean(self):
        return super().clean()


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.exclude(
            name__in=['ADM-CTB'])

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), empty_label='----',
        label='Contratante',
    )

    first_name = forms.CharField(
        required=True,
        label='Nome completo',
        min_length=2
    )
    email = forms.EmailField(
        required=True,
        label='Endereço de e-mail'
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'email',
            'username', 'password1', 'password2',
            'group',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                forms.ValidationError(
                    'E-mail já cadastrado!',
                    code='invalid'
                )
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['group'])
        return user


class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        label='Nome do usuário',
        help_text=('Esse é o nome que será exibido na tela. \
                   Não é possível alterar o user de login'),
        min_length=5,
        max_length=30,
        required=True,
        error_messages={
            'min_length': 'O nome deve ter 5 ou mais letras'
        }
    )

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Senha 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Confirme a nova senha.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = cleaned_data.get('password1')
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    forms.ValidationError(
                        'As senhas não batem!',
                        'invalid'
                    )
                )

        return super().clean()

    '''def clean_email(self):
        email = self.cleaned_data.get('email')
        email_atual = self.instance.email

        if email_atual != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    forms.ValidationError(
                        'E-mail já cadastrado!',
                        code='invalid'
                    )
                )

        return email
    '''

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except forms.ValidationError as errors:
                self.add_error(
                    'password1',
                    forms.ValidationError(errors)
                )

        return password1
