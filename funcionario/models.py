from django.db import models

from autenticacao.models import Users

class Rembolso (models.Model):
    # Info
    local = models.CharField(max_length=150)
    motivo = models.CharField(max_length=150)
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # max_digits é o número total de dígitos permitidos, decimal_places é o número de dígitos permitidos após o ponto decimal
    foto_comprovante = models.ImageField(upload_to='documentos/',null=True)
    data_comprovante = models.DateTimeField()
    # Envolvidos
    user_empresa = models.ForeignKey(Users, on_delete= models.CASCADE, related_name='empresa_rembolso')
    user_funcionario = models.ForeignKey(Users, on_delete = models.CASCADE, related_name = 'funcionario_rembolso' )
    pago = models.BooleanField(default=False)
    # Controle sistema
    data_modificacao = models.DateTimeField(auto_now=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
