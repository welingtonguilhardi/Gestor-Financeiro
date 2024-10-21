@echo off
REM Nome do arquivo: run_django_project.bat

REM Verifica se o ambiente virtual está configurado
IF NOT EXIST "venv\Scripts\activate" (
    echo Ambiente virtual não encontrado. Por favor, configure o ambiente primeiro.
    pause
    exit /b
)

REM Ativa o ambiente virtual
echo Ativando o ambiente virtual...
call venv\Scripts\activate

REM Verifica se o arquivo manage.py existe na pasta atual
IF NOT EXIST "manage.py" (
    echo Arquivo manage.py não encontrado. Certifique-se de que este script esteja na raiz do projeto Django.
    pause
    exit /b
)

REM Inicia o servidor do Django
echo Iniciando o servidor do Django...
python manage.py runserver

REM Mantém a janela aberta após parar o servidor
pause
