# template-fastapi
Template padrão para criar API com FastAPI

## 🔧 Criar o ambiente virtual (venv)
```
python3 -m venv venv
```
Obs: "python3" faz referência a versão do seu python, se estiver com o python 3.13 por exemplo, usará "python3.13" no comando

## 🔧 Ativar o ambiente virtual
```
source venv/bin/activate
```

## 🔧 Instalar dependências do projeto
```
pip install -r requirements.txt
```

## 🔧 Iniciar o projeto
```
uvicorn app.main:app --reload
```

## 🔧 Para sair do ambiente virtual
```
deactivate
```
