// JavaScript principal para o projeto NEOLIBRES

document.addEventListener('DOMContentLoaded', function() {
    console.log('NEOLIBRES carregado com sucesso!');

    // Efeitos visuais para cards de livros
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // As propriedades transform e boxShadow serão controladas pelo CSS agora
            // Remover estilos inline aqui para evitar sobrescrever o CSS
        });

        card.addEventListener('mouseleave', function() {
            // As propriedades transform e boxShadow serão controladas pelo CSS agora
            // Remover estilos inline aqui para evitar sobrescrever o CSS
        });
    });

    // Animação para botões (removida do JS, controlada por CSS)
    const buttons = document.querySelectorAll('.button, .details-button, .back-button, .edit-button, .action-button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            // Removido: this.style.transform = 'scale(1.05)';
        });

        button.addEventListener('mouseleave', function() {
            // Removido: this.style.transform = 'scale(1)';
        });
    });

    // Confirmação para deletar livros
    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const bookTitle = this.getAttribute('data-book-title');
            if (!confirm(`Tem certeza que deseja deletar o livro "${bookTitle}"?`)) {
                event.preventDefault();
            }
        });
    });

    // Função para pré-visualização de imagem (no editor_livro.html e cadastrar.html)
    const coverImageUrlInput = document.getElementById('cover_image_url');
    const imagePreview = document.getElementById('image-preview');

    if (coverImageUrlInput && imagePreview) {
        coverImageUrlInput.addEventListener('input', function() {
            let imageUrl = this.value;
            // Verifica se é uma URL completa ou um nome de arquivo local
            if (imageUrl && !imageUrl.startsWith('http://') && !imageUrl.startsWith('https://') && !imageUrl.startsWith('/static/')) {
                imageUrl = `/static/img/${imageUrl}`;
            } else if (!imageUrl) {
                // Se o campo estiver vazio, usa a imagem de capa padrão
                imageUrl = '/static/img/default_book_cover.svg';
            }
            imagePreview.src = imageUrl;
            imagePreview.style.display = 'block'; // Garante que a pré-visualização seja exibida
        });
        // Dispara o evento 'input' na carga da página para mostrar a capa existente (no caso de edição)
        coverImageUrlInput.dispatchEvent(new Event('input'));
    }

    // Funcionalidade para fechar mensagens flash (se houver)
    const flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        flashMessages.addEventListener('click', function(event) {
            if (event.target.classList.contains('close-btn')) {
                event.target.closest('li').remove();
            }
        });
        // Adiciona um botão de fechar a cada mensagem flash
        flashMessages.querySelectorAll('li').forEach(messageLi => {
            const closeButton = document.createElement('button');
            closeButton.classList.add('close-btn');
            closeButton.innerHTML = '&times;'; // Caractere 'x'
            messageLi.appendChild(closeButton);
        });

        // Opcional: Remover mensagens flash automaticamente após alguns segundos
        setTimeout(() => {
            if (flashMessages) {
                flashMessages.querySelectorAll('li').forEach(messageLi => {
                    messageLi.style.opacity = '0';
                    messageLi.style.transition = 'opacity 0.5s ease-out';
                    setTimeout(() => messageLi.remove(), 500); // Remove após a transição
                });
            }
        }, 5000); // 5 segundos
    }
});