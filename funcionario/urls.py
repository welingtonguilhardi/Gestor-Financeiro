
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_funcionario, name = "home_funcionario"),
    path('solicitar_vinculo/',views.solicitar_vinculo, name='solicitar_vinculo'),
    path('cadastrar_rembolso/', views.cadastrar_rembolso, name='cadastrar_rembolso'),
    path('rembolsos_funcionario/', views.rembolsos_funcionario, name='rembolsos_funcionario'),
    path('detalhes_rembolso/<str:id_rembolso>/', views.detalhes_rembolso ,name='detalhes_rembolso'),
]
