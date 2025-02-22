# Generated by Django 5.0.6 on 2024-05-10 01:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='status',
            field=models.CharField(choices=[('A', 'aceito'), ('N', 'negado'), ('D', 'desligado'), ('E', 'espera')], default='E', max_length=1),
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=150)),
                ('user_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresa_cargos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
