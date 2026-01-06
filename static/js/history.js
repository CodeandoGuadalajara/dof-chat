/**
 * History Panel / Sidebar functionality for DOF Chat
 * ChatGPT-style sidebar interactions
 */
class HistoryPanel {
    constructor() {
        // Cache DOM elements
        this.elements = {
            sidebar: document.getElementById('history-sidebar'),
            sidebarToggle: document.getElementById('sidebar-toggle'),
            mobileToggle: document.getElementById('mobile-sidebar-toggle'),
            overlay: document.getElementById('sidebar-overlay'),
            newChatBtn: document.getElementById('new-chat-btn'),
            searchInput: document.getElementById('history-search'),
            historyList: document.getElementById('history-list'),
            settingsBtn: document.getElementById('settings-btn')
        };

        this.initializeEventListeners();
        this.initializeDropdownMenus();
    }

    initializeEventListeners() {
        // Main sidebar toggle
        if (this.elements.sidebarToggle) {
            this.elements.sidebarToggle.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Mobile toggle button
        if (this.elements.mobileToggle) {
            this.elements.mobileToggle.addEventListener('click', () => {
                this.toggleSidebar(true);
            });
        }

        // Overlay click to close sidebar on mobile
        if (this.elements.overlay) {
            this.elements.overlay.addEventListener('click', () => {
                this.closeSidebar();
            });
        }

        // New conversation button
        if (this.elements.newChatBtn) {
            this.elements.newChatBtn.addEventListener('click', () => {
                this.handleNewConversation();
            });
        }

        // Search input
        if (this.elements.searchInput) {
            this.elements.searchInput.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });
        }

        // Settings button
        if (this.elements.settingsBtn) {
            this.elements.settingsBtn.addEventListener('click', () => {
                this.handleSettings();
            });
        }

        // Conversation item clicks (using event delegation)
        if (this.elements.historyList) {
            this.elements.historyList.addEventListener('click', (e) => {
                const item = e.target.closest('.history-item');
                if (item && !e.target.closest('.history-menu-trigger') && !e.target.closest('.history-dropdown-menu')) {
                    this.handleConversationClick(item);
                }
            });
        }

        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.history-item-actions-container')) {
                this.closeAllDropdowns();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Escape to close sidebar on mobile
            if (e.key === 'Escape' && this.isMobile() && this.isSidebarExpanded()) {
                this.closeSidebar();
            }
        });
    }

    initializeDropdownMenus() {
        // Event delegation for dropdown triggers
        document.addEventListener('click', (e) => {
            const trigger = e.target.closest('.history-menu-trigger');
            if (!trigger) return;

            e.stopPropagation();
            const container = trigger.closest('.history-item-actions-container');
            const dropdown = container?.querySelector('.history-dropdown-menu');

            if (dropdown) {
                // Close other dropdowns first
                this.closeAllDropdowns();
                dropdown.classList.toggle('hidden');
            }
        });

        // Handle dropdown menu item clicks
        document.addEventListener('click', (e) => {
            const menuItem = e.target.closest('.history-menu-item');
            if (!menuItem) return;

            e.stopPropagation();
            const container = menuItem.closest('.history-item-actions-container');
            const item = container?.closest('.history-item');
            const conversationId = item?.dataset.conversationId;

            if (menuItem.classList.contains('delete')) {
                this.handleDeleteConversation(conversationId, item);
            } else if (menuItem.querySelector('.menu-item-icon svg path[d*="M17 3"]')) {
                // Edit/Rename based on SVG path
                this.handleRenameConversation(conversationId, item);
            } else {
                this.handleShareConversation(conversationId);
            }

            this.closeAllDropdowns();
        });
    }

    toggleSidebar(forceExpand = false) {
        if (!this.elements.sidebar) return;

        if (forceExpand) {
            this.elements.sidebar.classList.add('expanded');
        } else {
            this.elements.sidebar.classList.toggle('expanded');
        }

        // Show/hide overlay on mobile
        if (this.isMobile() && this.elements.overlay) {
            this.elements.overlay.classList.toggle('visible', this.isSidebarExpanded());
        }
    }

    closeSidebar() {
        if (!this.elements.sidebar) return;
        this.elements.sidebar.classList.remove('expanded');
        
        if (this.elements.overlay) {
            this.elements.overlay.classList.remove('visible');
        }
    }

    isSidebarExpanded() {
        return this.elements.sidebar?.classList.contains('expanded') ?? false;
    }

    isMobile() {
        return window.innerWidth <= 768;
    }

    closeAllDropdowns() {
        document.querySelectorAll('.history-dropdown-menu').forEach(dropdown => {
            dropdown.classList.add('hidden');
        });
    }

    handleNewConversation() {
        // For demo purposes, just log the action
        console.log('New conversation requested');
        
        // In a real app, this would:
        // 1. Clear the current chat
        // 2. Reset the conversation state
        // 3. Optionally redirect to a new conversation page
        
        // Visual feedback
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            // Keep only the welcome message
            const messages = chatWindow.querySelectorAll('.message:not(.assistant):not(:first-child)');
            messages.forEach(msg => msg.remove());
        }
    }

    handleSearch(query) {
        const normalizedQuery = query.toLowerCase().trim();
        const items = this.elements.historyList?.querySelectorAll('.history-item');
        const groups = this.elements.historyList?.querySelectorAll('.history-group');

        items?.forEach(item => {
            const title = item.querySelector('.history-item-title')?.textContent.toLowerCase() || '';
            const preview = item.querySelector('.history-item-preview')?.textContent.toLowerCase() || '';
            const matches = title.includes(normalizedQuery) || preview.includes(normalizedQuery);
            item.style.display = matches ? '' : 'none';
        });

        // Hide empty groups
        groups?.forEach(group => {
            const visibleItems = group.querySelectorAll('.history-item:not([style*="display: none"])');
            group.style.display = visibleItems.length > 0 ? '' : 'none';
        });
    }

    handleConversationClick(item) {
        const conversationId = item.dataset.conversationId;
        console.log('Selected conversation:', conversationId);

        // Update active state
        this.elements.historyList?.querySelectorAll('.history-item').forEach(i => {
            i.classList.remove('active');
        });
        item.classList.add('active');

        // In a real app, this would load the conversation
        // For demo, just show a message
        const title = item.querySelector('.history-item-title')?.textContent;
        if (title) {
            console.log(`Loading conversation: ${title}`);
        }

        // Close sidebar on mobile after selection
        if (this.isMobile()) {
            this.closeSidebar();
        }
    }

    handleDeleteConversation(conversationId, item) {
        console.log('Delete conversation:', conversationId);
        
        // Animate removal
        if (item) {
            item.style.transition = 'all 0.2s ease';
            item.style.opacity = '0';
            item.style.transform = 'translateX(-10px)';
            
            setTimeout(() => {
                item.remove();
            }, 200);
        }
    }

    handleRenameConversation(conversationId, item) {
        console.log('Rename conversation:', conversationId);
        
        const titleEl = item?.querySelector('.history-item-title');
        if (!titleEl) return;

        const currentTitle = titleEl.textContent;
        const newTitle = prompt('Nuevo nombre:', currentTitle);
        
        if (newTitle && newTitle.trim() !== currentTitle) {
            titleEl.textContent = newTitle.trim();
        }
    }

    handleShareConversation(conversationId) {
        console.log('Share conversation:', conversationId);
        // In a real app, this would open a share dialog or copy a link
        alert('Funcionalidad de compartir próximamente disponible');
    }

    handleSettings() {
        console.log('Settings requested');
        // In a real app, this would open a settings modal or page
        alert('Configuración próximamente disponible');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize if sidebar elements exist
    if (document.getElementById('history-sidebar')) {
        new HistoryPanel();
    }
});
