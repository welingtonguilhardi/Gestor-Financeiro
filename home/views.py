
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required( login_url = 'logar' )
def home (request):
    
    if request.user.tipo_user == 'f':
        return HttpResponse('Pagina home funcionario')
    elif request.user.tipo_user == 'e':
        return redirect(reverse('home_empresa'))
    else:
        return HttpResponse('Erro, entre em contato conosco')


