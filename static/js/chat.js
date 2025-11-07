/**
 * Chat client for DOF Chat demo
 */
class ChatClient {
    constructor() {
        this.chatWindow = document.getElementById('chat-window');
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSubmit();
            }
        });
    }

    async handleSubmit() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        this.setInputEnabled(false);
        this.chatInput.value = '';
        this.addMessage(message, 'user');
        
        const loadingId = this.addMessage('Procesando tu consulta...', 'loading');

        try {
            const response = await this.sendChatRequest(message);
            this.removeMessage(loadingId);
            this.addBotResponse(response);
        } catch (error) {
            console.error('Chat error:', error);
            this.removeMessage(loadingId);
            this.addMessage('Lo siento, hubo un error al procesar tu consulta. Por favor, inténtalo de nuevo.', 'bot error-message');
        } finally {
            this.setInputEnabled(true);
            this.chatInput.focus();
        }
    }

    async sendChatRequest(message) {
        const response = await fetch('/api/v1/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: message })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }

        return response.json();
    }

    addMessage(content, type) {
        const messageId = 'msg-' + Date.now();
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.id = messageId;
        messageElement.textContent = content;

        this.chatWindow.appendChild(messageElement);
        this.scrollToBottom();
        return messageId;
    }

    addBotResponse(response) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot';
        
        // Add main answer
        const answerElement = document.createElement('div');
        answerElement.textContent = response.answer;
        messageElement.appendChild(answerElement);

        // Add context HTML or fallback to simple sources
        if (response.context_html?.trim() && this.isValidAccordionHTML(response.context_html)) {
            const contextElement = document.createElement('div');
            contextElement.className = 'context-container';
            contextElement.innerHTML = response.context_html;
            messageElement.appendChild(contextElement);
        } else if (response.sources?.length > 0) {
            this.addSimpleSources(messageElement, response.sources);
        }

        this.chatWindow.appendChild(messageElement);
        this.scrollToBottom();
    }

    addSimpleSources(messageElement, sources) {
        const sourcesElement = document.createElement('div');
        sourcesElement.className = 'sources';
        sourcesElement.innerHTML = `<strong>Fuentes:</strong><br>${sources.map(this.escapeHtml).join('<br>')}`;
        messageElement.appendChild(sourcesElement);
    }

    isValidAccordionHTML(html) {
        return html.includes('embedded-sources-container') && 
               html.includes('<details') && 
               html.includes('<summary');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    removeMessage(messageId) {
        document.getElementById(messageId)?.remove();
    }

    setInputEnabled(enabled) {
        this.chatInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        this.sendButton.textContent = enabled ? 'Enviar' : 'Enviando...';
    }

    scrollToBottom() {
        this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => new ChatClient());