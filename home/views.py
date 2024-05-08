from audioop import reverse
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required( login_url = 'logar' )
def home (request):
    
    if request.user.tipo_user == 'f':
        return HttpResponse('Pagina home funcionario')
    elif request.user.tipo_user == 'e':
        return HttpResponse('Pagina home empresas')
    else:
        return HttpResponse('Erro, entre em contato conosco')


