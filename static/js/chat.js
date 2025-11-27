/**
 * Chat client for DOF Chat demo
 */
class ChatClient {
    // Security and UI constants
    static DANGEROUS_ATTRIBUTES = ['onclick', 'onload', 'onerror', 'onmouseover', 'onfocus', 'onblur', 'onchange'];
    static DANGEROUS_PATTERNS = [
        /<script/i,
        /javascript:/i,
        /on\w+\s*=/i,
        /<iframe/i,
        /<object/i,
        /<embed/i
    ];
    static REQUIRED_ACCORDION_ELEMENTS = ['embedded-sources-container', '<details', '<summary'];
    static MESSAGES = {
        LOADING: 'Procesando tu consulta...',
        ERROR: 'Lo siento, hubo un error al procesar tu consulta. Por favor, inténtalo de nuevo.',
        SENDING: 'Enviando...',
        SEND: 'Enviar'
    };

    constructor() {
        // Cache DOM elements
        this.elements = {
            chatWindow: document.getElementById('chat-window'),
            chatForm: document.getElementById('chat-form'),
            chatInput: document.getElementById('chat-input'),
            sendButton: document.getElementById('send-button')
        };
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.elements.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        this.elements.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSubmit();
            }
        });
    }

    async handleSubmit() {
        const message = this.elements.chatInput.value.trim();
        if (!message) return;

        this.setInputEnabled(false);
        this.elements.chatInput.value = '';
        this.addMessage(message, 'user');
        
        const loadingId = this.addMessage(ChatClient.MESSAGES.LOADING, 'loading');

        try {
            const response = await this.sendChatRequest(message);
            this.removeMessage(loadingId);
            this.addBotResponse(response);
        } catch (error) {
            console.error('Chat error:', error);
            this.removeMessage(loadingId);
            this.addMessage(ChatClient.MESSAGES.ERROR, 'bot error-message');
        } finally {
            this.setInputEnabled(true);
            this.elements.chatInput.focus();
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
        const messageId = 'msg-' + (window.crypto && crypto.randomUUID ? crypto.randomUUID() : (Date.now().toString(36) + Math.random().toString(36).substr(2, 9)));
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.id = messageId;
        messageElement.textContent = content;

        this.elements.chatWindow.appendChild(messageElement);
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

        // Add context HTML with enhanced security validation
        if (response.context_html?.trim() && this.isValidAndSafeAccordionHTML(response.context_html)) {
            const contextElement = document.createElement('div');
            contextElement.className = 'context-container';
            // Use a more secure way to set HTML content
            this.setSafeHTML(contextElement, response.context_html);
            messageElement.appendChild(contextElement);
        } else if (response.sources?.length > 0) {
            this.addSimpleSources(messageElement, response.sources);
        }

        this.elements.chatWindow.appendChild(messageElement);
        this.scrollToBottom();
    }

    addSimpleSources(messageElement, sources) {
        const sourcesElement = document.createElement('div');
        sourcesElement.className = 'sources';
        sourcesElement.innerHTML = `<strong>Fuentes:</strong><br>${sources.map(this.escapeHtml).join('<br>')}`;
        messageElement.appendChild(sourcesElement);
    }

    isValidAndSafeAccordionHTML(html) {
        if (!html || typeof html !== 'string') return false;
        
        // Check for required accordion structure
        const hasRequiredStructure = ChatClient.REQUIRED_ACCORDION_ELEMENTS
            .every(element => html.includes(element));
        
        // Check for potentially dangerous content
        const hasDangerousContent = ChatClient.DANGEROUS_PATTERNS
            .some(pattern => pattern.test(html));
        
        return hasRequiredStructure && !hasDangerousContent;
    }

    setSafeHTML(element, html) {
        // Create a temporary element to parse and validate the HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        
        // Remove any potentially dangerous attributes
        this.sanitizeElement(tempDiv);
        
        // Set the cleaned content
        element.innerHTML = tempDiv.innerHTML;
    }

    sanitizeElement(element) {
        // Recursively sanitize all elements
        const walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_ELEMENT,
            null,
            false
        );
        
        let node;
        while (node = walker.nextNode()) {
            // Remove dangerous attributes
            ChatClient.DANGEROUS_ATTRIBUTES.forEach(attr => {
                if (node.hasAttribute(attr)) {
                    node.removeAttribute(attr);
                }
            });
            
            // Validate href attributes
            this.sanitizeHrefAttribute(node);
        }
    }

    sanitizeHrefAttribute(node) {
        if (!node.hasAttribute('href')) return;
        
        const href = node.getAttribute('href');
        if (!href) return;
        
        try {
            // Allow relative URLs, http, https protocols, and anchors
            if (href.startsWith('/') || href.startsWith('#')) return;
            
            const url = new URL(href, window.location.origin);
            if (!['http:', 'https:'].includes(url.protocol)) {
                node.removeAttribute('href');
            }
        } catch {
            // If URL parsing fails, remove the attribute for safety
            node.removeAttribute('href');
        }
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
        this.elements.chatInput.disabled = !enabled;
        this.elements.sendButton.disabled = !enabled;
        this.elements.sendButton.textContent = enabled ? ChatClient.MESSAGES.SEND : ChatClient.MESSAGES.SENDING;
    }

    scrollToBottom() {
        this.elements.chatWindow.scrollTop = this.elements.chatWindow.scrollHeight;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => new ChatClient());