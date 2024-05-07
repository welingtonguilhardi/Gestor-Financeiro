from audioop import reverse
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required( login_url = 'logar' )
def home (request):
    return HttpResponse('Pagina home')
