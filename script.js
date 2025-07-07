// particulas

// Quantidade total de particulas
const numParticles = 150;

// Tamanho mínimo e máximo das partículas
const minSize = 5;
const maxSize = 15;

// Função que cria as partículas na tela
function createParticles() {
    // Loop para criar partícula
    for (let i = 0; i < numParticles; i++) {
        // Cria uma div para as particulas
        const particle = document.createElement('div');
        
        // Define um tamanho aleatório entre minSize e maxSize
        const size = Math.random() * (maxSize - minSize) + minSize;
        
        // Configurações da partícula
        particle.className = 'particle'; // Classe no CSS
        particle.style.width = `${size}px`; 
        particle.style.height = `${size}px`; 
        particle.style.top = `${Math.random() * window.innerHeight}px`; // posição vertical
        particle.style.left = `${Math.random() * window.innerWidth}px`; // posição horizontal
        
        // Configuração da animação com valores aleatórios para tornar o movimento mais natural
        const duration = 10 + Math.random() * 20; // duração da animação
        const delay = Math.random() * 10; // Atraso inicial até 10 segundos
        particle.style.animation = `wave ${duration}s ease-in-out ${delay}s infinite`;
        
        // Adiciona particulas na página
        document.body.appendChild(particle);
    }
}

// carrega a página e os dados do cliente

document.addEventListener('DOMContentLoaded', () => {
    // função das particulas
    createParticles();

    const clientDataElement = document.getElementById('client-data');
    
    // mensagem de carregamento
    clientDataElement.innerHTML = '<p>Carregando dados...</p>';
    
    // solicita dados de clientes.json
    fetch('clientes.json')
        .then(response => response.json()) // Converte a resposta para JSON
        .then(data => {
            // Verifica se os dados são um array (pega o primeiro cliente) ou um objeto direto
            const client = Array.isArray(data) ? data[0] : data;
            
            // preenche o card do html
            clientDataElement.innerHTML = `
                <p><strong>ID:</strong> ${client.id}</p>
                <p><strong>Nome:</strong> ${client.nome}</p>
                <p><strong>Email:</strong> ${client.email}</p>
                <p><strong>Telefone:</strong> ${client.telefone}</p>
                <p><strong>Cidade:</strong> ${client.cidade}</p>
            `;
        })
        .catch(error => {
            // mostra mensagem em caso de erro
            console.error("Erro:", error);
            clientDataElement.innerHTML = '<p class="error">Erro ao carregar dados.</p>';
        });
});

// responsividade com as particulas

// evento ativado quando usuário redimenciona a janela
window.addEventListener('resize', () => {
    // reposiciona as particulas aleatoriamente
    document.querySelectorAll('.particle').forEach(particle => {
        particle.style.top = `${Math.random() * window.innerHeight}px`;
        particle.style.left = `${Math.random() * window.innerWidth}px`;
    });
});