"""
AI专项套题 NLP1（自然语言处理基础）- 空白版

覆盖：
- 中文分词与预处理
- 文本特征提取（TF-IDF）
- 文本相似度计算
- 文本分类
- 实战：发票描述分类

依赖：jieba, scikit-learn
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import re


def tokenize_chinese(text: str) -> List[str]:
    """
    中文分词
    
    示例：
        "增值税专用发票" -> ["增值税", "专用", "发票"]
    
    提示：使用 jieba.lcut()
    """
    import jieba
    
    # TODO: 使用jieba分词
    return ____


def add_custom_word(word: str):
    """
    添加自定义词到jieba词典
    
    示例：
        add_custom_word("增值税专用发票")
        tokenize_chinese("增值税专用发票") -> ["增值税专用发票"]
    
    提示：使用 jieba.add_word()
    """
    import jieba
    
    # TODO: 添加自定义词
    ____


def remove_stopwords(tokens: List[str], stopwords: set) -> List[str]:
    """
    去除停用词
    
    示例：
        tokens = ["这是", "一张", "发票"]
        stopwords = {"这是", "一张"}
        结果 -> ["发票"]
    
    提示：列表推导式过滤
    """
    # TODO: 过滤停用词
    return [____ for ____ in ____ if ____]


def extract_keywords_tfidf(text: str, topk: int = 5) -> List[str]:
    """
    使用TF-IDF提取关键词
    
    提示：使用 jieba.analyse.extract_tags()
    """
    import jieba.analyse
    
    # TODO: 提取关键词
    return jieba.analyse.extract_tags(____, topK=____)


def extract_keywords_textrank(text: str, topk: int = 5) -> List[str]:
    """
    使用TextRank提取关键词
    
    提示：使用 jieba.analyse.textrank()
    """
    import jieba.analyse
    
    # TODO: 提取关键词
    return jieba.analyse.textrank(____, topK=____)


def texts_to_tfidf_matrix(texts: List[str], max_features: int = 100):
    """
    将文本列表转换为TF-IDF矩阵
    
    返回：(tfidf_matrix, vectorizer)
    
    提示：使用 sklearn.feature_extraction.text.TfidfVectorizer
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    # TODO: 创建vectorizer并fit_transform
    vectorizer = TfidfVectorizer(max_features=____)
    tfidf_matrix = vectorizer.fit_transform(____)
    
    return tfidf_matrix, vectorizer


def compute_cosine_similarity(vec1, vec2) -> float:
    """
    计算余弦相似度
    
    提示：使用 sklearn.metrics.pairwise.cosine_similarity
    """
    from sklearn.metrics.pairwise import cosine_similarity
    
    # TODO: 计算相似度
    # 注意：cosine_similarity返回矩阵，需要取[0, 0]
    return float(cosine_similarity(____, ____)[0, 0])


def compute_edit_distance(text1: str, text2: str) -> float:
    """
    计算编辑距离相似度（0-1之间，1表示完全相同）
    
    提示：使用 difflib.SequenceMatcher
    """
    from difflib import SequenceMatcher
    
    # TODO: 计算相似度
    return SequenceMatcher(None, ____, ____).ratio()


def train_text_classifier(texts: List[str], labels: List[int]):
    """
    训练文本分类器
    
    流程：
    1. 分词（空格分隔）
    2. TF-IDF向量化
    3. 训练分类器（LogisticRegression）
    
    返回：(model, vectorizer)
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    
    # TODO: 创建vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(____)
    
    # TODO: 训练模型
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(____, ____)
    
    return model, vectorizer


def predict_text_category(text: str, model, vectorizer) -> int:
    """
    预测文本类别
    
    提示：先用vectorizer.transform()转换，再用model.predict()
    """
    # TODO: 转换并预测
    X = vectorizer.transform([____])
    return int(model.predict(____)[0])


def extract_amounts(text: str) -> List[float]:
    """
    从文本中提取金额
    
    示例：
        "金额：113.50元，税额：13.50元" -> [113.50, 13.50]
    
    提示：正则表达式 r"\d+(?:\.\d+)?"
    """
    # TODO: 使用正则提取
    matches = re.findall(r"____", text)
    return [float(m) for m in matches]


def extract_dates(text: str) -> List[str]:
    """
    从文本中提取日期（YYYY-MM-DD格式）
    
    示例：
        "开票日期：2024-03-15" -> ["2024-03-15"]
    
    提示：正则表达式 r"\d{4}-\d{2}-\d{2}"
    """
    # TODO: 使用正则提取
    return re.findall(r"____", text)


def extract_company_names(text: str) -> List[str]:
    """
    从文本中提取公司名称（简化版：以"公司"或"有限责任公司"结尾）
    
    示例：
        "购买方：北京科技有限公司" -> ["北京科技有限公司"]
    
    提示：正则表达式 r"[\u4e00-\u9fa5]+(?:有限责任公司|有限公司|公司)"
    """
    # TODO: 使用正则提取
    return re.findall(r"____", text)


# ========== 实战：发票描述分类 ==========

def invoice_description_classifier(train_data: List[Dict], test_texts: List[str]) -> List[str]:
    """
    发票商品描述分类
    
    输入训练数据示例：
    [
        {'description': '办公用品 A4纸', 'category': '办公用品'},
        {'description': '电子产品 笔记本电脑', 'category': '电子产品'},
        {'description': '办公桌椅', 'category': '办公用品'},
        ...
    ]
    
    流程：
    1. 中文分词
    2. 构建类别映射（category -> label_id）
    3. TF-IDF向量化
    4. 训练分类器
    5. 预测测试文本
    
    返回：预测的类别列表
    """
    import jieba
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    
    # 1. 提取训练数据
    descriptions = [d['description'] for d in train_data]
    categories = [d['category'] for d in train_data]
    
    # 2. 中文分词（空格分隔）
    tokenized_texts = [' '.join(jieba.lcut(text)) for text in descriptions]
    
    # 3. 构建类别映射
    unique_categories = sorted(set(categories))
    category_to_id = {cat: i for i, cat in enumerate(unique_categories)}
    id_to_category = {i: cat for cat, i in category_to_id.items()}
    
    # 转换标签
    y_train = [category_to_id[cat] for cat in categories]
    
    # 4. TF-IDF向量化
    vectorizer = TfidfVectorizer(max_features=500)
    X_train = vectorizer.fit_transform(____)  # TODO
    
    # 5. 训练分类器
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(____, ____)  # TODO
    
    # 6. 预测测试文本
    tokenized_test = [' '.join(jieba.lcut(text)) for text in test_texts]
    X_test = vectorizer.transform(____)  # TODO
    y_pred = model.predict(____)  # TODO
    
    # 7. 转换回类别名称
    predicted_categories = [id_to_category[label] for label in y_pred]
    
    return predicted_categories


def _run_self_tests():
    """自检"""
    try:
        import jieba
        
        # 测试1：分词
        tokens = tokenize_chinese("增值税专用发票")
        assert len(tokens) > 0, "分词结果为空"
        
        # 测试2：自定义词
        add_custom_word("增值税专用发票")
        tokens = tokenize_chinese("增值税专用发票")
        assert "增值税专用发票" in tokens, "自定义词未生效"
        
        # 测试3：停用词过滤
        filtered = remove_stopwords(["这是", "一张", "发票"], {"这是", "一张"})
        assert filtered == ["发票"], f"停用词过滤错误: {filtered}"
        
        # 测试4：关键词提取
        keywords = extract_keywords_tfidf("增值税专用发票是一种重要的税务凭证", topk=3)
        assert len(keywords) <= 3, "关键词数量错误"
        
        # 测试5：TF-IDF矩阵
        texts = ["文本一", "文本二", "文本三"]
        matrix, vectorizer = texts_to_tfidf_matrix(texts, max_features=10)
        assert matrix.shape[0] == 3, "TF-IDF矩阵行数错误"
        
        # 测试6：余弦相似度
        import numpy as np
        vec1 = np.array([[1, 0, 1]]).reshape(1, -1)
        vec2 = np.array([[1, 1, 0]]).reshape(1, -1)
        sim = compute_cosine_similarity(vec1, vec2)
        assert 0 <= sim <= 1, f"相似度应在[0,1]范围: {sim}"
        
        # 测试7：编辑距离
        ratio = compute_edit_distance("abc", "abd")
        assert 0 <= ratio <= 1, f"编辑距离相似度应在[0,1]范围: {ratio}"
        
        # 测试8：文本分类
        train_texts = ["好评 很好", "差评 很差", "好评 不错", "差评 糟糕"]
        train_labels = [1, 0, 1, 0]
        model, vectorizer = train_text_classifier(train_texts, train_labels)
        pred = predict_text_category("好评 推荐", model, vectorizer)
        assert pred in [0, 1], "预测标签错误"
        
        # 测试9：提取金额
        amounts = extract_amounts("金额：113.50元，税额：13.50元")
        assert len(amounts) == 2 and 113.50 in amounts, f"金额提取错误: {amounts}"
        
        # 测试10：提取日期
        dates = extract_dates("开票日期：2024-03-15")
        assert "2024-03-15" in dates, f"日期提取错误: {dates}"
        
        # 测试11：提取公司名
        companies = extract_company_names("购买方：北京科技有限公司")
        assert len(companies) > 0, "公司名提取失败"
        
        # 测试12：发票描述分类
        train_data = [
            {'description': '办公用品 A4纸', 'category': '办公用品'},
            {'description': '电子产品 笔记本电脑', 'category': '电子产品'},
            {'description': '办公桌椅', 'category': '办公用品'},
            {'description': '手机 智能手机', 'category': '电子产品'},
            {'description': '打印机', 'category': '办公用品'},
            {'description': '平板电脑', 'category': '电子产品'},
        ]
        test_texts = ['复印纸', '鼠标键盘']
        predictions = invoice_description_classifier(train_data, test_texts)
        assert len(predictions) == 2, "预测结果数量错误"
        assert all(p in ['办公用品', '电子产品'] for p in predictions), "预测类别错误"
        
        print("✅ NLP1 所有测试通过！")
        
    except ImportError as e:
        print(f"⚠️  缺少依赖: {e}")
        print("请安装: pip install jieba scikit-learn")
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        raise
    except Exception as e:
        print(f"❌ 错误: {e}")
        raise


if __name__ == "__main__":
    _run_self_tests()

