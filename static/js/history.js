/**
 * History Panel / Sidebar functionality for DOF Chat
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
                // Early return: skip if clicking on menu trigger or dropdown
                if (e.target.closest('[data-menu-trigger]')) return;
                if (e.target.closest('[data-dropdown="true"]')) return;

                const item = e.target.closest('[data-conversation-id]');
                if (item) {
                    this.handleConversationClick(item);
                }
            });
        }

        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('[data-dropdown-container]')) {
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
        // Event delegation for dropdown triggers - using data-menu-trigger
        document.addEventListener('click', (e) => {
            const trigger = e.target.closest('[data-menu-trigger]');
            if (!trigger) return;

            e.stopPropagation();
            const container = trigger.closest('[data-dropdown-container]');
            const dropdown = container?.querySelector('[data-dropdown="true"]');

            if (dropdown) {
                // Close other dropdowns first
                this.closeAllDropdowns();
                dropdown.classList.toggle('hidden');
            }
        });

        // Handle dropdown menu item clicks
        document.addEventListener('click', (e) => {
            const menuItem = e.target.closest('[data-dropdown="true"] button');
            if (!menuItem) return;

            e.stopPropagation();
            const container = menuItem.closest('[data-dropdown-container]');
            const item = container?.closest('[data-conversation-id]');
            const conversationId = item?.dataset.conversationId;

            // Detect action by data-action attribute
            const action = menuItem.dataset.action;

            switch (action) {
                case 'delete':
                    this.handleDeleteConversation(conversationId, item);
                    break;
                case 'rename':
                    this.handleRenameConversation(conversationId, item);
                    break;
                case 'share':
                    this.handleShareConversation(conversationId);
                    break;
            }

            this.closeAllDropdowns();
        });
    }

    toggleSidebar(forceExpand = false) {
        if (!this.elements.sidebar) return;

        const isCurrentlyExpanded = this.elements.sidebar.getAttribute('data-state') === 'expanded';

        if (forceExpand || !isCurrentlyExpanded) {
            this.elements.sidebar.setAttribute('data-state', 'expanded');
        } else {
            this.elements.sidebar.setAttribute('data-state', 'collapsed');
        }

        // Show/hide overlay on mobile
        if (this.isMobile() && this.elements.overlay) {
            this.elements.overlay.classList.toggle('visible', !this.isSidebarExpanded());
        }
    }



    closeSidebar() {
        if (!this.elements.sidebar) return;
        this.elements.sidebar.setAttribute('data-state', 'collapsed');

        if (this.elements.overlay) {
            this.elements.overlay.classList.remove('visible');
        }
    }

    isSidebarExpanded() {
        return this.elements.sidebar?.getAttribute('data-state') === 'expanded';
    }

    isMobile() {
        return window.innerWidth <= 768;
    }

    closeAllDropdowns() {
        document.querySelectorAll('[data-dropdown="true"]').forEach(dropdown => {
            dropdown.classList.add('hidden');
        });
    }

    handleNewConversation() {
        // TODO: Reset chat state and navigate to new session ID
        console.log('New conversation requested');

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
        const items = this.elements.historyList?.querySelectorAll('[data-conversation-id]');
        const groups = this.elements.historyList?.querySelectorAll('[data-conversation-group]');

        items?.forEach(item => {
            // Use semantic selector for title
            const titleEl = item.querySelector('[data-conversation-title]');
            const title = titleEl?.textContent.toLowerCase() || '';
            const matches = title.includes(normalizedQuery);
            item.style.display = matches ? '' : 'none';
        });

        // Hide empty groups
        groups?.forEach(group => {
            const visibleItems = group.querySelectorAll('[data-conversation-id]:not([style*="display: none"])');
            group.style.display = visibleItems.length > 0 ? '' : 'none';
        });
    }

    handleConversationClick(item) {
        const conversationId = item.dataset.conversationId;
        console.log('Selected conversation:', conversationId);

        // Update active state using data attribute (single source of truth)
        this.elements.historyList?.querySelectorAll('[data-conversation-id]').forEach(i => {
            i.dataset.active = 'false';
        });

        // Set selected as active
        item.dataset.active = 'true';

        // TODO: Fetch and load conversation history from API
        const titleEl = item.querySelector('[data-conversation-title]');
        const title = titleEl?.textContent;
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
            item.style.transition = `all 200ms ease`;
            item.style.opacity = '0';
            item.style.transform = 'translateX(-10px)';

            setTimeout(() => {
                item.remove();
            }, 200);
        }
    }

    handleRenameConversation(conversationId, item) {
        console.log('Rename conversation:', conversationId);

        const titleEl = item?.querySelector('[data-conversation-title]');
        if (!titleEl) return;

        const currentTitle = titleEl.textContent;
        const newTitle = prompt('Nuevo nombre:', currentTitle);

        if (newTitle && newTitle.trim() !== currentTitle) {
            titleEl.textContent = newTitle.trim();
        }
    }

    handleShareConversation(conversationId) {
        console.log('Share conversation:', conversationId);
        // TODO: Implement share dialog modal
        alert('Funcionalidad de compartir próximamente disponible');
    }

    handleSettings() {
        console.log('Settings requested');
        // TODO: Connect to global settings panel
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
