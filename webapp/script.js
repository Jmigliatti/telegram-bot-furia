const chatBox = document.getElementById('chat-box');
const form = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

// Definir URL da IA
const IA_URL = 'http://localhost:8000/perguntar/'; // Correto para navegador!

function adicionarMensagem(texto, remetente) {
    const mensagem = document.createElement('div');
    mensagem.classList.add('message', remetente);
    mensagem.innerText = texto;
    chatBox.appendChild(mensagem);
    chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const texto = userInput.value.trim();
    if (!texto) return;

    adicionarMensagem(texto, 'user');
    userInput.value = '';

    try {
        const resposta = await fetch(IA_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texto })
        });
        const data = await resposta.json();
        adicionarMensagem(data.resposta, 'bot');
    } catch (error) {
        console.error('Erro ao buscar IA:', error);
        adicionarMensagem("Desculpe, não consegui responder agora.", 'bot');
    }
});
