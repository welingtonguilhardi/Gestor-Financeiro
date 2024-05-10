from django.db import models

from autenticacao.models import Users

class Cargo (models.Model):
    user_empresa = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='empresa_cargos')
    cargo = models.CharField(max_length=150)

class Funcionario (models.Model):
    
    CHOICES_STATUS_FUNCINARIO = [
        ('A','aceito'),
        ('N','negado'),
        ('D','desligado'),
        ('E','espera')
    ]
    
    user_empresa = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='empresa')
    user_funcionario = models.OneToOneField(Users, on_delete=models.CASCADE,related_name='empregado')
    cargo = models.ForeignKey(Cargo,on_delete = models.CASCADE, related_name = 'cargo_funcionario' )
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,choices=CHOICES_STATUS_FUNCINARIO, default='E')
    aceito = models.BooleanField(default=False)  
    


    