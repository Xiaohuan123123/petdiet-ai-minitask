/**
 * PetDiet AI 聊天模块
 * 处理用户输入、API调用、消息渲染
 */

const ChatApp = {
    // 对话历史
    messages: [],

    // API 基础地址
    API_BASE: window.location.origin,

    // 初始化
    init() {
        this.bindEvents();
        this.scrollToBottom();
        console.log('🐾 宠食记 PetDiet AI - ChatApp initialized');
    },

    // 绑定事件
    bindEvents() {
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const micBtn = document.getElementById('mic-btn');

        // 回车发送
        input?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // 发送按钮
        sendBtn?.addEventListener('click', () => this.sendMessage());

        // 语音按钮（预留）
        micBtn?.addEventListener('click', () => {
            alert('语音输入功能开发中...');
        });

        // 快捷标签
        document.querySelectorAll('.skill-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                const text = pill.textContent.trim();
                input.value = `帮我做一个${text}的方案`;
                input.focus();
            });
        });
    },

    // 发送消息
    async sendMessage() {
        const input = document.getElementById('chat-input');
        const text = input.value.trim();

        if (!text) return;

        // 清空输入框
        input.value = '';

        // 添加用户消息到界面
        this.addMessageToUI('user', text);

        // 添加到对话历史
        this.messages.push({ role: 'user', content: text });

        // 显示思考中状态
        const thinkingId = this.showThinking();

        try {
            // 调用 API
            const response = await fetch(`${this.API_BASE}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: this.messages })
            });

            const data = await response.json();

            // 移除思考状态
            this.removeThinking(thinkingId);

            if (data.success) {
                // 添加 AI 回复到界面
                this.addMessageToUI('assistant', data.message);

                // 添加到对话历史
                this.messages.push({ role: 'assistant', content: data.message });
            } else {
                this.addMessageToUI('error', data.error || '请求失败，请重试');
            }
        } catch (error) {
            this.removeThinking(thinkingId);
            this.addMessageToUI('error', '网络错误，请检查后端服务是否启动');
            console.error('Chat error:', error);
        }

        this.scrollToBottom();
    },

    // 添加消息到界面
    addMessageToUI(role, content) {
        const chatContainer = document.getElementById('chat-messages');
        if (!chatContainer) return;

        // 如果是第一条消息，清除预设内容
        if (this.messages.length === 1) {
            chatContainer.innerHTML = '';
        }

        if (role === 'user') {
            // 用户消息
            const html = `
                <div class="flex justify-end">
                    <div class="message-bubble message-user">
                        <p>${this.escapeHtml(content)}</p>
                    </div>
                </div>
            `;
            chatContainer.insertAdjacentHTML('beforeend', html);
        } else if (role === 'assistant') {
            // AI 思考卡片
            const thinkingHtml = `
                <div class="suggestion-card mb-3">
                    <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <i data-lucide="lightbulb" class="w-4 h-4 text-primary-600"></i>
                    </div>
                    <span class="text-sm text-warm-text flex-1">正在分析您的问题...</span>
                    <i data-lucide="chevron-right" class="w-4 h-4 text-warm-muted"></i>
                </div>
            `;
            chatContainer.insertAdjacentHTML('beforeend', thinkingHtml);

            // AI 回复内容（支持 Markdown 基础渲染）
            const renderedContent = this.renderMarkdown(content);
            const html = `
                <div class="ai-response">
                    ${renderedContent}
                </div>
            `;
            chatContainer.insertAdjacentHTML('beforeend', html);

            // 重新渲染图标
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        } else if (role === 'error') {
            const html = `
                <div class="flex justify-center">
                    <div class="px-4 py-2 bg-red-50 text-red-600 rounded-xl text-sm">
                        ${this.escapeHtml(content)}
                    </div>
                </div>
            `;
            chatContainer.insertAdjacentHTML('beforeend', html);
        }

        this.scrollToBottom();
    },

    // 显示思考中状态
    showThinking() {
        const chatContainer = document.getElementById('chat-messages');
        const id = 'thinking-' + Date.now();

        const html = `
            <div id="${id}" class="flex justify-center">
                <div class="flex items-center gap-2 px-4 py-2 bg-primary-50 rounded-xl">
                    <div class="animate-spin w-4 h-4 border-2 border-primary-400 border-t-transparent rounded-full"></div>
                    <span class="text-sm text-primary-700">AI 正在思考...</span>
                </div>
            </div>
        `;
        chatContainer.insertAdjacentHTML('beforeend', html);
        this.scrollToBottom();

        return id;
    },

    // 移除思考状态
    removeThinking(id) {
        const element = document.getElementById(id);
        if (element) element.remove();
    },

    // 简单的 Markdown 渲染
    renderMarkdown(text) {
        // 转义 HTML
        let html = this.escapeHtml(text);

        // 处理加粗 **text**
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // 处理标题 ### text
        html = html.replace(/^### (.*?)(\n|$)/gm, '<p class="section-title">$1</p>');

        // 处理分割线 ---
        html = html.replace(/^---$/gm, '<hr class="divider">');

        // 处理有序列表
        html = html.replace(/^(\d+)\. (.*?)(\n|$)/gm, '<li>$2</li>');

        // 处理无序列表
        html = html.replace(/^- (.*?)(\n|$)/gm, '<li>$1</li>');

        // 处理表格（简单实现）
        if (html.includes('|')) {
            html = this.renderTable(html);
        }

        // 处理段落（换行）
        html = html.replace(/\n\n/g, '</p><p>');
        html = html.replace(/\n/g, '<br>');

        // 包裹在段落中
        if (!html.startsWith('<')) {
            html = '<p>' + html + '</p>';
        }

        return html;
    },

    // 渲染表格
    renderTable(text) {
        const lines = text.split('\n');
        let tableHtml = '';
        let inTable = false;
        let isHeader = true;

        for (const line of lines) {
            if (line.includes('|')) {
                if (!inTable) {
                    tableHtml += '<table>';
                    inTable = true;
                    isHeader = true;
                }

                // 跳过分隔行 |---|---|
                if (line.match(/^\|[\s-]+\|/)) {
                    continue;
                }

                const cells = line.split('|').filter(c => c.trim());
                const tag = isHeader ? 'th' : 'td';
                const rowTag = isHeader ? 'thead' : (isHeader ? 'thead' : 'tbody');

                if (isHeader) {
                    tableHtml += '<thead><tr>';
                    cells.forEach(cell => {
                        tableHtml += `<th>${cell.trim()}</th>`;
                    });
                    tableHtml += '</tr></thead><tbody>';
                    isHeader = false;
                } else {
                    tableHtml += '<tr>';
                    cells.forEach(cell => {
                        tableHtml += `<td>${cell.trim()}</td>`;
                    });
                    tableHtml += '</tr>';
                }
            } else {
                if (inTable) {
                    tableHtml += '</tbody></table>';
                    inTable = false;
                    isHeader = true;
                }
                tableHtml += line + '\n';
            }
        }

        if (inTable) {
            tableHtml += '</tbody></table>';
        }

        return tableHtml;
    },

    // HTML 转义
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    // 滚动到底部
    scrollToBottom() {
        const chatContainer = document.getElementById('chat-messages');
        if (chatContainer) {
            setTimeout(() => {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 100);
        }
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    ChatApp.init();
});
