"""
AI专项套题 NLP1（自然语言处理基础）- 答案版
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import re


def tokenize_chinese(text: str) -> List[str]:
    """中文分词"""
    import jieba
    return jieba.lcut(text)


def add_custom_word(word: str):
    """添加自定义词到jieba词典"""
    import jieba
    jieba.add_word(word)


def remove_stopwords(tokens: List[str], stopwords: set) -> List[str]:
    """去除停用词"""
    return [token for token in tokens if token not in stopwords]


def extract_keywords_tfidf(text: str, topk: int = 5) -> List[str]:
    """使用TF-IDF提取关键词"""
    import jieba.analyse
    return jieba.analyse.extract_tags(text, topK=topk)


def extract_keywords_textrank(text: str, topk: int = 5) -> List[str]:
    """使用TextRank提取关键词"""
    import jieba.analyse
    return jieba.analyse.textrank(text, topK=topk)


def texts_to_tfidf_matrix(texts: List[str], max_features: int = 100):
    """将文本列表转换为TF-IDF矩阵"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    return tfidf_matrix, vectorizer


def compute_cosine_similarity(vec1, vec2) -> float:
    """计算余弦相似度"""
    from sklearn.metrics.pairwise import cosine_similarity
    return float(cosine_similarity(vec1, vec2)[0, 0])


def compute_edit_distance(text1: str, text2: str) -> float:
    """计算编辑距离相似度"""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, text1, text2).ratio()


def train_text_classifier(texts: List[str], labels: List[int]):
    """训练文本分类器"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X, labels)
    
    return model, vectorizer


def predict_text_category(text: str, model, vectorizer) -> int:
    """预测文本类别"""
    X = vectorizer.transform([text])
    return int(model.predict(X)[0])


def extract_amounts(text: str) -> List[float]:
    """从文本中提取金额"""
    matches = re.findall(r"\d+(?:\.\d+)?", text)
    return [float(m) for m in matches]


def extract_dates(text: str) -> List[str]:
    """从文本中提取日期"""
    return re.findall(r"\d{4}-\d{2}-\d{2}", text)


def extract_company_names(text: str) -> List[str]:
    """从文本中提取公司名称"""
    return re.findall(r"[\u4e00-\u9fa5]+(?:有限责任公司|有限公司|公司)", text)


def invoice_description_classifier(train_data: List[Dict], test_texts: List[str]) -> List[str]:
    """发票商品描述分类"""
    import jieba
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    
    descriptions = [d['description'] for d in train_data]
    categories = [d['category'] for d in train_data]
    
    tokenized_texts = [' '.join(jieba.lcut(text)) for text in descriptions]
    
    unique_categories = sorted(set(categories))
    category_to_id = {cat: i for i, cat in enumerate(unique_categories)}
    id_to_category = {i: cat for cat, i in category_to_id.items()}
    
    y_train = [category_to_id[cat] for cat in categories]
    
    vectorizer = TfidfVectorizer(max_features=500)
    X_train = vectorizer.fit_transform(tokenized_texts)
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    
    tokenized_test = [' '.join(jieba.lcut(text)) for text in test_texts]
    X_test = vectorizer.transform(tokenized_test)
    y_pred = model.predict(X_test)
    
    predicted_categories = [id_to_category[label] for label in y_pred]
    
    return predicted_categories


def _run_self_tests():
    """自检"""
    try:
        import jieba
        
        tokens = tokenize_chinese("增值税专用发票")
        assert len(tokens) > 0, "分词结果为空"
        
        add_custom_word("增值税专用发票")
        tokens = tokenize_chinese("增值税专用发票")
        assert "增值税专用发票" in tokens, "自定义词未生效"
        
        filtered = remove_stopwords(["这是", "一张", "发票"], {"这是", "一张"})
        assert filtered == ["发票"], f"停用词过滤错误: {filtered}"
        
        keywords = extract_keywords_tfidf("增值税专用发票是一种重要的税务凭证", topk=3)
        assert len(keywords) <= 3, "关键词数量错误"
        
        texts = ["文本一", "文本二", "文本三"]
        matrix, vectorizer = texts_to_tfidf_matrix(texts, max_features=10)
        assert matrix.shape[0] == 3, "TF-IDF矩阵行数错误"
        
        import numpy as np
        vec1 = np.array([[1, 0, 1]]).reshape(1, -1)
        vec2 = np.array([[1, 1, 0]]).reshape(1, -1)
        sim = compute_cosine_similarity(vec1, vec2)
        assert 0 <= sim <= 1, f"相似度应在[0,1]范围: {sim}"
        
        ratio = compute_edit_distance("abc", "abd")
        assert 0 <= ratio <= 1, f"编辑距离相似度应在[0,1]范围: {ratio}"
        
        train_texts = ["好评 很好", "差评 很差", "好评 不错", "差评 糟糕"]
        train_labels = [1, 0, 1, 0]
        model, vectorizer = train_text_classifier(train_texts, train_labels)
        pred = predict_text_category("好评 推荐", model, vectorizer)
        assert pred in [0, 1], "预测标签错误"
        
        amounts = extract_amounts("金额：113.50元，税额：13.50元")
        assert len(amounts) == 2 and 113.50 in amounts, f"金额提取错误: {amounts}"
        
        dates = extract_dates("开票日期：2024-03-15")
        assert "2024-03-15" in dates, f"日期提取错误: {dates}"
        
        companies = extract_company_names("购买方：北京科技有限公司")
        assert len(companies) > 0, "公司名提取失败"
        
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

