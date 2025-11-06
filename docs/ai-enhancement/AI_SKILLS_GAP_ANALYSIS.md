# 🤖 AI工程师技能缺口分析与扩充方案

## 📊 当前状态评估

### ✅ 已覆盖的AI相关技能

1. **数据处理基础** ⭐⭐⭐⭐⭐
   - pandas 数据清洗、聚合、透视（Set B, G）
   - NumPy 向量化计算（Set D）
   - 数据类型转换、缺失值处理
   - 时间序列处理（环比、同比）

2. **文本处理** ⭐⭐⭐⭐
   - 正则表达式（Set A, E, F, V）
   - OCR文本清洗（Set V - 仅模拟）
   - 字符串规范化

3. **工程能力** ⭐⭐⭐⭐
   - 并发编程（asyncio/threading）
   - API设计与服务化
   - 日志与可观测性
   - 异常处理

### ❌ 严重缺失的AI核心技能

#### 1. **机器学习基础** 🔴 完全缺失

**缺失内容**：
- ❌ 特征工程（编码、归一化、分箱、特征选择）
- ❌ 模型训练与评估（sklearn基础）
- ❌ 交叉验证与超参数调优
- ❌ 模型评估指标（准确率、精确率、召回率、F1、AUC）
- ❌ 过拟合与正则化
- ❌ 模型持久化（pickle/joblib）

**影响**：
- 无法评估候选人的ML基础
- 缺少实际建模能力考察
- 不符合"AI工程师"岗位定位

#### 2. **深度学习基础** 🔴 完全缺失

**缺失内容**：
- ❌ 张量操作（PyTorch/TensorFlow基础）
- ❌ 神经网络基本概念
- ❌ 损失函数与优化器
- ❌ 模型训练循环
- ❌ GPU加速基础

**影响**：
- 无法评估深度学习能力
- 现代AI岗位必备技能缺失

#### 3. **NLP专项** 🟡 严重不足

**现状**：
- ✅ 仅有基础文本处理（正则、清洗）
- ❌ 缺少分词、词向量
- ❌ 缺少文本分类、情感分析
- ❌ 缺少命名实体识别（NER）
- ❌ 缺少文本相似度计算

**税务场景需求**：
- 发票文本分类
- 税务政策文本理解
- 合同关键信息提取
- 税务问答系统

#### 4. **计算机视觉（OCR）** 🟡 严重不足

**现状**：
- ✅ Set V 有OCR文本清洗（但仅模拟）
- ❌ 缺少实际OCR调用（Tesseract/PaddleOCR）
- ❌ 缺少图像预处理
- ❌ 缺少OCR结果后处理
- ❌ 缺少表格识别

**税务场景需求**：
- 发票OCR识别
- 表格结构化提取
- 印章检测
- 图像质量评估

#### 5. **模型部署与服务化** 🟡 部分缺失

**现状**：
- ✅ 有API设计基础（Set S, U, AB）
- ❌ 缺少模型推理服务
- ❌ 缺少批量预测
- ❌ 缺少模型版本管理
- ❌ 缺少A/B测试

#### 6. **数据标注与质量** 🔴 完全缺失

**缺失内容**：
- ❌ 数据标注流程
- ❌ 标注质量评估
- ❌ 主动学习
- ❌ 数据增强

---

## 🎯 扩充方案（按优先级）

### 🔥 P0 - 核心AI技能（必须添加）

#### 1. 机器学习基础套题（Set ML1）

**题目设计**：
```python
# 1. 特征工程
def encode_categorical(df, col: str, method: str = "onehot"):
    """类别编码：onehot/label/target"""
    
def normalize_features(df, cols: List[str], method: str = "standard"):
    """特征归一化：standard/minmax/robust"""
    
def create_bins(series, bins: int = 5, labels=None):
    """数值分箱"""

# 2. 模型训练与评估
def train_classifier(X_train, y_train, model_type: str = "logistic"):
    """训练分类器：logistic/tree/rf"""
    
def evaluate_model(y_true, y_pred, y_prob=None) -> dict:
    """计算评估指标：accuracy/precision/recall/f1/auc"""
    
def cross_validate_model(X, y, model, cv: int = 5) -> dict:
    """交叉验证"""

# 3. 模型持久化
def save_model(model, path: str):
    """保存模型"""
    
def load_and_predict(model_path: str, X) -> np.ndarray:
    """加载模型并预测"""
```

**业务场景**：
- 税务风险分类（高/中/低风险）
- 发票真伪判断
- 企业信用评分

#### 2. NLP基础套题（Set NLP1）

**题目设计**：
```python
# 1. 文本预处理
def tokenize_chinese(text: str) -> List[str]:
    """中文分词（jieba）"""
    
def remove_stopwords(tokens: List[str]) -> List[str]:
    """去除停用词"""
    
def extract_keywords(text: str, topk: int = 5) -> List[str]:
    """关键词提取（TF-IDF/TextRank）"""

# 2. 文本特征
def text_to_tfidf(texts: List[str]) -> np.ndarray:
    """TF-IDF向量化"""
    
def compute_text_similarity(text1: str, text2: str) -> float:
    """文本相似度（余弦/编辑距离）"""

# 3. 文本分类
def train_text_classifier(texts: List[str], labels: List[int]):
    """训练文本分类器"""
    
def extract_entities(text: str) -> List[Dict]:
    """命名实体识别（金额/日期/公司名）"""
```

**业务场景**：
- 发票描述分类（商品类别）
- 税务政策文本检索
- 合同关键信息提取
- 发票抬头标准化

#### 3. OCR实战套题（Set OCR1）

**题目设计**：
```python
# 1. 图像预处理
def preprocess_invoice_image(img_path: str) -> np.ndarray:
    """发票图像预处理：灰度化/二值化/去噪/倾斜校正"""
    
def detect_text_regions(img: np.ndarray) -> List[Tuple]:
    """文本区域检测"""

# 2. OCR识别
def ocr_invoice(img_path: str, engine: str = "paddleocr") -> List[Dict]:
    """发票OCR识别"""
    
def extract_invoice_fields(ocr_result: List[Dict]) -> Dict:
    """从OCR结果提取结构化字段"""

# 3. 后处理与校验
def correct_ocr_errors(text: str, field_type: str) -> str:
    """OCR错误纠正（基于规则/字典）"""
    
def validate_invoice_data(data: Dict) -> Tuple[bool, List[str]]:
    """发票数据校验"""
```

**业务场景**：
- 增值税发票识别
- 表格型发票结构化
- 印章检测与验证
- 多张发票批量处理

---

### 🔶 P1 - 进阶AI技能（强烈建议）

#### 4. 深度学习基础套题（Set DL1）

**题目设计**：
```python
# 1. 张量操作
def tensor_operations():
    """PyTorch基础：创建/索引/变形/运算"""
    
def build_simple_nn(input_dim: int, hidden_dim: int, output_dim: int):
    """构建简单神经网络"""

# 2. 训练循环
def train_epoch(model, dataloader, optimizer, criterion):
    """训练一个epoch"""
    
def evaluate_epoch(model, dataloader, criterion):
    """评估一个epoch"""

# 3. 实际应用
def train_invoice_classifier(train_data, val_data, epochs: int = 10):
    """训练发票分类模型"""
```

**业务场景**：
- 发票图像分类
- 文本情感分析
- 序列标注（NER）

#### 5. 模型部署套题（Set DEPLOY1）

**题目设计**：
```python
# 1. 模型推理服务
def create_prediction_api(model_path: str, port: int = 8000):
    """创建模型推理API（FastAPI/Flask）"""
    
def batch_predict(model, data_path: str, batch_size: int = 32):
    """批量预测"""

# 2. 性能优化
def optimize_inference(model):
    """推理优化：量化/剪枝/ONNX转换"""
    
def cache_predictions(cache_key: str, ttl: int = 3600):
    """预测结果缓存"""

# 3. 监控与版本管理
def log_prediction_metrics(y_true, y_pred, model_version: str):
    """记录预测指标"""
    
def ab_test_models(model_a, model_b, traffic_split: float = 0.5):
    """A/B测试"""
```

#### 6. 数据工程套题（Set DATA_ENG1）

**题目设计**：
```python
# 1. 数据标注
def create_annotation_task(data: List[Dict], task_type: str):
    """创建标注任务"""
    
def validate_annotations(annotations: List[Dict]) -> float:
    """标注质量评估（一致性/覆盖率）"""

# 2. 数据增强
def augment_text(text: str, methods: List[str]) -> List[str]:
    """文本数据增强：同义词替换/回译/随机插入"""
    
def augment_image(img: np.ndarray) -> List[np.ndarray]:
    """图像数据增强：旋转/翻转/噪声/亮度"""

# 3. 主动学习
def select_samples_for_annotation(model, unlabeled_data, n: int = 100):
    """主动学习样本选择（不确定性采样）"""
```

---

### 🔷 P2 - 高级AI技能（时间充裕时）

#### 7. 大模型应用套题（Set LLM1）

**题目设计**：
```python
# 1. Prompt工程
def create_tax_qa_prompt(question: str, context: str) -> str:
    """构建税务问答Prompt"""
    
def extract_info_with_llm(text: str, schema: Dict) -> Dict:
    """使用LLM提取结构化信息"""

# 2. RAG（检索增强生成）
def build_tax_knowledge_base(documents: List[str]):
    """构建税务知识库（向量数据库）"""
    
def retrieve_and_generate(query: str, top_k: int = 3) -> str:
    """检索相关文档并生成答案"""

# 3. Fine-tuning
def finetune_llm_for_tax(train_data: List[Dict], base_model: str):
    """微调LLM用于税务场景"""
```

#### 8. 时间序列预测套题（Set TS1）

**题目设计**：
```python
# 1. 时间序列特征
def create_lag_features(df, col: str, lags: List[int]):
    """创建滞后特征"""
    
def create_rolling_features(df, col: str, windows: List[int]):
    """创建滚动窗口特征"""

# 2. 预测模型
def train_arima_model(series, order: Tuple[int, int, int]):
    """训练ARIMA模型"""
    
def train_lstm_forecaster(X_train, y_train, seq_len: int = 12):
    """训练LSTM预测模型"""

# 3. 业务应用
def forecast_tax_revenue(historical_data, periods: int = 12):
    """预测税收收入"""
```

**业务场景**：
- 税收收入预测
- 发票开具量预测
- 企业纳税趋势分析

---

## 📋 具体实施计划

### 阶段1：核心AI技能（2-3周）

**Week 1: 机器学习基础**
```bash
# 创建 Set ML1
interview_exercises/set_ML1_blank.py
interview_exercises/set_ML1_answers.py
interview_exercises/set_ML1_answers_annotated.py

# 内容：
# - 特征工程（5题）
# - 模型训练（5题）
# - 模型评估（5题）
# - 实战：税务风险分类
```

**Week 2: NLP基础**
```bash
# 创建 Set NLP1
# 内容：
# - 中文分词与预处理（5题）
# - 文本特征提取（5题）
# - 文本分类（5题）
# - 实战：发票描述分类
```

**Week 3: OCR实战**
```bash
# 创建 Set OCR1
# 内容：
# - 图像预处理（5题）
# - OCR识别与提取（5题）
# - 后处理与校验（5题）
# - 实战：发票批量识别
```

### 阶段2：进阶技能（2-3周）

- Set DL1: 深度学习基础
- Set DEPLOY1: 模型部署
- Set DATA_ENG1: 数据工程

### 阶段3：高级技能（可选）

- Set LLM1: 大模型应用
- Set TS1: 时间序列预测

---

## 🎯 AI技能速查卡

### 机器学习常用API

```python
# sklearn 基础
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score

# 特征工程
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# 模型训练
model = LogisticRegression()
model.fit(X_train, y_train)

# 评估
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
```

### NLP常用API

```python
# jieba 分词
import jieba
tokens = jieba.lcut("增值税专用发票")

# TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# 文本相似度
from sklearn.metrics.pairwise import cosine_similarity
sim = cosine_similarity(vec1, vec2)
```

### OCR常用API

```python
# PaddleOCR
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')
result = ocr.ocr(img_path)

# Tesseract
import pytesseract
text = pytesseract.image_to_string(img, lang='chi_sim')
```

---

## ✅ 预期成果

### 完成P0后

**AI技能覆盖度**：
- 机器学习基础：0/10 → **8/10** ✅
- NLP基础：2/10 → **7/10** ✅
- OCR实战：1/10 → **7/10** ✅
- 综合AI能力：**4/10 → 7.5/10**

**岗位匹配度**：
- 税务所AI工程师：**60% → 85%**
- 通用AI工程师：**40% → 70%**

### 完成P0+P1后

**AI技能覆盖度**：
- 深度学习：0/10 → **6/10** ✅
- 模型部署：3/10 → **8/10** ✅
- 数据工程：2/10 → **7/10** ✅
- 综合AI能力：**7.5/10 → 9/10**

**岗位匹配度**：
- 税务所AI工程师：**85% → 95%**
- 通用AI工程师：**70% → 85%**

---

## 🚀 立即行动

**是否需要我立即创建以下内容？**

1. ✅ **Set ML1**（机器学习基础套题）
2. ✅ **Set NLP1**（NLP基础套题）
3. ✅ **Set OCR1**（OCR实战套题）
4. ✅ **AI_CHEATSHEET.md**（AI技能速查卡）
5. ✅ 更新 `interview_simulator.py` 添加 "ai" 主题
6. ✅ 更新 `INTERVIEW_SPRINT_GUIDE.md` 添加AI技能冲刺

**建议优先级**：
1. **立即创建** Set ML1（最核心）
2. **本周内创建** Set NLP1 + Set OCR1
3. **下周创建** Set DL1 + Set DEPLOY1

请告诉我是否开始创建这些AI专项套题？

