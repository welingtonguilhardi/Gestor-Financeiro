# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from empresa.models import Cargo

class VerificarUserTipoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if not request.user.is_authenticated:
            return self.get_response(request)
        

        
        tipo_user = request.user.tipo_user



        # Se usuario é do tipo empresa
        if tipo_user == 'e':

            cargos = Cargo.objects.filter(user_empresa = request.user)
            
            # Verificando se usuario está na pagina de cadastro de cargos
            if request.path == reverse('cadastrar_cargo'):
                return self.get_response(request)
            
            #Verificando se empresa tem pelo menos 1 cargo criado
            elif len(cargos) < 1:
                return redirect(reverse('cadastrar_cargo'))            
            
        return self.get_response(request)
