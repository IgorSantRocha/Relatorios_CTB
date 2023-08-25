# type:ignore
from django.urls import path

from Dashboard import views

app_name = 'Dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),

    # relatorio (CRUD)
    path('relatorio/<int:link_id>/', views.relatorio,
         name='relatorio'),  # Visualizar dashboard

    path('relatorio/create', views.create,
         name='create'),  # Adicionar nova DB ou relatório

    path('relatorio/<int:link_id>/update/', views.update,
         name='update'),  # Atualizar dashboard

    path('relatorio/<int:link_id>/delete/', views.delete,
         name='delete'),  # Ocultar dashboard


    # user
    path('user/create/', views.register,
         name='register'),  # Adicionar nova DB ou relatório

    path('login/', views.login_usuario,
         name='login'),  # Adicionar nova DB ou relatório

    path('user/logout/', views.logout_usuario,
         name='logout'),  # Adicionar nova DB ou relatório

    path('user/update/', views.update_usuario,
         name='update_usuario'),  # Adicionar nova DB ou relatório

]
