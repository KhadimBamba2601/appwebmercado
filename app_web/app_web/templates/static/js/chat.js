document.addEventListener('DOMContentLoaded', () => {
    const chatModal = document.getElementById('chatModal');
    const chatOverlay = document.getElementById('chatOverlay');
    const chatButton = document.querySelector('.chat-button');
    const chatBody = document.getElementById('chatBody');
    const chatForm = document.getElementById('chatForm');
    const chatMessageInput = document.getElementById('chatMessageInput');
    const chatSubmitButton = document.getElementById('chatSubmitButton');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function toggleChat() {
        chatModal.classList.toggle('show');
        chatOverlay.style.display = chatModal.classList.contains('show') ? 'block' : 'none';
        if (chatModal.classList.contains('show')) {
            chatBody.scrollTop = chatBody.scrollHeight;
        }
    }

    chatButton.addEventListener('click', toggleChat);
    chatOverlay.addEventListener('click', toggleChat);

    function appendMessage(sender, text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message');
        if (isUser) {
            messageDiv.classList.add('user-message');
            messageDiv.textContent = text;
        } else {
            messageDiv.classList.add('bot-message');
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
        }
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function sendMessage() {
        const message = chatMessageInput.value.trim();
        if (message) {
            appendMessage('Tú', message, true);
            chatMessageInput.value = '';
            chatSubmitButton.disabled = true;

            fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ 'mensaje': message })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                appendMessage('IA', data.response);
            })
            .catch(error => {
                console.error('Error al enviar el mensaje:', error);
                appendMessage('Error', error.message || 'No se pudo enviar el mensaje.');
            })
            .finally(() => {
                chatSubmitButton.disabled = false;
                chatMessageInput.focus();
            });
        }
    }

    chatSubmitButton.addEventListener('click', sendMessage);
    chatMessageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    // Auto-scroll al cargar la página
    chatBody.scrollTop = chatBody.scrollHeight;
});