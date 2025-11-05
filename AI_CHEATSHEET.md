# 🤖 AI工程师技能速查卡

> 机器学习、NLP、OCR核心知识点快速参考

---

## 🧠 机器学习基础

### 特征工程

#### 1. 类别编码

```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Label编码（转为整数）
le = LabelEncoder()
encoded = le.fit_transform(['high', 'low', 'medium'])  # [0, 1, 2]

# One-Hot编码
ohe = OneHotEncoder(sparse_output=False)
values_2d = np.array(['A', 'B', 'A']).reshape(-1, 1)
encoded = ohe.fit_transform(values_2d)  # [[1,0], [0,1], [1,0]]

# pandas get_dummies（更简单）
import pandas as pd
df = pd.DataFrame({'category': ['A', 'B', 'A']})
encoded = pd.get_dummies(df['category'])
```

#### 2. 数值归一化

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# 标准化：(x - mean) / std
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 注意：用transform而非fit_transform

# Min-Max归一化：缩放到[0, 1]
scaler = MinMaxScaler(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X)

# Robust归一化：对异常值鲁棒
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
```

#### 3. 数值分箱

```python
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

# pandas.cut（等宽分箱）
bins = pd.cut([1, 5, 10, 15, 20], bins=3, labels=False)  # [0, 0, 1, 2, 2]

# pandas.qcut（等频分箱）
bins = pd.qcut([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], q=4, labels=False)

# sklearn KBinsDiscretizer
kbd = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile')
X_binned = kbd.fit_transform(X)
```

---

### 模型训练

#### 1. 分类器

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

# 逻辑回归
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train, y_train)

# 决策树
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 随机森林
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 梯度提升树（GBDT）
model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 支持向量机
model = SVC(kernel='rbf', probability=True, random_state=42)
model.fit(X_train, y_train)
```

#### 2. 回归器

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor

# 线性回归
model = LinearRegression()
model.fit(X_train, y_train)

# Ridge回归（L2正则化）
model = Ridge(alpha=1.0)
model.fit(X_train, y_train)

# Lasso回归（L1正则化）
model = Lasso(alpha=1.0)
model.fit(X_train, y_train)

# 随机森林回归
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

---

### 模型评估

#### 1. 分类指标

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    roc_auc_score, roc_curve
)

# 基本指标
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='binary')  # 或 'weighted'
recall = recall_score(y_true, y_pred, average='binary')
f1 = f1_score(y_true, y_pred, average='binary')

# 混淆矩阵
cm = confusion_matrix(y_true, y_pred)
# [[TN, FP],
#  [FN, TP]]

# 分类报告
report = classification_report(y_true, y_pred)

# AUC（需要预测概率）
y_prob = model.predict_proba(X_test)[:, 1]  # 正类概率
auc = roc_auc_score(y_true, y_prob)

# ROC曲线
fpr, tpr, thresholds = roc_curve(y_true, y_prob)
```

#### 2. 回归指标

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# MSE（均方误差）
mse = mean_squared_error(y_true, y_pred)

# RMSE（均方根误差）
rmse = np.sqrt(mse)

# MAE（平均绝对误差）
mae = mean_absolute_error(y_true, y_pred)

# R²（决定系数）
r2 = r2_score(y_true, y_pred)
```

#### 3. 交叉验证

```python
from sklearn.model_selection import cross_val_score, cross_validate

# 简单交叉验证
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Mean: {scores.mean():.4f}, Std: {scores.std():.4f}")

# 多指标交叉验证
scoring = ['accuracy', 'precision', 'recall', 'f1']
scores = cross_validate(model, X, y, cv=5, scoring=scoring)
```

---

### 数据分割

```python
from sklearn.model_selection import train_test_split

# 简单分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 分层分割（保持类别比例）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

---

## 📝 NLP基础

### 中文分词

```python
import jieba

# 基本分词
text = "增值税专用发票"
tokens = jieba.lcut(text)  # ['增值税', '专用', '发票']

# 添加自定义词典
jieba.add_word("增值税专用发票")
tokens = jieba.lcut(text)  # ['增值税专用发票']

# 关键词提取
import jieba.analyse
keywords = jieba.analyse.extract_tags(text, topK=5)
```

### 停用词过滤

```python
# 加载停用词表
with open('stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

# 过滤
tokens = [w for w in tokens if w not in stopwords]
```

### TF-IDF

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# 创建向量化器
vectorizer = TfidfVectorizer(max_features=1000)

# 训练并转换
texts = ["文本1", "文本2", "文本3"]
X = vectorizer.fit_transform(texts)

# 获取特征名
feature_names = vectorizer.get_feature_names_out()
```

### 文本相似度

```python
from sklearn.metrics.pairwise import cosine_similarity

# 余弦相似度
sim = cosine_similarity(vec1, vec2)

# 编辑距离
from difflib import SequenceMatcher
ratio = SequenceMatcher(None, text1, text2).ratio()
```

---

## 🖼️ OCR基础

### PaddleOCR

```python
from paddleocr import PaddleOCR

# 初始化
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 识别
result = ocr.ocr(img_path, cls=True)

# 解析结果
for line in result[0]:
    box = line[0]  # 坐标
    text = line[1][0]  # 文本
    confidence = line[1][1]  # 置信度
    print(f"{text} ({confidence:.2f})")
```

### Tesseract

```python
import pytesseract
from PIL import Image

# 识别
img = Image.open(img_path)
text = pytesseract.image_to_string(img, lang='chi_sim')

# 获取详细信息
data = pytesseract.image_to_data(img, lang='chi_sim', output_type=pytesseract.Output.DICT)
```

### 图像预处理

```python
import cv2

# 读取图像
img = cv2.imread(img_path)

# 灰度化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 二值化
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 去噪
denoised = cv2.fastNlMeansDenoising(gray)

# 倾斜校正
coords = np.column_stack(np.where(binary > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
```

---

## 🎯 常见陷阱

### 1. 数据泄露

```python
# ❌ 错误：在分割前归一化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled, ...)

# ✅ 正确：先分割，再归一化
X_train, X_test = train_test_split(X, ...)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 用transform而非fit_transform
```

### 2. 类别不平衡

```python
# 方法1：调整类别权重
model = LogisticRegression(class_weight='balanced')

# 方法2：过采样（SMOTE）
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# 方法3：欠采样
from imblearn.under_sampling import RandomUnderSampler
rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(X_train, y_train)
```

### 3. 过拟合

```python
# 方法1：正则化
model = Ridge(alpha=1.0)  # L2
model = Lasso(alpha=1.0)  # L1

# 方法2：减少模型复杂度
model = DecisionTreeClassifier(max_depth=5)  # 限制深度
model = RandomForestClassifier(max_features='sqrt')  # 限制特征数

# 方法3：增加数据
# 数据增强、收集更多数据

# 方法4：Dropout（深度学习）
# 在神经网络中添加Dropout层
```

---

## 📊 评估指标选择

| 场景 | 推荐指标 | 原因 |
|------|---------|------|
| 类别平衡 | Accuracy | 简单直观 |
| 类别不平衡 | F1, AUC | 综合考虑精确率和召回率 |
| 关注误报 | Precision | 减少假阳性 |
| 关注漏报 | Recall | 减少假阴性 |
| 排序质量 | AUC | 评估模型区分能力 |
| 回归任务 | RMSE, MAE | 误差的绝对值 |

---

**快速记忆口诀**：

- 特征工程：**编码类别，归一数值，分箱离散**
- 模型训练：**先分割，再归一，最后训练**
- 模型评估：**准确率看整体，F1看平衡，AUC看排序**
- NLP：**分词去停，向量化，算相似**
- OCR：**预处理图像，识别文本，后处理校验**

