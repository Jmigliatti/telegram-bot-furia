from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Dicionário para armazenar usuários online
online_users = {}

# Configurações dos provedores
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
TWITTER_CLIENT_ID = os.getenv('TWITTER_CLIENT_ID')
TWITTER_CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET')

# Rota para atualizar status do usuário
@app.route('/api/update-status', methods=['POST'])
def update_status():
    try:
        data = request.json
        user_id = data.get('userId')
        user_name = data.get('userName')
        user_picture = data.get('userPicture')

        if not user_id or not user_name:
            return jsonify({'error': 'Dados do usuário incompletos'}), 400

        # Atualizar ou adicionar usuário
        online_users[user_id] = {
            'name': user_name,
            'picture': user_picture,
            'last_seen': datetime.now().isoformat()
        }

        # Remover usuários inativos (mais de 5 minutos)
        current_time = datetime.now()
        inactive_users = [
            user_id for user_id, user_data in online_users.items()
            if current_time - datetime.fromisoformat(user_data['last_seen']) > timedelta(minutes=5)
        ]
        for user_id in inactive_users:
            del online_users[user_id]

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para obter lista de usuários online
@app.route('/api/online-users', methods=['GET'])
def get_online_users():
    try:
        # Remover usuários inativos antes de retornar a lista
        current_time = datetime.now()
        inactive_users = [
            user_id for user_id, user_data in online_users.items()
            if current_time - datetime.fromisoformat(user_data['last_seen']) > timedelta(minutes=5)
        ]
        for user_id in inactive_users:
            del online_users[user_id]

        # Retornar lista de usuários ativos
        users_list = [
            {
                'id': user_id,
                'name': user_data['name'],
                'picture': user_data['picture']
            }
            for user_id, user_data in online_users.items()
        ]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rotas de callback para autenticação
@app.route('/auth/google/callback', methods=['GET', 'POST'])
def google_callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'Código não fornecido'}), 400

    # Trocar código por token de acesso
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'http://localhost:5000/auth/google/callback',
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        return jsonify({'error': 'Falha na autenticação'}), 400

    access_token = response.json()['access_token']
    
    # Obter informações do usuário
    user_info = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user_info['id'],
            'name': user_info['name'],
            'email': user_info['email'],
            'picture': user_info.get('picture')
        }
    })

@app.route('/auth/facebook/callback', methods=['GET', 'POST'])
def facebook_callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'Código não fornecido'}), 400

    # Trocar código por token de acesso
    token_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
    token_data = {
        'client_id': FACEBOOK_APP_ID,
        'client_secret': FACEBOOK_APP_SECRET,
        'redirect_uri': 'http://localhost:5000/auth/facebook/callback',
        'code': code
    }

    response = requests.get(token_url, params=token_data)
    if response.status_code != 200:
        return jsonify({'error': 'Falha na autenticação'}), 400

    access_token = response.json()['access_token']
    
    # Obter informações do usuário
    user_info = requests.get(
        'https://graph.facebook.com/me',
        params={
            'fields': 'id,name,email,picture',
            'access_token': access_token
        }
    ).json()

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user_info['id'],
            'name': user_info['name'],
            'email': user_info.get('email'),
            'picture': user_info.get('picture', {}).get('data', {}).get('url')
        }
    })

@app.route('/auth/twitter/callback', methods=['GET', 'POST'])
def twitter_callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'Código não fornecido'}), 400

    # Trocar código por token de acesso
    token_url = 'https://api.twitter.com/2/oauth2/token'
    token_data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': TWITTER_CLIENT_ID,
        'redirect_uri': 'http://localhost:5000/auth/twitter/callback',
        'code_verifier': 'challenge'
    }

    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        return jsonify({'error': 'Falha na autenticação'}), 400

    access_token = response.json()['access_token']
    
    # Obter informações do usuário
    user_info = requests.get(
        'https://api.twitter.com/2/users/me',
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user_info['data']['id'],
            'name': user_info['data']['name'],
            'username': user_info['data']['username']
        }
    })

# Rota para servir o feed.html
@app.route('/templates/feed.html')
def serve_feed():
    return send_from_directory('templates', 'feed.html')

if __name__ == '__main__':
    app.run(debug=True) 