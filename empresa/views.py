from datetime import datetime
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import requests
from django.http import JsonResponse


from django.contrib import messages 
from django.contrib.messages import constants

from autenticacao.models import Users
from empresa.models import Cargo, Funcionario
from django.db.models import Q,Sum
from django.utils import timezone
from urllib.parse import unquote


from funcionario.models import Rembolso


def home_empresa (request):
    return render(request,'home_empresa.html')

def funcionarios_empresa(request):
    if request.method == 'GET':

        funcionarios = Funcionario.objects.filter(user_empresa=request.user, aceito = True, status = 'A')
    
    elif request.method == 'POST' :
        busca_nome =request.POST.get('busca_nome')
        botao_nome = request.POST.get('botao_nome')
        if botao_nome:
            return redirect(reverse('rembolsos_empresa') + f'?nome={botao_nome}')
        if busca_nome:
        
            funcionarios = Funcionario.objects.filter(
                user_empresa=request.user,
                aceito=True,
                status='A',
                user_funcionario__first_name__icontains=busca_nome
                ).order_by('user_funcionario__first_name') | Funcionario.objects.filter(
                    user_empresa=request.user,
                    aceito=True,
                    status='A',
                    user_funcionario__last_name__icontains=busca_nome
                    ).order_by('user_funcionario__last_name')
    
    return render(request,'funcionarios_empresa.html',{'funcionarios':funcionarios})

def rembolsos_empresa(request):
    if request.method == 'GET':
        input_nome = request.GET.get('nome', '').strip()
        input_nome = unquote(input_nome).replace("+", " ")
        
        print(input_nome)

        if input_nome:
            # Busca pelo nome do funcionário
            rembolsos = Rembolso.objects.filter(
                Q(user_funcionario__first_name__icontains=input_nome) |
                Q(user_funcionario__last_name__icontains=input_nome) |
                Q(user_funcionario__first_name__icontains=input_nome.split()[0],user_funcionario__last_name__icontains=input_nome.split()[1]),
                user_empresa=request.user,

            )
            busca_nome = input_nome.split()[0] + " " + input_nome.split()[1]
            print('Buscou apenas por nome')
            input_pago = None
            
            #Pegando valor total de rembolsos não pagos
            valor_total = rembolsos.aggregate(total=Sum('preco'))['total']
            # Formatando valor com 2 casas decimais 
            valor_total = '{:,.2f}'.format(valor_total) if valor_total is not None else '0,00'
            
            return render(request,'rembolsos_empresa.html',{'rembolsos':rembolsos,'pago':input_pago,'valor_total':valor_total, 'busca_nome':busca_nome,})


        else:       
            # Setando rembolsos como não pagos por padrão
            input_pago = False
            
            # Pegando rembolsos não pagos 
            rembolsos = Rembolso.objects.filter(
                user_empresa = request.user,
                pago = input_pago
                )
        
        #Pegando valor total de rembolsos não pagos
        valor_total = rembolsos.aggregate(total=Sum('preco'))['total']
        # Formatando valor com 2 casas decimais 
        valor_total = '{:,.2f}'.format(valor_total) if valor_total is not None else '0,00'
        return render(request,'rembolsos_empresa.html',{'rembolsos':rembolsos,'pago':input_pago,'valor_total':valor_total})
        
    elif request.method == 'POST' :
        
        input_nome = request.POST.get('nome', '').strip()
        input_data = request.POST.get('data', '').strip()
        input_pago = request.POST.get('pago', '').strip()

        # Convertendo o input_pago para o tipo booleano
        if input_pago == 'N':
            input_pago = False
        elif input_pago == 'S':
            input_pago = True
        else:
            input_pago = None

        # Filtrar objetos de acordo com as condições fornecidas
        if input_nome and not input_data and input_pago is None:
            # Busca pelo nome do funcionário
            rembolsos = Rembolso.objects.filter(
                Q(user_funcionario__first_name__icontains=input_nome) |
                Q(user_funcionario__last_name__icontains=input_nome) |
                Q(user_funcionario__first_name__icontains=input_nome.split(), user_funcionario__last_name__icontains=input_nome.split()),
                user_empresa=request.user,

            )
            print('Buscou apenas por nome')
            
        elif input_data and not input_nome and input_pago is None:
            # Convertendo a entrada de mês/ano para uma data completa (primeiro dia do mês)
            data_completa = timezone.datetime.strptime(input_data, '%Y-%m')
            rembolsos = Rembolso.objects.filter(
                    user_empresa=request.user,
                    data_comprovante__year=data_completa.year,
                    data_comprovante__month=data_completa.month
                )
            print('Buscou apenas por mês/ano')
            
        elif input_pago is not None and not input_nome and not input_data:
            rembolsos = Rembolso.objects.filter(
                user_empresa=request.user,
                pago=input_pago
                )
            print('Buscou apenas por status')
            
        elif input_nome and input_data and input_pago is None:
            # Convertendo a entrada de mês/ano para uma data completa (primeiro dia do mês)
            data_completa = timezone.datetime.strptime(input_data, '%Y-%m')
            rembolsos = Rembolso.objects.filter(
                Q(user_funcionario__first_name__icontains=input_nome) |
                Q(user_funcionario__last_name__icontains=input_nome) |
                Q(user_funcionario__first_name__icontains=input_nome.split(),user_funcionario__last_name__icontains=input_nome.split()),
                user_empresa=request.user,
            )
            rembolsos = rembolsos.filter(
                data_comprovante__year=data_completa.year,
                data_comprovante__month=data_completa.month
                )
            print('Buscou por nome e mês/ano')
            
        elif input_nome and input_pago is not None and not input_data:
            # Busca pelo nome do funcionário e pelo status do pagamento
            rembolsos = Rembolso.objects.filter(
                Q(user_funcionario__first_name__icontains=input_nome) |
                Q(user_funcionario__last_name__icontains=input_nome) |
                Q(user_funcionario__first_name__icontains=input_nome.split(), user_funcionario__last_name__icontains=input_nome.split()),
                pago=input_pago,
                user_empresa=request.user
            )
            print('Buscou por nome e status')
            
        elif input_data and input_pago is not None and not input_nome:
            # Convertendo a entrada de mês/ano para uma data completa (primeiro dia do mês)
            data_completa = timezone.datetime.strptime(input_data, '%Y-%m')
            rembolsos = Rembolso.objects.filter(
                data_comprovante__year=data_completa.year,
                data_comprovante__month=data_completa.month,
                pago=input_pago,
                user_empresa=request.user,
                )
            print('Buscou por mês/ano e status')
            
        elif input_nome and input_data and input_pago is not None:
            # Convertendo a entrada de mês/ano para uma data completa (primeiro dia do mês)
            data_completa = timezone.datetime.strptime(input_data, '%Y-%m')
            rembolsos = Rembolso.objects.filter(
                Q(user_funcionario__first_name__icontains=input_nome) |
                Q(user_funcionario__last_name__icontains=input_nome) |
                Q(user_funcionario__first_name__icontains=input_nome.split(), user_funcionario__last_name__icontains=input_nome.split()),
                data_comprovante__year=data_completa.year, 
                data_comprovante__month=data_completa.month, 
                pago=input_pago,
                user_empresa=request.user,
            )
            print('Buscou por nome, mês/ano e status')
            
        elif input_nome == '' and input_data == '' and input_pago is None:
            # Quando nenhum filtro é aplicado
            rembolsos = Rembolso.objects.filter(user_empresa=request.user)
            print('Buscou por qualquer combinação de nome, mês/ano e status')
            
        else:
            rembolsos = Rembolso.objects.none()
            print('Nenhuma busca foi realizada ou combinação inválida')

    #Pegando valor total de rembolsos não pagos
    valor_total = rembolsos.aggregate(total=Sum('preco'))['total']
    # Formatando valor com 2 casas decimais 
    valor_total = '{:,.2f}'.format(valor_total) if valor_total is not None else '0,00'
        
    return render(request,'rembolsos_empresa.html',{'rembolsos':rembolsos,'pago':input_pago,'valor_total':valor_total,'busca_nome':input_nome,'ano_mes':input_data})

def solicitacoes_vinculo (request):
    
    # Pegando Funcionarios com aceito = False e com status = espera
    solicitacoes = Funcionario.objects.filter(user_empresa = request.user, aceito = False, status = 'E')
    return render(request,'solicitacoes_vinculo.html',{'solicitacoes':solicitacoes})

def aceitar_vinculo (request,id_vinculo):
    
    try:
        funcionario = Funcionario.objects.get(pk = id_vinculo, user_empresa = request.user)
        funcionario.aceito = True
        funcionario.status = 'A'
        funcionario.save()
        messages.add_message(request, constants.SUCCESS, 'Funcionario aceito com sucesso') 

    except Exception as e:
        messages.add_message(request, constants.ERROR, f'Erro ao tentar aceitar usuario: {e}') 

    return redirect(reverse('solicitacoes_vinculo')) 

def negar_vinculo (request,id_vinculo):
    
    try:
        funcionario = Funcionario.objects.get(pk = id_vinculo, user_empresa = request.user)
        funcionario.delete()
        messages.add_message(request, constants.SUCCESS, 'Funcionario recusado com sucesso') 

    except Exception as e:
        messages.add_message(request, constants.ERROR, f'Erro ao tentar recusar usuario: {e}') 

    return redirect(reverse('solicitacoes_vinculo')) 

def demitir_funcionario (request,id_vinculo):
    
    try:
        funcionario = Funcionario.objects.get(pk = id_vinculo, user_empresa = request.user)
        funcionario.delete()
        messages.add_message(request, constants.SUCCESS, 'Funcionario demitido com sucesso') 

    except Exception as e:
        messages.add_message(request, constants.ERROR, f'Erro ao tentar demitir usuario: {e}') 

    return redirect(reverse('funcionarios_empresa')) 

def cadastrar_cargo (request):
    
    if request.method == 'POST':
        input_cargo = request.POST['cargo']
        
        if input_cargo.strip == '':
            messages.add_message(request, constants.ERROR, 'Não é possivel criar cargo vazio') 

        
        try:
            cargo = Cargo(
                user_empresa = request.user,
                cargo = input_cargo
            )
            cargo.save()
            messages.add_message(request, constants.SUCCESS, 'Cargo criado com sucesso') 

        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro inesperado ao tentar salvar cargo') 
    
    return render(request,'cadastrar_cargo.html')

def registrar_pagamento_reembolso(request,id_reembolso):
    try:
        reembolso = Rembolso.objects.get(pk=id_reembolso,user_empresa = request.user)
        reembolso.pago = True
        reembolso.save()
        messages.add_message(request, constants.SUCCESS, 'Reembolso setado com pago') 

    except Exception as e:
        print(e)
        messages.add_message(request, constants.ERROR, 'Erro inesperado ao tentar salvar reembolso como pago') 
    return redirect(reverse('detalhes_rembolso', kwargs={'id_rembolso': id_reembolso}))

def retirar_pagamento_reembolso(request,id_reembolso):
    try:
        reembolso = Rembolso.objects.get(pk=id_reembolso,user_empresa = request.user)
        reembolso.pago = False
        reembolso.save()
        messages.add_message(request, constants.SUCCESS, 'Reembolso setado com não pago') 

    except Exception as e:
        print(e)
        messages.add_message(request, constants.ERROR, 'Erro inesperado ao tentar salvar reembolso como pago') 
    return redirect(reverse('detalhes_rembolso', kwargs={'id_rembolso': id_reembolso}))


# API

from django.core import serializers

def cargos_disponiveis(request, empresa_id):
    user_empresa = Users.objects.get(pk=empresa_id)
    cargos_disponiveis = Cargo.objects.filter(user_empresa=user_empresa)
    
    # Serializar o QuerySet para JSON
    cargos_json = [{'cargo': instancia_cargo.cargo,'id':instancia_cargo.pk} for instancia_cargo in cargos_disponiveis]
    print(cargos_json)
    return JsonResponse(cargos_json, safe=False)
