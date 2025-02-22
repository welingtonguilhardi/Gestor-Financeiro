# Generated by Django 5.0.6 on 2024-05-09 03:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rembolso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.CharField(max_length=150)),
                ('motivo', models.CharField(max_length=150)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('foto_comprovante', models.ImageField(null=True, upload_to='documentos/')),
                ('data_comprovante', models.DateTimeField()),
                ('pago', models.BooleanField(default=False)),
                ('data_modificacao', models.DateTimeField(auto_now=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('user_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresa_rembolso', to=settings.AUTH_USER_MODEL)),
                ('user_funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funcionario_rembolso', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
