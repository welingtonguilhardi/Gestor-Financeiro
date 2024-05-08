from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from autenticacao.models import Users #importa a class de usuario do django 
from django.contrib import messages #importa as mensagens de verificação
from django.contrib.messages import constants #importa o modulo constants das mensagens de verificação
from django.contrib import auth
from django.urls import reverse #importa o modulo de autenticação de usuario do django  

def cadastro(request):
    
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:# verificação se meu usuario já está logado
            
            return redirect('/')

        
        return render(request, 'cadastro.html')

    elif request.method == 'POST':

        
        inputs = {
            'username' : request.POST.get('username'),
            'senha' : request.POST.get('password') ,
            'confirmar_senha' : request.POST.get('confirm-password'),
            'first_name': request.POST.get('first_name') ,
            'last_name' : request.POST.get('last_name'),
            'email' : request.POST.get('email')
        }
        
        documento = verifica_tipo_documento(inputs['username'])
        tipo_user = ''
        
        if documento == 'CPF' and valida_cpf(inputs['username']):
            tipo_user = 'f'
        elif documento == 'CNPJ' and valida_cnpj(inputs['username']):
            tipo_user = 'e'
        else:
            messages.add_message(request, constants.ERROR, 'Documento invalido') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return render(request, 'cadastro.html',inputs)
                    
        if not inputs['senha'] == inputs['confirmar_senha']:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return render(request, 'cadastro.html',inputs)
        
        elif len(inputs['username'].strip()) == 0 or len(inputs['senha'].strip()) == 0:  #funçao strip é para o usuario não conseguir cadastrar uma senha só com espaço como exemplo senha = '    '           
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return render(request, 'cadastro.html',inputs)
        
        busca_cpf_cnpj = Users.objects.filter(username = inputs['username'])
        busca_email = Users.objects.filter(email = inputs['email'])
        
        if busca_cpf_cnpj.exists():
            messages.add_message(request, constants.ERROR, 'CPF OU CNPJ já existe') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return render(request, 'cadastro.html',inputs)
        
        elif busca_email.exists():
            messages.add_message(request, constants.ERROR, 'Email já existe') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return render(request, 'cadastro.html',inputs)
        
        try:
            
            user = Users.objects.create_user(
                    username=inputs['username'],
                    password=inputs['senha'],
                    first_name = inputs['first_name'],
                    last_name = inputs['last_name'],
                    tipo_user = tipo_user,
                    email = inputs['email']
                    
                )
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return redirect(reverse('logar'))
        
        except Exception as e:
            print(e)    
            messages.add_message(request, constants.ERROR, 'Erro no sistema') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return render(request, 'cadastro.html',inputs)
        
def verifica_tipo_documento(documento):
    # Removendo caracteres não numéricos do username
    documento = ''.join(filter(str.isdigit, documento))

    # Verificando o tamanho do username para determinar se é CPF ou CNPJ
    if len(documento) == 11:
        return "CPF"
    elif len(documento) == 14:
        return "CNPJ"
    else:
        return "Tipo de documento inválido"

def valida_cpf(cpf):
    # Removendo caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verificando se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Calculando o primeiro dígito verificador
    soma = 0
    peso = 10
    for i in range(9):
        soma += int(cpf[i]) * peso
        peso -= 1

    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    # Verificando o primeiro dígito verificador
    if digito1 != int(cpf[9]):
        return False

    # Calculando o segundo dígito verificador
    soma = 0
    peso = 11
    for i in range(10):
        soma += int(cpf[i]) * peso
        peso -= 1

    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    # Verificando o segundo dígito verificador
    if digito2 != int(cpf[10]):
        return False

    # Se passar por todas as verificações, o CPF é válido
    return True

def valida_cnpj(cnpj):
    # Removendo caracteres não numéricos do CNPJ
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verificando se o CNPJ tem 14 dígitos
    if len(cnpj) != 14:
        return False

    # Calculando o primeiro dígito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso -= 1
        if peso == 1:
            peso = 9

    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    # Verificando o primeiro dígito verificador
    if digito1 != int(cnpj[12]):
        return False

    # Calculando o segundo dígito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso -= 1
        if peso == 1:
            peso = 9

    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    # Verificando o segundo dígito verificador
    if digito2 != int(cnpj[13]):
        return False

    # Se passar por todas as verificações, o CNPJ é válido
    return True


def logar(request):
    
   if request.method == 'GET': 
       
    if request.user.is_authenticated:# verificação se meu usuario já está logado
        return redirect('/')   
       
       
    return render(request, 'logar.html')


   elif request.method == 'POST':
       username = request.POST.get('username')# obtém informaçao do campo input do cadastro conforme o name = 'username'
       senha = request.POST.get('password')# obtém informaçao do campo input do cadastro conforme o name = 'password'
       user = auth.authenticate(username=username,password=senha) #verifica no banco de dados as informações passados no form
       
       if not user:           
        messages.add_message(request, constants.ERROR, 'Usuario ou Senha invalidos!') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
        return redirect(reverse('logar'))
    
       else: #se o usuario/senha for verdadeiro me redicionara para uma url
           auth.login(request, user)
           return redirect(reverse('home'))
       
def sair(request): #função responsavel pelo logout do site 
    auth.logout(request)
    return redirect(reverse('logar'))    


   



