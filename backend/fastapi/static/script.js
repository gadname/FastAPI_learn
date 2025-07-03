// Kanban Board JavaScript
class KanbanBoard {
    constructor() {
        this.items = {
            bots: [],
            cats: []
        };
        this.columnStates = {
            todo: [],
            progress: [],
            done: []
        };
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadData();
    }

    bindEvents() {
        // Add item buttons
        document.getElementById('addBotBtn').addEventListener('click', () => this.showAddModal('bot'));
        document.getElementById('addCatBtn').addEventListener('click', () => this.showAddModal('cat'));
        document.getElementById('refreshBtn').addEventListener('click', () => this.loadData());

        // Modal events
        const modal = document.getElementById('addItemModal');
        const closeBtn = document.querySelector('.close');
        const cancelBtn = document.getElementById('cancelBtn');
        const form = document.getElementById('addItemForm');

        closeBtn.addEventListener('click', () => this.hideModal());
        cancelBtn.addEventListener('click', () => this.hideModal());
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.hideModal();
        });

        form.addEventListener('submit', (e) => this.handleFormSubmit(e));

        // Setup drag and drop
        this.setupDragAndDrop();
    }

    async loadData() {
        try {
            this.showLoading();
            
            // Fetch bots and cats from API
            const [botsResponse, catsResponse] = await Promise.all([
                fetch('/api/v1/bot/'),
                fetch('/api/v1/cat/')
            ]);

            if (botsResponse.ok) {
                const botsData = await botsResponse.json();
                this.items.bots = botsData.bots || [];
            }

            if (catsResponse.ok) {
                const catsData = await catsResponse.json();
                this.items.cats = catsData.cats || [];
            }

            this.initializeColumnStates();
            this.renderBoard();
            this.hideLoading();
        } catch (error) {
            console.error('Error loading data:', error);
            this.showMessage('データの読み込みに失敗しました', 'error');
            this.hideLoading();
        }
    }

    initializeColumnStates() {
        // Initialize column states with some sample distribution
        this.columnStates = {
            todo: [],
            progress: [],
            done: []
        };

        // Distribute items across columns (simulate kanban state)
        const allItems = [
            ...this.items.bots.map(bot => ({...bot, type: 'bot'})),
            ...this.items.cats.map(cat => ({...cat, type: 'cat'}))
        ];

        allItems.forEach((item, index) => {
            const column = index % 3 === 0 ? 'todo' : index % 3 === 1 ? 'progress' : 'done';
            this.columnStates[column].push(item);
        });
    }

    renderBoard() {
        // Clear all columns
        ['todo', 'progress', 'done'].forEach(status => {
            const column = document.getElementById(`${status}-column`);
            column.innerHTML = '';
        });

        // Render items in each column
        Object.keys(this.columnStates).forEach(status => {
            this.renderColumn(status);
        });

        this.updateItemCounts();
    }

    renderColumn(status) {
        const column = document.getElementById(`${status}-column`);
        const items = this.columnStates[status];

        if (items.length === 0) {
            column.innerHTML = '<div class="empty-state">アイテムがありません</div>';
            return;
        }

        items.forEach(item => {
            const card = this.createCard(item);
            column.appendChild(card);
        });
    }

    createCard(item) {
        const card = document.createElement('div');
        card.className = 'card';
        card.draggable = true;
        card.dataset.itemId = item.id;
        card.dataset.itemType = item.type;

        let cardContent = `
            <div class="card-header">
                <div class="card-title">${item.name}</div>
                <div class="card-type ${item.type}">${item.type === 'bot' ? 'ボット' : '猫'}</div>
            </div>
        `;

        if (item.type === 'bot') {
            cardContent += `
                <div class="card-details">
                    <div class="card-detail-item">
                        <div class="bot-color" style="background-color: #${item.color}"></div>
                    </div>
                </div>
            `;
        } else if (item.type === 'cat') {
            cardContent += `
                <div class="card-details">
                    ${item.breed ? `<div class="card-detail-item">品種: ${item.breed}</div>` : ''}
                    ${item.age ? `<div class="card-detail-item">年齢: ${item.age}歳</div>` : ''}
                    ${item.weight ? `<div class="card-detail-item">体重: ${item.weight}kg</div>` : ''}
                </div>
            `;
        }

        cardContent += `
            <div class="card-actions">
                <button class="btn btn-secondary" onclick="kanban.editItem('${item.id}', '${item.type}')">編集</button>
                <button class="btn btn-cancel" onclick="kanban.deleteItem('${item.id}', '${item.type}')">削除</button>
            </div>
        `;

        card.innerHTML = cardContent;
        return card;
    }

    setupDragAndDrop() {
        document.addEventListener('dragstart', (e) => {
            if (e.target.classList.contains('card')) {
                e.target.classList.add('dragging');
                e.dataTransfer.setData('text/plain', '');
            }
        });

        document.addEventListener('dragend', (e) => {
            if (e.target.classList.contains('card')) {
                e.target.classList.remove('dragging');
            }
        });

        ['todo', 'progress', 'done'].forEach(status => {
            const column = document.getElementById(`${status}-column`);
            
            column.addEventListener('dragover', (e) => {
                e.preventDefault();
                column.classList.add('drag-over');
            });

            column.addEventListener('dragleave', (e) => {
                if (!column.contains(e.relatedTarget)) {
                    column.classList.remove('drag-over');
                }
            });

            column.addEventListener('drop', (e) => {
                e.preventDefault();
                column.classList.remove('drag-over');
                
                const draggingCard = document.querySelector('.dragging');
                if (draggingCard) {
                    this.moveCard(draggingCard, status);
                }
            });
        });
    }

    moveCard(card, newStatus) {
        const itemId = card.dataset.itemId;
        const itemType = card.dataset.itemType;

        // Find item in current column states
        let item = null;
        let currentStatus = null;

        Object.keys(this.columnStates).forEach(status => {
            const foundIndex = this.columnStates[status].findIndex(i => i.id === itemId);
            if (foundIndex !== -1) {
                item = this.columnStates[status][foundIndex];
                currentStatus = status;
                this.columnStates[status].splice(foundIndex, 1);
            }
        });

        if (item && currentStatus !== newStatus) {
            this.columnStates[newStatus].push(item);
            this.renderBoard();
            this.showMessage(`${item.name}を${this.getStatusLabel(newStatus)}に移動しました`, 'success');
        }
    }

    getStatusLabel(status) {
        const labels = {
            todo: 'To Do',
            progress: 'In Progress',
            done: 'Done'
        };
        return labels[status] || status;
    }

    updateItemCounts() {
        Object.keys(this.columnStates).forEach(status => {
            const count = this.columnStates[status].length;
            const countElement = document.querySelector(`[data-status="${status}"] .item-count`);
            if (countElement) {
                countElement.textContent = count;
            }
        });
    }

    showAddModal(type) {
        const modal = document.getElementById('addItemModal');
        const modalTitle = document.getElementById('modalTitle');
        const botColorGroup = document.getElementById('botColorGroup');
        const catDetailsGroup = document.getElementById('catDetailsGroup');
        const form = document.getElementById('addItemForm');

        // Reset form
        form.reset();
        form.dataset.itemType = type;

        // Set modal title and show appropriate fields
        if (type === 'bot') {
            modalTitle.textContent = '新しいボットを追加';
            botColorGroup.style.display = 'block';
            catDetailsGroup.style.display = 'none';
        } else {
            modalTitle.textContent = '新しい猫を追加';
            botColorGroup.style.display = 'none';
            catDetailsGroup.style.display = 'block';
        }

        modal.style.display = 'block';
    }

    hideModal() {
        const modal = document.getElementById('addItemModal');
        modal.style.display = 'none';
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        const itemType = form.dataset.itemType;

        let data = {
            name: formData.get('name')
        };

        if (itemType === 'bot') {
            data.color = formData.get('color') || 'C5E24A';
        } else if (itemType === 'cat') {
            if (formData.get('breed')) data.breed = formData.get('breed');
            if (formData.get('age')) data.age = parseInt(formData.get('age'));
            if (formData.get('weight')) data.weight = parseFloat(formData.get('weight'));
        }

        try {
            const response = await fetch(`/api/v1/${itemType}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                this.hideModal();
                this.showMessage(`${itemType === 'bot' ? 'ボット' : '猫'}を追加しました`, 'success');
                this.loadData();
            } else {
                throw new Error('Failed to create item');
            }
        } catch (error) {
            console.error('Error creating item:', error);
            this.showMessage('アイテムの作成に失敗しました', 'error');
        }
    }

    async deleteItem(itemId, itemType) {
        if (!confirm('このアイテムを削除しますか？')) {
            return;
        }

        try {
            const response = await fetch(`/api/v1/${itemType}/${itemId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showMessage('アイテムを削除しました', 'success');
                this.loadData();
            } else {
                throw new Error('Failed to delete item');
            }
        } catch (error) {
            console.error('Error deleting item:', error);
            this.showMessage('アイテムの削除に失敗しました', 'error');
        }
    }

    editItem(itemId, itemType) {
        // For now, just show an alert. Could implement edit modal later
        alert('編集機能は今後実装予定です');
    }

    showLoading() {
        ['todo', 'progress', 'done'].forEach(status => {
            const column = document.getElementById(`${status}-column`);
            column.innerHTML = '<div class="loading">読み込み中...</div>';
        });
    }

    hideLoading() {
        // Loading will be hidden when renderBoard is called
    }

    showMessage(text, type = 'success') {
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        
        document.body.appendChild(message);
        
        // Trigger animation
        setTimeout(() => {
            message.classList.add('show');
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            message.classList.remove('show');
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the kanban board when the page loads
let kanban;
document.addEventListener('DOMContentLoaded', () => {
    kanban = new KanbanBoard();
});