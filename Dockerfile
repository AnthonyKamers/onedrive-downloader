#FROM python:3.10-slim
#
## Instalações básicas
#RUN apt-get update && apt-get install -y \
#    wget unzip curl gnupg2 ca-certificates fonts-liberation \
#    libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 \
#    chromium chromium-driver
#
## Ambiente
#ENV DISPLAY=:99
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
## Dependências Python
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install --upgrade pip && pip install -r requirements.txt
#
## Código
#COPY . .
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM selenium/standalone-chrome:latest

USER root

# Instala dependências adicionais do Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Cria diretório da aplicação
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
