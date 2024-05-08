from django.db import models

from autenticacao.models import Users

class Funcionario (models.Model):
    
    CHOICES_STATUS_FUNCINARIO = [
        ('A','aceito'),
        ('N','negado'),
        ('D','desligado')
    ]
    
    user_empresa = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='empresa')
    user_funcionario = models.OneToOneField(Users, on_delete=models.CASCADE,related_name='empregado')
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,choices=CHOICES_STATUS_FUNCINARIO)
    aceito = models.BooleanField(default=False)  
    
    