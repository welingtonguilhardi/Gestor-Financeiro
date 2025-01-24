@echo off
REM Nome do arquivo: setup_django.bat

REM Verifica se o Python está instalado
echo Verificando a instalação do Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python não encontrado. Baixando a versão mais recente...
    REM Baixa a versão mais recente do Python (ajuste o link conforme necessário)
    powershell -command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile python_installer.exe"
    
    REM Instala o Python silenciosamente
    echo Instalando Python...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    REM Verifica novamente se o Python foi instalado com sucesso
    python --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo Houve um problema na instalação do Python. Por favor, instale-o manualmente.
        pause
        exit /b
    ) ELSE (
        echo Python instalado com sucesso.
        del python_installer.exe
    )
)

REM Cria um ambiente virtual
echo Criando ambiente virtual...
python -m venv venv

REM Ativa o ambiente virtual
echo Ativando o ambiente virtual...
call venv\Scripts\activate

REM Atualiza o pip
echo Atualizando o pip...
python -m pip install --upgrade pip

REM Instala as dependências do Django
echo Instalando Django e outras dependências...
pip install django

REM Verifica se o arquivo requirements.txt existe e instala dependências adicionais
IF EXIST requirements.txt (
    echo Instalando dependências adicionais do requirements.txt...
    pip install -r requirements.txt
)

REM Realiza as migrações do banco de dados
echo Realizando as migrações do banco de dados...
python manage.py migrate

REM Cria um superusuario
echo from autenticacao.models import Users; from empresa.models import Cargo; superuser = Users.objects.create_superuser('admin', 'admin@example.com', 'admin', tipo_user='e',first_name='Empresa', last_name='Superusuário'); Cargo.objects.create(user_empresa=superuser, cargo='Dono') | python manage.py shell
echo Superusuário criado com sucesso!


REM Informa ao usuário que a configuração foi concluída
echo Instalação concluída com sucesso!
pause
