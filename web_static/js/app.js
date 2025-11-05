// Python学习平台 - 前端应用

class PythonLearningApp {
    constructor() {
        this.questions = [];
        this.currentQuestion = null;
        this.editor = null;
        this.originalCode = '';
        
        this.init();
    }
    
    async init() {
        // 初始化CodeMirror编辑器
        this.editor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
            mode: 'python',
            theme: 'monokai',
            lineNumbers: true,
            indentUnit: 4,
            indentWithTabs: false,
            lineWrapping: true,
            matchBrackets: true,
            autoCloseBrackets: true,
        });
        
        // 绑定事件
        this.bindEvents();
        
        // 加载题目列表
        await this.loadQuestions();
    }
    
    bindEvents() {
        // 筛选器
        document.getElementById('categoryFilter').addEventListener('change', () => this.filterQuestions());
        document.getElementById('difficultyFilter').addEventListener('change', () => this.filterQuestions());
        
        // 按钮
        document.getElementById('runCodeBtn').addEventListener('click', () => this.runCode());
        document.getElementById('resetCodeBtn').addEventListener('click', () => this.resetCode());
        document.getElementById('showHintBtn').addEventListener('click', () => this.showHint());
        document.getElementById('showAnswerBtn').addEventListener('click', () => this.showAnswer());
        document.getElementById('clearOutputBtn').addEventListener('click', () => this.clearOutput());
    }
    
    async loadQuestions() {
        try {
            const response = await fetch('/api/questions');
            const data = await response.json();
            this.questions = data.questions;
            this.renderQuestionList();
        } catch (error) {
            console.error('加载题目失败:', error);
            this.showError('加载题目失败，请刷新页面重试');
        }
    }
    
    renderQuestionList(filteredQuestions = null) {
        const questions = filteredQuestions || this.questions;
        const listEl = document.getElementById('questionList');
        
        if (questions.length === 0) {
            listEl.innerHTML = '<div class="loading">没有找到题目</div>';
            return;
        }
        
        listEl.innerHTML = questions.map(q => `
            <div class="question-item" data-id="${q.id}">
                <div class="question-item-title">${q.id}. ${q.name}</div>
                <div class="question-item-meta">
                    <span>${q.category}</span>
                    <span>${q.difficulty}</span>
                    <span>${q.time}</span>
                </div>
            </div>
        `).join('');
        
        // 绑定点击事件
        listEl.querySelectorAll('.question-item').forEach(item => {
            item.addEventListener('click', () => {
                const questionId = item.dataset.id;
                this.loadQuestion(questionId);
            });
        });
    }
    
    filterQuestions() {
        const category = document.getElementById('categoryFilter').value;
        const difficulty = document.getElementById('difficultyFilter').value;
        
        const filtered = this.questions.filter(q => {
            const matchCategory = !category || q.category === category;
            const matchDifficulty = !difficulty || q.difficulty.startsWith(difficulty);
            return matchCategory && matchDifficulty;
        });
        
        this.renderQuestionList(filtered);
    }
    
    async loadQuestion(questionId) {
        try {
            const response = await fetch(`/api/question/${questionId}`);
            const data = await response.json();
            
            this.currentQuestion = data;
            this.originalCode = data.code;
            
            // 更新UI
            document.getElementById('welcomePage').style.display = 'none';
            document.getElementById('questionPage').style.display = 'block';
            
            document.getElementById('questionTitle').textContent = `${data.id}. ${data.meta.name}`;
            document.getElementById('questionCategory').textContent = data.meta.category;
            document.getElementById('questionDifficulty').textContent = data.meta.difficulty;
            document.getElementById('questionTime').textContent = data.meta.time;
            
            // 设置代码
            this.editor.setValue(data.code);
            
            // 高亮当前题目
            document.querySelectorAll('.question-item').forEach(item => {
                item.classList.toggle('active', item.dataset.id === questionId);
            });
            
            // 清空输出
            this.clearOutput();
            
        } catch (error) {
            console.error('加载题目失败:', error);
            this.showError('加载题目失败，请重试');
        }
    }
    
    async runCode() {
        const code = this.editor.getValue();
        const outputEl = document.getElementById('outputContent');
        
        // 显示加载状态
        outputEl.innerHTML = '<div class="output-info">⏳ 正在执行代码...</div>';
        
        try {
            const response = await fetch('/api/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code }),
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showOutput(data.stdout, 'success');
            } else {
                const errorMsg = data.stderr || data.error || '未知错误';
                this.showOutput(errorMsg, 'error');
            }
            
        } catch (error) {
            console.error('执行代码失败:', error);
            this.showOutput('执行失败: ' + error.message, 'error');
        }
    }
    
    showOutput(text, type = 'info') {
        const outputEl = document.getElementById('outputContent');
        const className = `output-${type}`;
        outputEl.innerHTML = `<pre class="${className}">${this.escapeHtml(text)}</pre>`;
    }

    resetCode() {
        if (confirm('确定要重置代码吗？所有修改将丢失。')) {
            this.editor.setValue(this.originalCode);
            this.clearOutput();
        }
    }

    showHint() {
        if (!this.currentQuestion) return;

        const hints = [
            '💡 提示1: 仔细阅读函数的文档字符串（docstring）',
            '💡 提示2: 查看测试用例了解预期的输入输出',
            '💡 提示3: 使用print()调试中间结果',
            '💡 提示4: 注意边界条件和异常处理',
            '💡 提示5: 参考Python官方文档了解API用法',
        ];

        const hintText = hints.join('\n');
        this.showOutput(hintText, 'info');
    }

    showAnswer() {
        if (!this.currentQuestion || !this.currentQuestion.answer_code) {
            alert('该题目暂无答案');
            return;
        }

        if (confirm('查看答案将显示完整解答。确定要查看吗？')) {
            this.editor.setValue(this.currentQuestion.answer_code);
            this.showOutput('✅ 已加载答案代码。建议先尝试自己完成，再查看答案学习。', 'info');
        }
    }

    clearOutput() {
        const outputEl = document.getElementById('outputContent');
        outputEl.innerHTML = '<div class="output-placeholder">运行代码后，测试结果将显示在这里</div>';
    }

    showError(message) {
        this.showOutput('❌ ' + message, 'error');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.app = new PythonLearningApp();
});

