// Configurações dos provedores de autenticação
const config = {
    google: {
        clientId: 'SEU_CLIENT_ID_GOOGLE',
        redirectUri: 'http://localhost:5000/auth/google/callback'
    },
    facebook: {
        appId: 'SEU_APP_ID_FACEBOOK',
        redirectUri: 'http://localhost:5000/auth/facebook/callback'
    },
    twitter: {
        clientId: 'SEU_CLIENT_ID_TWITTER',
        redirectUri: 'http://localhost:5000/auth/twitter/callback'
    }
};

// Função para autenticação com Google
function loginWithGoogle() {
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${config.google.clientId}&redirect_uri=${config.google.redirectUri}&response_type=code&scope=email profile&access_type=offline&prompt=consent`;
    window.location.href = authUrl;
}

// Função para autenticação com Facebook
function loginWithFacebook() {
    const authUrl = `https://www.facebook.com/v12.0/dialog/oauth?client_id=${config.facebook.appId}&redirect_uri=${config.facebook.redirectUri}&scope=email,public_profile`;
    window.location.href = authUrl;
}

// Função para autenticação com Twitter
function loginWithTwitter() {
    const authUrl = `https://twitter.com/i/oauth2/authorize?response_type=code&client_id=${config.twitter.clientId}&redirect_uri=${config.twitter.redirectUri}&scope=tweet.read users.read&state=state&code_challenge=challenge&code_challenge_method=plain`;
    window.location.href = authUrl;
}

// Função para processar o callback de autenticação
async function handleAuthCallback(provider, code) {
    try {
        const response = await fetch(`/auth/${provider}/callback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });

        if (response.ok) {
            const data = await response.json();
            // Armazenar o token de acesso
            localStorage.setItem('authToken', data.access_token);
            localStorage.setItem('userData', JSON.stringify(data.user));
            
            // Redirecionar para a página principal
            window.location.href = '/feed.html';
        } else {
            throw new Error('Falha na autenticação');
        }
    } catch (error) {
        console.error('Erro na autenticação:', error);
        alert('Erro ao fazer login. Por favor, tente novamente.');
    }
}

// Verificar se estamos na página de callback
if (window.location.pathname.includes('/auth/')) {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const provider = window.location.pathname.split('/')[2];
    
    if (code) {
        handleAuthCallback(provider, code);
    }
}

// Função para verificar se o usuário está autenticado
function isAuthenticated() {
    return !!localStorage.getItem('authToken');
}

// Função para fazer logout
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    window.location.href = '/index.html';
} 