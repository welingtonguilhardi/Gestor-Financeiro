from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User #importa a class de usuario do django 
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
        username = request.POST.get('username')# obtém informaçao do campo input do cadastro conforme o name = 'username'
        senha = request.POST.get('password') # obtém informaçao do campo input do cadastro conforme o name = 'password'
        confirmar_senha = request.POST.get('confirm-password') # obtém informaçao do campo input do cadastro conforme o name = 'confirm-password'
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return redirect('/auth/cadastro/')
        
        if len(username.strip()) == 0 or len(senha.strip()) == 0:  #funçao strip é para o usuario não conseguir cadastrar uma senha só com espaço como exemplo senha = '    '           
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return redirect('/auth/cadastro/')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuario já existe') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return redirect('/auth/cadastro/')
        
        try:
            
            user = User.objects.create_user(username=username, password=senha)
            user.save()
            return redirect('/auth/logar')
        
        except:    
            messages.add_message(request, constants.ERROR, 'Erro no sistema') #mensagem de erro para mais informação acessar settings.py e procurar por mensagens de erros
            return redirect('/auth/cadastro/')


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
        return redirect('/auth/logar/')
    
       else: #se o usuario/senha for verdadeiro me redicionara para uma url
           auth.login(request, user)
           return redirect(reverse('home'))
       
def sair(request): #função responsavel pelo logout do site 
    auth.logout(request)
    return redirect('/auth/logar')    


   



