# 🐺 Chat da Torcida FURIA – Experiência Conversacional

Este projeto foi desenvolvido como parte do **Challenge #1: Experiência Conversacional** do processo seletivo da **FURIA Tech**.

🔗 Repositório oficial: [https://github.com/Jmigliatti/telegram-bot-furia](https://github.com/Jmigliatti/telegram-bot-furia)

## 🧠 Sobre o projeto

Criei um **protótipo web interativo** que simula a experiência de um fã acompanhando o time de **CS:GO da FURIA**, com foco na **interação, engajamento e usabilidade**.

O sistema é composto por:

- 💬 **Chat da torcida**: simula uma conversa entre fãs durante os jogos.
- 🗓 **Calendário de jogos**: acompanhe a agenda da FURIA.
- 📰 **Feed de acontecimentos**: últimas notícias, destaques de partidas e movimentações do time.
- 🤖 **Link direto para o Assistente Inteligente da FURIA no WhatsApp**: [Clique aqui](https://wa.me/5511993404466)

---

## 🧰 Requisitos

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

> ❗ O projeto roda com Docker e **exige acesso à internet para gerar o link público via ngrok**.

---

## 🐧 Como instalar o Docker

### Windows

1. Acesse: https://www.docker.com/products/docker-desktop/
2. Baixe o instalador e execute.
3. Siga as instruções e reinicie o computador, se necessário.
4. Verifique a instalação:
   ```powershell
   docker --version
   docker-compose --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

> Reinicie sua sessão para aplicar as permissões.

---

## 🚀 Como rodar o projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/Jmigliatti/telegram-bot-furia.git
   cd telegram-bot-furia
   ```

2. Inicie o ambiente com Docker:
   ```bash
   docker-compose up -d
   ```

3. Acesse no navegador:
   ```
   http://localhost:4040
   ```

   Esse endereço abrirá o painel do **ngrok**, onde você encontrará um link público como:
   ```
   https://xxxx-xx-xx-xx-xx.ngrok-free.app
   ```

4. Acesse esse link em qualquer navegador ou dispositivo conectado à internet para ver o protótipo em funcionamento.

---

## 📸 Preview

(Adicione aqui capturas de tela ou gifs do protótipo se desejar)

---

## 📹 Demonstração em vídeo

Veja como funciona a experiência do fã com o sistema:
👉 (Adicione aqui o link do vídeo demonstrativo)

---

## 🤝 Contribuições

Este projeto foi feito como desafio técnico individual, mas sugestões e feedbacks são sempre bem-vindos!

---

## 📄 Licença

Este repositório é de uso demonstrativo e segue a licença MIT.
