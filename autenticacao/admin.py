from django.contrib import admin
from django.contrib.auth import admin as auth_admin


from autenticacao.models import Users

@admin.register(Users)
class UsersAdmin(auth_admin.UserAdmin):
    fieldsets = auth_admin.UserAdmin.fieldsets + (("Tipo Usuario", {"fields": ("tipo_user",) } ),)