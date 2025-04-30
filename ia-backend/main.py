from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import requests
import re

app = FastAPI()

# Definir seu CLIENT_ID e CLIENT_SECRET da Twitch
CLIENT_ID = 'wr73kqw6rhwwsipxw5jlch8wk6kufi'
CLIENT_SECRET = 'kxexed9anrwbz2tj5p942i4lrdmklj'

# Função para obter o Access Token da Twitch
def obter_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=payload)
    data = response.json()
    return data['access_token']

# Função para verificar se o canal está ao vivo
def verificar_canal_ao_vivo(canal: str):
    access_token = obter_access_token()
    url = f'https://api.twitch.tv/helix/streams?user_login={canal}'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if data['data']:
        return True  # Canal está ao vivo
    return False  # Canal não está ao vivo

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Perguntas e respostas
PERGUNTAS_E_RESPOSTAS = {
    "Quando é o próximo jogo da FURIA?": "O próximo jogo da FURIA é dia 27 de abril, às 19h, contra o Flamengo. O jogo será no estádio do Pacaembu, em São Paulo.",
    "Que horas é o jogo da FURIA?": "O próximo jogo será às 19h, no dia 27 de abril, contra o Flamengo!",
    "Onde vai ser o próximo jogo da FURIA?": "O jogo será no estádio do Pacaembu, em São Paulo.",
    
    "Como faço para entrar na comunidade da FURIA no Telegram?": "Claro! Aqui está o link do grupo oficial: https://t.me/furia_community",
    "Tem grupo da FURIA no Telegram?": "Tem sim! Você pode participar clicando aqui: https://t.me/furia_community",
    
    "Olá": "Olá! Como posso ajudar você hoje?",
    "Oi": "Oi! Tudo bem? Me diga como posso te ajudar!",
    "Bom dia": "Bom dia! Como posso te ajudar hoje?",
    "Boa tarde": "Boa tarde! Em que posso ajudar você?",
    "Boa noite": "Boa noite! Precisa de alguma informação?",

    "Qual o site da FURIA?": "O site oficial da FURIA é: https://www.furia.gg",
    "Onde encontro mais informações sobre a FURIA?": "Você pode acessar nosso site oficial: https://www.furia.gg",
    
    "Quem é o dono da FURIA?": "A FURIA foi fundada por Jaime Pádua e André Akkari.",
    "Quem fundou a FURIA?": "Jaime Pádua e André Akkari são os fundadores da FURIA!",
    
    "Como faço para entrar no time da FURIA?": "Fique de olho no nosso site e nas redes sociais para saber sobre seletivas e oportunidades!",
    "Quero ser jogador da FURIA, como faço?": "Ótimo saber do seu interesse! Acompanhe as seletivas divulgadas no site e nas redes sociais oficiais da FURIA.",
    "A FURIA faz peneiras?": "Sim! Divulgamos informações sobre seletivas no site e nas nossas redes sociais. Fique atento!",
    
    "Quais são as redes sociais da FURIA?": "Você pode nos encontrar no Instagram, Twitter, Facebook, TikTok e YouTube! Busque por @FURIA ou acesse via nosso site.",
    "Onde posso seguir a FURIA?": "Estamos presentes no Instagram, Twitter, Facebook, TikTok e YouTube! É só buscar por @FURIA.",
    
    "Quais são os times da FURIA?": "A FURIA tem equipes em diversas modalidades como CS:GO, League of Legends, Valorant, entre outras!",
    "A FURIA tem time de LoL?": "Sim! A FURIA tem uma equipe que disputa o CBLOL, o principal campeonato de League of Legends do Brasil.",
    "A FURIA tem time de CS?": "Sim! A FURIA é muito conhecida pela sua equipe de Counter-Strike: Global Offensive (CS:GO)!",

    "Vocês vendem produtos oficiais?": "Vendemos sim! Você pode conferir nossos produtos na loja oficial: https://www.furia.gg/store",
    "Onde posso comprar produtos da FURIA?": "Confira nossa loja online aqui: https://www.furia.gg/store",

    "Como faço para trabalhar na FURIA?": "Ficamos felizes com seu interesse! As oportunidades são divulgadas no nosso site e no LinkedIn da FURIA. Fique de olho!",
    
    "Onde posso assistir os jogos da FURIA?": "Você pode assistir os jogos pelo canal oficial da FURIA na Twitch ou nas transmissões oficiais dos campeonatos.",
    "A FURIA transmite os jogos?": "Sim! Acompanhe nossos jogos ao vivo pelo canal da FURIA na Twitch ou nas transmissões oficiais dos campeonatos.",

    "Quantos títulos a FURIA tem?": "A FURIA conquistou vários títulos em diferentes modalidades! Quer saber sobre algum esporte específico?",
    "A FURIA já foi campeã?": "Sim, a FURIA já conquistou diversos títulos nacionais e internacionais em várias modalidades!",

    "Quem são os jogadores da FURIA?": "O elenco pode mudar ao longo do tempo! Quer saber de qual modalidade especificamente para eu te informar melhor?",

    "Obrigado": "Eu que agradeço! Qualquer outra dúvida, é só chamar!",
    "Valeu": "Valeu! Sempre que precisar, estarei por aqui!",
    "Tchau": "Até mais! Foi ótimo falar com você!",
}


# Carregar o modelo de embeddings
modelo = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Carregar o modelo transformer para gerar respostas (usando T5, por exemplo)
modelo_transformer = pipeline("text-generation", model="t5-small", tokenizer="t5-small")

# Gerar embeddings para as perguntas programadas
perguntas = list(PERGUNTAS_E_RESPOSTAS.keys())
embeddings_perguntas = modelo.encode(perguntas)

class Mensagem(BaseModel):
    texto: str

@app.post("/perguntar/")
async def responder_pergunta(mensagem: Mensagem):
    pergunta = mensagem.texto.strip().lower()

    # Usar o modelo de embeddings para calcular a similaridade da pergunta
    embedding_usuario = modelo.encode([pergunta])
    similaridades = cosine_similarity(embedding_usuario, embeddings_perguntas)
    indice_pergunta_mais_similar = similaridades.argmax()
    pergunta_mais_similar = perguntas[indice_pergunta_mais_similar]

    # Verificar se a pergunta é sobre "canal ao vivo"
    if re.search(r"(canal|stream|ao vivo)", pergunta):
        canal = 'furiatv'
        if canal:
            canal = canal.group(1)  # O nome do canal
            ao_vivo = verificar_canal_ao_vivo(canal)

            if ao_vivo:
                resposta = f"O canal {canal} está ao vivo agora!"
            else:
                resposta = f"O canal {canal} não está ao vivo no momento."
        else:
            resposta = "Desculpe, não consegui identificar o nome do canal na sua pergunta."
    else:
        # Se a similaridade for muito baixa, gerar uma resposta usando o modelo transformer
        if similaridades[0][indice_pergunta_mais_similar] < 0.5:
            resposta_transformer = modelo_transformer(f"Gerar uma resposta para: {pergunta}", max_length=50)
            resposta = resposta_transformer[0]['generated_text']
        else:
            resposta = PERGUNTAS_E_RESPOSTAS[pergunta_mais_similar]

    return {"resposta": resposta}
