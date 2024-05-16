from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q, Sum

from autenticacao.models import Users
from empresa.models import Cargo, Funcionario

from django.contrib import messages 
from django.contrib.messages import constants

from funcionario.models import Rembolso

def home_funcionario (request):
    return render(request, 'home_funcionario.html')


def solicitar_vinculo (request):
    
    
    solictacao = None
    
    # Verificando se já existe uma solitação feita
    try:
        solictacao = Funcionario.objects.get(user_funcionario = request.user)
    
        if solictacao.status == 'E':
            messages.add_message(request, constants.WARNING, f'Aguarde sua solicitação para empresa {solictacao.user_empresa.first_name} ser respondida') 
        elif solictacao.status == 'A':
            messages.add_message(request, constants.ERROR, 'Você já faz parte de uma empresa') 
            return redirect(reverse('home'))
    except:
        pass
    
    empresas = Users.objects.filter(tipo_user = 'e')
    
    if request.method == 'POST':
        id_user_empresa = request.POST['empresa']
        id_cargo_empresa = request.POST['cargo_select']
        
        empresa = Users.objects.get(pk = id_user_empresa, tipo_user = 'e')
        cargo_empresa = Cargo.objects.get(pk = id_cargo_empresa, user_empresa = empresa)
        
        try:
            Funcionario.objects.create(
                user_empresa = empresa,
                user_funcionario = request.user,
                cargo = cargo_empresa,
            )
            messages.add_message(request, constants.SUCCESS, 'Solicitação enviada com sucesso') 
        except Exception as e:
            print(e)
            messages.add_message(request, constants.ERROR, 'Você já tem uma solicitação em andamento') 
    
    return render(request, 'solicitar_vinculo.html',{'empresas':empresas, 'solicitacao':solictacao})

def cancelar_solicitacao (request):
    try:
        Funcionario.objects.get(user_funcionario = request.user).delete()
        messages.add_message(request, constants.SUCCESS, 'Solicitação cancelada') 
    except:
        messages.add_message(request, constants.ERROR, 'Rrro ao tentar cancelar solicitação') 

    return redirect(reverse('home'))

def cadastrar_rembolso(request):
    
    if request.method == 'POST':
        
        try:        
            input_local = request.POST.get('local', '')
            input_motivo = request.POST.get('motivo', '')
            input_preco = request.POST.get('preco', '')
            input_data_hora = request.POST.get('data_hora', '')
            input_foto_comprovante = request.FILES.get('foto_comprovante', None)
            
            input_preco = float(input_preco.replace(",", "."))

            
            empresa = Funcionario.objects.get(user_funcionario = request.user, aceito = True,status = 'A' ).user_empresa
            
            
            Rembolso.objects.create(
                local = input_local,
                motivo = input_motivo,
                preco = input_preco,
                data_comprovante = input_data_hora,
                foto_comprovante = input_foto_comprovante,
                user_empresa = empresa,
                user_funcionario = request.user
            )
            
            messages.add_message(request, constants.SUCCESS, 'Rembolso cadastrado com sucesso') 

        except Exception as e:
            print(e)
            messages.add_message(request, constants.ERROR, 'Error ao cadastrar rembolso') 

    return render(request, 'cadastrar_rembolso.html')

def rembolsos_funcionario(request):
    if request.method == 'GET':

        # Setando rembolsos como não pagos por padrão
        input_pago = False
        
        # Pegando rembolsos não pagos 
        rembolsos = Rembolso.objects.filter(
            user_funcionario = request.user,
            pago = input_pago
            )
    
        #Pegando valor total de rembolsos não pagos
        valor_total = rembolsos.aggregate(total=Sum('preco'))['total']
        # Formatando valor com 2 casas decimais 
        valor_total = '{:,.2f}'.format(valor_total) if valor_total is not None else '0,00'
        return render(request,'rembolsos_funcionario.html',{'rembolsos':rembolsos,'pago':input_pago,'valor_total':valor_total})
        
    elif request.method == 'POST' :
        
        input_data = request.POST.get('data', '').strip()
        input_pago = request.POST.get('pago', '').strip()

        # Convertendo o input_pago para o tipo booleano
        if input_pago == 'N':
            input_pago = False
        elif input_pago == 'S':
            input_pago = True
        else:
            input_pago = None


        if input_data and input_pago is None:
            # Convertendo a entrada de mês/ano para uma data completa (primeiro dia do mês)
            data_completa = timezone.datetime.strptime(input_data, '%Y-%m')
            rembolsos = Rembolso.objects.filter(
                user_funcionario = request.user,
                data_comprovante__year=data_completa.year,
                data_comprovante__month=data_completa.month
                )
            print('Buscou apenas por mês/ano')
            
        elif input_pago is not None and not input_data:
            rembolsos = Rembolso.objects.filter(
                user_funcionario = request.user,
                pago=input_pago
                )
            print('Buscou apenas por status')
            
        elif input_data and input_pago is None:
            # Convertendo a entrada de mês/ano para uma data completa (primeiro dia do mês)
            data_completa = timezone.datetime.strptime(input_data, '%Y-%m')
            rembolsos = Rembolso.objects.filter(
                user_funcionario = request.user ,
                data_comprovante__year=data_completa.year,
                data_comprovante__month=data_completa.month
                )
            print('Buscou por nome e mês/ano')
            
        elif input_pago is not None and not input_data:
            # Busca pelo nome do funcionário e pelo status do pagamento
            rembolsos = Rembolso.objects.filter(
                user_funcionario = request.user,
                pago=input_pago
            )
            print('Buscou por nome e status')
            
        elif input_data and input_pago is not None:
            # Convertendo a entrada de mês/ano para uma data completa (primeiro dia do mês)
            data_completa = timezone.datetime.strptime(input_data, '%Y-%m')
            rembolsos = Rembolso.objects.filter(
                user_funcionario = request.user,
                data_comprovante__year=data_completa.year,
                data_comprovante__month=data_completa.month,
                pago=input_pago
                )
            print('Buscou por mês/ano e status')
            
        elif input_data and input_pago is not None:
            # Convertendo a entrada de mês/ano para uma data completa (primeiro dia do mês)
            data_completa = timezone.datetime.strptime(input_data, '%Y-%m')
            rembolsos = Rembolso.objects.filter(
                user_funcionario = request.user,
                data_comprovante__year=data_completa.year,
                data_comprovante__month=data_completa.month,
                pago=input_pago
            )
            print('Buscou por nome, mês/ano e status')
            
        elif input_data == '' and input_pago is None:
            # Quando nenhum filtro é aplicado
            rembolsos = Rembolso.objects.filter(user_funcionario = request.user)
            print('Buscou por qualquer combinação de nome, mês/ano e status')
            
        else:
            rembolsos = Rembolso.objects.none()
            print('Nenhuma busca foi realizada ou combinação inválida')

    #Pegando valor total de rembolsos não pagos
    valor_total = rembolsos.aggregate(total=Sum('preco'))['total']
    # Formatando valor com 2 casas decimais 
    valor_total = '{:,.2f}'.format(valor_total) if valor_total is not None else '0,00'
        
    return render(request,'rembolsos_empresa.html',{'rembolsos':rembolsos,'pago':input_pago,'valor_total':valor_total,'ano_mes':input_data})
from django.shortcuts import get_object_or_404

def detalhes_rembolso(request,id_rembolso):

    try:
        rembolso = Rembolso.objects.get(pk=id_rembolso, user_empresa=request.user)
    except Rembolso.DoesNotExist:
        try:
            rembolso = Rembolso.objects.get(pk=id_rembolso, user_funcionario=request.user)
        except Rembolso.DoesNotExist:
            # Se nenhum dos dois casos for encontrado, retorna um erro
            messages.add_message(request, constants.ERROR, 'Você não está envolvido nesse rembolso') 
            return redirect(reverse('home'))
    eh_empresa = rembolso.user_empresa == request.user
    return render (request,'detalhes_rembolso.html',{'rembolso':rembolso,'eh_empresa':eh_empresa})