import requests
import time
import subprocess
import json

def get_ngrok_url():
    # Acessa a API do ngrok para pegar o link público
    response = requests.get("http://ngrok:4040/api/tunnels")  # ngrok é o nome do serviço
    if response.status_code == 200:
        tunnels = response.json().get("tunnels", [])
        if tunnels:
            public_url = tunnels[0]["public_url"]
            return public_url
    return None

def update_bot_code(ngrok_url):
    # Aqui você atualiza o código do bot (ou algum arquivo) com a URL do ngrok
    with open("/app/bot_config.json", "w") as config_file:
        json.dump({"ngrok_url": ngrok_url}, config_file)
import os
import requests

def get_ngrok_url():
    # A URL do ngrok será passada como variável de ambiente
    ngrok_url = os.getenv("NGROK_URL")
    if ngrok_url:
        # Usando a API do ngrok para pegar o URL gerado
        response = requests.get(f"{ngrok_url}/api/tunnels")
        if response.status_code == 200:
            tunnels = response.json()["tunnels"]
            # Pegando o primeiro túnel HTTP
            return tunnels[0]["public_url"]
    return None

