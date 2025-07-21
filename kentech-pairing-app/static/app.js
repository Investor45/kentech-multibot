// Kentech Bot Pairing - Frontend JavaScript
class BotPairingApp {
    constructor() {
        this.bots = [];
        this.pairs = [];
        this.selectedBots = [];
        this.websocket = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.connectWebSocket();
        this.loadData();
        this.render();
        
        // Auto-refresh data every 5 seconds
        setInterval(() => this.loadData(), 5000);
    }

    setupEventListeners() {
        // Create Pair button
        document.getElementById('createPairBtn').addEventListener('click', () => {
            this.createPair();
        });

        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refresh();
        });
    }

    async connectWebSocket() {
        try {
            this.websocket = new WebSocket('ws://localhost:8000/ws/monitoring');
            
            this.websocket.onopen = () => {
                console.log('Connected to monitoring WebSocket');
                this.updateStatus('Connected to real-time monitoring');
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };
            
            this.websocket.onclose = () => {
                console.log('WebSocket connection closed');
                this.updateStatus('Disconnected - attempting to reconnect...');
                // Attempt to reconnect after 3 seconds
                setTimeout(() => this.connectWebSocket(), 3000);
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateStatus('Connection error');
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            this.updateStatus('Failed to connect to real-time monitoring');
        }
    }

    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'bot_registered':
                this.loadData(); // Refresh bots list
                this.updateStatus(`New bot registered: ${data.bot_name}`);
                break;
            case 'pair_created':
                this.loadData(); // Refresh pairs list
                this.updateStatus(`New pair created`);
                break;
            case 'pair_terminated':
                this.loadData(); // Refresh pairs list
                this.updateStatus(`Pair terminated`);
                break;
            case 'bot_disconnected':
                this.loadData(); // Refresh bots list
                this.updateStatus(`Bot disconnected: ${data.bot_name}`);
                break;
        }
    }

    async loadData() {
        try {
            // Load bots
            const botsResponse = await fetch('/api/bots');
            if (botsResponse.ok) {
                this.bots = await botsResponse.json();
            }

            // Load pairs
            const pairsResponse = await fetch('/api/pairs');
            if (pairsResponse.ok) {
                this.pairs = await pairsResponse.json();
            }

            this.render();
        } catch (error) {
            console.error('Failed to load data:', error);
            this.updateStatus('Failed to load data from server');
        }
    }

    async createPair() {
        if (this.selectedBots.length !== 2) {
            this.updateStatus('Please select exactly 2 bots to create a pair');
            return;
        }

        try {
            const response = await fetch('/api/pairs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    primary_bot_id: this.selectedBots[0],
                    secondary_bot_id: this.selectedBots[1]
                })
            });

            if (response.ok) {
                const pair = await response.json();
                this.updateStatus(`Pair created successfully between ${this.getBotName(this.selectedBots[0])} and ${this.getBotName(this.selectedBots[1])}`);
                this.selectedBots = [];
                this.loadData(); // Refresh the display
            } else {
                const error = await response.text();
                this.updateStatus(`Failed to create pair: ${error}`);
            }
        } catch (error) {
            console.error('Failed to create pair:', error);
            this.updateStatus('Error creating pair');
        }
    }

    async terminatePair(pairId) {
        if (!confirm('Are you sure you want to terminate this pair?')) {
            return;
        }

        try {
            const response = await fetch(`/api/pairs/${pairId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.updateStatus('Pair terminated successfully');
                this.loadData(); // Refresh the display
            } else {
                const error = await response.text();
                this.updateStatus(`Failed to terminate pair: ${error}`);
            }
        } catch (error) {
            console.error('Failed to terminate pair:', error);
            this.updateStatus('Error terminating pair');
        }
    }

    getBotName(botId) {
        const bot = this.bots.find(b => b.id === botId);
        return bot ? bot.name : 'Unknown Bot';
    }

    refresh() {
        this.updateStatus('Refreshing data...');
        this.loadData();
    }

    updateStatus(message) {
        const statusElement = document.getElementById('statusMessage');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.style.opacity = '1';
            
            // Fade out after 3 seconds
            setTimeout(() => {
                statusElement.style.opacity = '0.7';
            }, 3000);
        }
        console.log('Status:', message);
    }

    selectBot(botId) {
        if (this.selectedBots.includes(botId)) {
            this.selectedBots = this.selectedBots.filter(id => id !== botId);
        } else if (this.selectedBots.length < 2) {
            this.selectedBots.push(botId);
        } else {
            this.updateStatus('You can only select 2 bots at a time');
            return;
        }
        this.render();
    }

    render() {
        this.renderBots();
        this.renderPairs();
        this.updateCreatePairButton();
    }

    renderBots() {
        const botsList = document.getElementById('botsList');
        if (!botsList) return;

        if (this.bots.length === 0) {
            botsList.innerHTML = '<div class="empty-state">No bots connected. Start some bots to see them here.</div>';
            return;
        }

        botsList.innerHTML = this.bots.map(bot => `
            <div class="bot-card ${this.selectedBots.includes(bot.id) ? 'selected' : ''}" 
                 onclick="app.selectBot('${bot.id}')">
                <div class="bot-header">
                    <h3>${bot.name}</h3>
                    <span class="bot-status ${bot.status || 'active'}">${bot.status || 'active'}</span>
                </div>
                <div class="bot-details">
                    <p><strong>Type:</strong> ${bot.bot_type}</p>
                    <p><strong>ID:</strong> ${bot.id}</p>
                    <p><strong>Capabilities:</strong> ${bot.capabilities || 'none specified'}</p>
                    <p><strong>Endpoint:</strong> ${bot.endpoint || 'N/A'}</p>
                    <p><strong>Last Seen:</strong> ${this.formatTime(bot.last_seen || bot.created_at)}</p>
                </div>
            </div>
        `).join('');
    }

    renderPairs() {
        const pairsList = document.getElementById('pairsList');
        if (!pairsList) return;

        if (this.pairs.length === 0) {
            pairsList.innerHTML = '<div class="empty-state">No active pairs. Create a pair by selecting 2 bots above.</div>';
            return;
        }

        pairsList.innerHTML = this.pairs.map(pair => {
            const primaryBot = this.bots.find(b => b.id === pair.primary_bot_id);
            const secondaryBot = this.bots.find(b => b.id === pair.secondary_bot_id);
            
            return `
                <div class="pair-card">
                    <div class="pair-header">
                        <h3>Pair: ${primaryBot?.name || 'Unknown'} ↔ ${secondaryBot?.name || 'Unknown'}</h3>
                        <button class="terminate-btn" onclick="app.terminatePair('${pair.id}')">Terminate</button>
                    </div>
                    <div class="pair-details">
                        <p><strong>Status:</strong> ${pair.status}</p>
                        <p><strong>Created:</strong> ${this.formatTime(pair.created_at)}</p>
                        <p><strong>Primary Bot:</strong> ${primaryBot?.name || 'Unknown'} (${primaryBot?.bot_type || 'unknown'})</p>
                        <p><strong>Secondary Bot:</strong> ${secondaryBot?.name || 'Unknown'} (${secondaryBot?.bot_type || 'unknown'})</p>
                    </div>
                </div>
            `;
        }).join('');
    }

    updateCreatePairButton() {
        const button = document.getElementById('createPairBtn');
        if (!button) return;

        button.disabled = this.selectedBots.length !== 2;
        button.textContent = this.selectedBots.length === 2 
            ? 'Create Pair' 
            : `Select ${2 - this.selectedBots.length} more bot${2 - this.selectedBots.length === 1 ? '' : 's'}`;
    }

    formatTime(dateString) {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} min ago`;
        if (diffMins < 1440) return `${Math.floor(diffMins / 60)} hr ago`;
        return date.toLocaleDateString();
    }
}

// Initialize the app when the page loads
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new BotPairingApp();
});
