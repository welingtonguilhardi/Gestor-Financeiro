from django.db import models
from django.contrib.auth.models import AbstractUser


class Users (AbstractUser):
    
    '''
        username será usado para identificar CPF / CNPJ
    '''
    
    CHOICES_TIPO_USER = [
        ('e', 'empresa'),
        ('f','funcionario')
    ]
    
    tipo_user = models.CharField(max_length=1,choices=CHOICES_TIPO_USER)
    

    
    
    
    

    
