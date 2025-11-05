#!/usr/bin/env python3
"""
Python学习平台 - Web应用后端
提供交互式学习界面和实时代码执行
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import subprocess
import tempfile
import traceback
from pathlib import Path
from typing import Dict, List, Any
import re

app = Flask(__name__, 
            static_folder='web_static',
            template_folder='web_templates')
CORS(app)

# 项目根目录
ROOT_DIR = Path(__file__).parent
EXERCISES_DIR = ROOT_DIR / "interview_exercises"

# 题目元数据
QUESTION_SETS = {
    # AI专项
    "ML1": {"name": "机器学习基础", "category": "AI", "difficulty": "⭐⭐⭐", "time": "90分钟"},
    "NLP1": {"name": "自然语言处理", "category": "AI", "difficulty": "⭐⭐⭐", "time": "90分钟"},
    "OCR1": {"name": "OCR图像识别", "category": "AI", "difficulty": "⭐⭐⭐", "time": "90分钟"},
    
    # 基础入门
    "A": {"name": "Python基础", "category": "基础", "difficulty": "⭐", "time": "30分钟"},
    "K": {"name": "数据结构基础", "category": "基础", "difficulty": "⭐", "time": "30分钟"},
    
    # 数据处理
    "B": {"name": "Pandas数据处理", "category": "数据", "difficulty": "⭐⭐", "time": "45分钟"},
    "G": {"name": "NumPy数组操作", "category": "数据", "difficulty": "⭐⭐", "time": "45分钟"},
    
    # 算法思维
    "C": {"name": "算法基础", "category": "算法", "difficulty": "⭐⭐⭐", "time": "60分钟"},
    "I": {"name": "动态规划", "category": "算法", "difficulty": "⭐⭐⭐", "time": "60分钟"},
    "O": {"name": "图算法", "category": "算法", "difficulty": "⭐⭐⭐", "time": "60分钟"},
    
    # 并发编程
    "D": {"name": "异步编程", "category": "并发", "difficulty": "⭐⭐⭐", "time": "60分钟"},
    "H": {"name": "多线程", "category": "并发", "difficulty": "⭐⭐⭐", "time": "60分钟"},
    "T": {"name": "并发模式", "category": "并发", "difficulty": "⭐⭐⭐", "time": "60分钟"},
    
    # 业务应用
    "E": {"name": "财税计算", "category": "业务", "difficulty": "⭐⭐⭐", "time": "60分钟"},
    "J": {"name": "业务进阶", "category": "业务", "difficulty": "⭐⭐⭐", "time": "60分钟"},
    "F": {"name": "高精度计算", "category": "业务", "difficulty": "⭐⭐", "time": "45分钟"},
    "Q": {"name": "数据合规", "category": "业务", "difficulty": "⭐⭐", "time": "45分钟"},
}


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    """静态文件服务"""
    return send_from_directory('web_static', path)


@app.route('/api/questions')
def get_questions():
    """获取题目列表"""
    questions = []
    for set_id, meta in QUESTION_SETS.items():
        blank_file = EXERCISES_DIR / f"set_{set_id}_blank.py"
        if blank_file.exists():
            questions.append({
                "id": set_id,
                "name": meta["name"],
                "category": meta["category"],
                "difficulty": meta["difficulty"],
                "time": meta["time"],
                "file": f"set_{set_id}_blank.py"
            })
    
    return jsonify({"questions": questions})


@app.route('/api/question/<set_id>')
def get_question(set_id):
    """获取题目详情"""
    if set_id not in QUESTION_SETS:
        return jsonify({"error": "题目不存在"}), 404
    
    blank_file = EXERCISES_DIR / f"set_{set_id}_blank.py"
    answers_file = EXERCISES_DIR / f"set_{set_id}_answers.py"
    
    if not blank_file.exists():
        return jsonify({"error": "题目文件不存在"}), 404
    
    # 读取题目代码
    with open(blank_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # 读取答案（如果存在）
    answer_code = None
    if answers_file.exists():
        with open(answers_file, 'r', encoding='utf-8') as f:
            answer_code = f.read()
    
    # 提取函数列表
    functions = extract_functions(code)
    
    return jsonify({
        "id": set_id,
        "meta": QUESTION_SETS[set_id],
        "code": code,
        "answer_code": answer_code,
        "functions": functions
    })


def extract_functions(code: str) -> List[Dict[str, str]]:
    """提取代码中的函数定义"""
    functions = []
    lines = code.split('\n')
    current_func = None
    
    for i, line in enumerate(lines):
        # 匹配函数定义
        match = re.match(r'^def\s+(\w+)\s*\(([^)]*)\)', line)
        if match:
            func_name = match.group(1)
            func_params = match.group(2)
            
            # 查找文档字符串
            docstring = ""
            if i + 1 < len(lines) and '"""' in lines[i + 1]:
                doc_start = i + 1
                doc_end = doc_start
                for j in range(doc_start + 1, len(lines)):
                    if '"""' in lines[j]:
                        doc_end = j
                        break
                docstring = '\n'.join(lines[doc_start:doc_end + 1])
            
            functions.append({
                "name": func_name,
                "params": func_params,
                "docstring": docstring,
                "line": i + 1
            })
    
    return functions


@app.route('/api/run', methods=['POST'])
def run_code():
    """执行代码并返回结果"""
    data = request.json
    code = data.get('code', '')
    
    if not code:
        return jsonify({"error": "代码不能为空"}), 400
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # 执行代码（设置超时）
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=30,  # 30秒超时
            cwd=str(EXERCISES_DIR)
        )
        
        return jsonify({
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
    
    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": "代码执行超时（超过30秒）"
        }), 408
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"执行错误: {str(e)}"
        }), 500
    
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_file)
        except:
            pass


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    print("🚀 Python学习平台启动中...")
    print(f"📖 访问地址: http://localhost:{port}")
    print("💡 按 Ctrl+C 停止服务")
    app.run(debug=True, host='0.0.0.0', port=port)

