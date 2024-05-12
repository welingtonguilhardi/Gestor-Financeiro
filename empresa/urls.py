
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_empresa, name='home_empresa'),
    path('funcionarios/',views.funcionarios_empresa, name='funcionarios_empresa'),
    path('rembolsos_empresa/',views.rembolsos_empresa, name='rembolsos_empresa'),
    path('solicitacoes_vinculo/',views.solicitacoes_vinculo, name='solicitacoes_vinculo'),
    path('aceitar_vinculo/<int:id_vinculo>/',views.aceitar_vinculo, name='aceitar_vinculo'),
    path('negar_vinculo/<int:id_vinculo>/',views.negar_vinculo, name='negar_vinculo'),
    path('cadastrar_cargo/',views.cadastrar_cargo, name='cadastrar_cargo'),
    path('registrar_pagamento_reembolso/<id_reembolso>',views.registrar_pagamento_reembolso, name='registrar_pagamento_reembolso'),
    path('retirar_pagamento_reembolso/<id_reembolso>',views.retirar_pagamento_reembolso, name='retirar_pagamento_reembolso'),

    
    # API
    path('cargos_disponiveis/<str:empresa_id>/',views.cargos_disponiveis, name='cargos_disponiveis'),
    
]
