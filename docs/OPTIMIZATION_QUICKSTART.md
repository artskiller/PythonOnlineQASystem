# 🚀 优化方案快速开始指南

> **目标**: 快速实现核心优化功能  
> **时间**: 4周MVP版本  
> **优先级**: P0功能优先

---

## 📋 4周MVP计划

### Week 1: 题目配置化

**目标**: 实现YAML格式题目支持

**任务清单**:
- [ ] Day 1-2: 设计YAML题目格式
- [ ] Day 3-4: 实现题目解析器
- [ ] Day 5: 实现题目生成工具
- [ ] Day 6-7: 测试和文档

**交付物**:
```yaml
# 示例题目文件: questions/basic/str001.yml
id: STR001
title: 字符串反转
type: coding
difficulty: 1
estimated_time: 5

description: |
  实现字符串反转功能

template: |
  def reverse_string(s: str) -> str:
      # TODO
      pass

solution: |
  def reverse_string(s: str) -> str:
      return s[::-1]

test_cases:
  - input: ["hello"]
    output: "olleh"
```

**代码示例**:
```python
# tools/question_parser.py
import yaml
from pathlib import Path

class QuestionParser:
    def parse_yaml(self, yaml_file):
        """解析YAML题目文件"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return {
            'id': data['id'],
            'title': data['title'],
            'type': data.get('type', 'coding'),
            'difficulty': data.get('difficulty', 1),
            'description': data['description'],
            'template': data.get('template', ''),
            'solution': data.get('solution', ''),
            'test_cases': data.get('test_cases', [])
        }
    
    def generate_python_file(self, question_data, output_dir):
        """生成Python练习文件"""
        # 生成blank版本
        blank_code = self._generate_blank(question_data)
        blank_file = output_dir / f"set_{question_data['id']}_blank.py"
        blank_file.write_text(blank_code, encoding='utf-8')
        
        # 生成answer版本
        answer_code = self._generate_answer(question_data)
        answer_file = output_dir / f"set_{question_data['id']}_answers.py"
        answer_file.write_text(answer_code, encoding='utf-8')
```

---

### Week 2: 智能提示系统

**目标**: 实现3级渐进式提示

**任务清单**:
- [ ] Day 1-2: 设计提示数据结构
- [ ] Day 3-4: 实现提示API
- [ ] Day 5-6: 前端提示界面
- [ ] Day 7: 测试

**交付物**:
```python
# web/api/hints.py
@app.route('/api/questions/<question_id>/hints/<int:level>', methods=['POST'])
def get_hint(question_id, level):
    """获取提示"""
    user = get_current_user()
    question = Question.query.get_or_404(question_id)
    
    # 检查提示级别
    if level < 1 or level > 3:
        return jsonify({'error': '无效的提示级别'}), 400
    
    # 获取提示
    hint = Hint.query.filter_by(
        question_id=question_id,
        level=level
    ).first_or_404()
    
    # 扣除积分
    cost = hint.cost
    if user.points < cost:
        return jsonify({'error': '积分不足'}), 400
    
    user.points -= cost
    
    # 记录使用提示
    hint_usage = HintUsage(
        user_id=user.id,
        question_id=question_id,
        level=level,
        cost=cost
    )
    db.session.add(hint_usage)
    db.session.commit()
    
    return jsonify({
        'hint': hint.content,
        'cost': cost,
        'remaining_points': user.points
    })
```

**前端界面**:
```vue
<!-- components/HintPanel.vue -->
<template>
  <div class="hint-panel">
    <h3>💡 需要帮助吗？</h3>
    
    <div class="hint-levels">
      <button 
        v-for="level in 3" 
        :key="level"
        @click="getHint(level)"
        :disabled="usedHints.includes(level)"
        class="hint-btn"
      >
        Level {{ level }} 提示
        <span class="cost">-{{ getHintCost(level) }}分</span>
      </button>
    </div>
    
    <div v-if="currentHint" class="hint-content">
      <p>{{ currentHint }}</p>
    </div>
    
    <div class="hint-warning">
      ⚠️ 使用提示会扣除积分并影响得分
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useQuestionStore } from '@/stores/question'

const questionStore = useQuestionStore()
const currentHint = ref('')
const usedHints = ref([])

const getHint = async (level) => {
  const hint = await questionStore.getHint(level)
  currentHint.value = hint.content
  usedHints.value.push(level)
}

const getHintCost = (level) => {
  return level * 5  // Level 1: 5分, Level 2: 10分, Level 3: 15分
}
</script>
```

---

### Week 3: 实时代码执行

**目标**: 实现安全的代码执行环境

**任务清单**:
- [ ] Day 1-2: Docker沙箱配置
- [ ] Day 3-4: 代码执行API
- [ ] Day 5-6: 测试结果展示
- [ ] Day 7: 性能优化

**交付物**:
```python
# web/api/execute.py
@app.route('/api/execute', methods=['POST'])
def execute_code():
    """执行代码"""
    data = request.json
    code = data.get('code', '')
    question_id = data.get('question_id')
    
    # 获取题目和测试用例
    question = Question.query.get_or_404(question_id)
    test_cases = TestCase.query.filter_by(
        question_id=question_id
    ).all()
    
    # 执行代码
    executor = CodeExecutor()
    results = executor.execute(code, test_cases, timeout=5)
    
    # 计算得分
    total = len(results)
    passed = sum(1 for r in results if r['success'])
    score = (passed / total) * 100 if total > 0 else 0
    
    # 保存提交记录
    submission = Submission(
        user_id=get_current_user().id,
        question_id=question_id,
        code=code,
        result=json.dumps(results),
        success=(score == 100),
        score=score
    )
    db.session.add(submission)
    db.session.commit()
    
    return jsonify({
        'results': results,
        'score': score,
        'passed': passed,
        'total': total
    })
```

---

### Week 4: 基础激励系统

**目标**: 实现积分和等级系统

**任务清单**:
- [ ] Day 1-2: 积分规则设计
- [ ] Day 3-4: 等级系统实现
- [ ] Day 5-6: 排行榜
- [ ] Day 7: 测试和优化

**交付物**:
```python
# models/user.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    
    def add_points(self, points):
        """添加积分"""
        self.points += points
        self._check_level_up()
    
    def _check_level_up(self):
        """检查是否升级"""
        level_thresholds = {
            1: 0,
            2: 100,
            3: 300,
            4: 600,
            5: 1000,
            6: 1500,
            7: 2000,
            8: 3000,
            9: 4500,
            10: 6000
        }
        
        for level, threshold in sorted(level_thresholds.items(), reverse=True):
            if self.points >= threshold:
                if level > self.level:
                    self.level = level
                    # 触发升级事件
                    self._on_level_up(level)
                break
    
    def _on_level_up(self, new_level):
        """升级回调"""
        # 发送通知
        # 解锁新功能
        pass
```

---

## 🎯 MVP功能清单

### ✅ 必须实现

1. **题目配置化**
   - YAML格式支持
   - 题目解析器
   - 自动生成工具

2. **智能提示**
   - 3级提示系统
   - 积分扣除机制
   - 提示使用记录

3. **代码执行**
   - Docker沙箱
   - 测试用例执行
   - 结果展示

4. **积分系统**
   - 积分规则
   - 等级系统
   - 简单排行榜

### ⏳ 可选功能

5. **成就系统**（Week 5-6）
6. **学习规划**（Week 7-8）
7. **挑战赛**（Week 9-10）

---

## 🛠️ 开发环境准备

### 1. 安装依赖

```bash
# Python依赖
pip install -r requirements.txt

# 新增依赖
pip install pyyaml docker pylint

# 前端依赖
cd web-frontend
npm install
```

### 2. 数据库初始化

```bash
# 创建数据库
python tools/init_db.py

# 导入示例题目
python tools/import_questions.py questions/
```

### 3. 启动服务

```bash
# 后端
python web/app.py

# 前端
cd web-frontend
npm run dev
```

---

## 📚 参考资源

- [完整优化方案](OPTIMIZATION_PLAN.md)
- [数据库设计](DATABASE_DESIGN.md)
- [API文档](API_DOCUMENTATION.md)
- [前端组件库](COMPONENT_LIBRARY.md)

---

**📅 创建日期**: 2025-11-07  
**⏱️ 预计完成**: 4周  
**👤 负责人**: 待定


