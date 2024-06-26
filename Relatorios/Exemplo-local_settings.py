SECRET_KEY = 'CHANGE-ME'
# DEBUG = True
ALLOWED_HOSTS: list[str] = [
    'localhost',
    '127.0.0.1',
    # Coloque os demais IP's aqui
]
CSRF_TRUSTED_ORIGINS: list[str] = [
    'https://www.dominio.com.br',
    'http://www.dominio.com.br'
]
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'Nome_DB',
        'USER': 'user',
        'PASSWORD': 'password',
        # Pode ser o endereço do servidor SQL Server
        'HOST': 'IP ou nome do servidor',
        'PORT': '',           # Deixe vazio para usar a porta padrão

    },
}
