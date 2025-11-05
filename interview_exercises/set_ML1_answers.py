"""
AI专项套题 ML1（机器学习基础）- 答案版

覆盖：
- 特征工程：编码、归一化、分箱
- 模型训练：分类器训练
- 模型评估：准确率、精确率、召回率、F1、AUC
- 实战：税务风险分类

依赖：pandas, numpy, scikit-learn
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import numpy as np


def encode_categorical_onehot(values: List[str]) -> np.ndarray:
    """类别编码：One-Hot编码"""
    from sklearn.preprocessing import OneHotEncoder
    
    enc = OneHotEncoder(sparse_output=False)
    values_2d = np.array(values).reshape(-1, 1)
    return enc.fit_transform(values_2d)


def encode_categorical_label(values: List[str]) -> np.ndarray:
    """类别编码：Label编码（转为整数）"""
    from sklearn.preprocessing import LabelEncoder
    
    enc = LabelEncoder()
    return enc.fit_transform(values)


def normalize_standard(X: np.ndarray) -> np.ndarray:
    """标准化：(x - mean) / std"""
    from sklearn.preprocessing import StandardScaler
    
    scaler = StandardScaler()
    return scaler.fit_transform(X)


def normalize_minmax(X: np.ndarray, feature_range: Tuple[float, float] = (0, 1)) -> np.ndarray:
    """Min-Max归一化：缩放到指定范围"""
    from sklearn.preprocessing import MinMaxScaler
    
    scaler = MinMaxScaler(feature_range=feature_range)
    return scaler.fit_transform(X)


def create_bins(values: List[float], n_bins: int = 5) -> np.ndarray:
    """数值分箱：将连续值分为n个区间"""
    import pandas as pd
    
    result = pd.cut(values, bins=n_bins, labels=False)
    return result.values


def train_logistic_regression(X_train: np.ndarray, y_train: np.ndarray) -> object:
    """训练逻辑回归分类器"""
    from sklearn.linear_model import LogisticRegression
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train: np.ndarray, y_train: np.ndarray, n_estimators: int = 100) -> object:
    """训练随机森林分类器"""
    from sklearn.ensemble import RandomForestClassifier
    
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_classifier(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """评估分类器：计算准确率、精确率、召回率、F1"""
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='binary', zero_division=0
    )
    
    return {
        'accuracy': round(accuracy, 4),
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1': round(f1, 4),
    }


def compute_auc(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """计算AUC（Area Under ROC Curve）"""
    from sklearn.metrics import roc_auc_score
    
    return round(roc_auc_score(y_true, y_prob), 4)


def cross_validate(X: np.ndarray, y: np.ndarray, model, cv: int = 5) -> Dict[str, float]:
    """交叉验证"""
    from sklearn.model_selection import cross_val_score
    
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    
    return {
        'mean_score': round(scores.mean(), 4),
        'std_score': round(scores.std(), 4),
    }


def tax_risk_classification_pipeline(data: List[Dict]) -> Dict:
    """税务风险分类完整流程"""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    
    df = pd.DataFrame(data)
    df['tax_rate'] = df['tax_paid'] / df['revenue']
    
    le = LabelEncoder()
    df['industry_encoded'] = le.fit_transform(df['industry'])
    
    feature_cols = ['revenue', 'tax_paid', 'tax_rate', 'industry_encoded']
    X = df[feature_cols].values
    y = df['risk'].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average='binary', zero_division=0
    )
    
    return {
        'model': model,
        'scaler': scaler,
        'label_encoder': le,
        'metrics': {
            'accuracy': round(accuracy, 4),
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1': round(f1, 4),
        }
    }


def _run_self_tests():
    """自检"""
    try:
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier
        
        values = ['A', 'B', 'A', 'C']
        encoded = encode_categorical_onehot(values)
        assert encoded.shape == (4, 3), f"One-Hot shape错误: {encoded.shape}"
        
        labels = encode_categorical_label(['high', 'low', 'medium', 'high'])
        assert len(labels) == 4 and labels[0] == labels[3], "Label编码错误"
        
        X = np.array([[1, 2], [3, 4], [5, 6]])
        X_scaled = normalize_standard(X)
        assert abs(X_scaled.mean()) < 0.01, "标准化均值应接近0"
        
        X_minmax = normalize_minmax(X, (0, 1))
        assert X_minmax.min() >= 0 and X_minmax.max() <= 1, "Min-Max范围错误"
        
        bins = create_bins([1, 5, 10, 15, 20], n_bins=3)
        assert len(bins) == 5, "分箱数量错误"
        
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0, 0, 1, 1])
        model = train_logistic_regression(X_train, y_train)
        assert hasattr(model, 'predict'), "模型应有predict方法"
        
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([0, 1, 1, 1])
        metrics = evaluate_classifier(y_true, y_pred)
        assert 'accuracy' in metrics and 'f1' in metrics, "评估指标缺失"
        
        y_prob = np.array([0.1, 0.4, 0.6, 0.9])
        auc = compute_auc(y_true, y_prob)
        assert 0 <= auc <= 1, f"AUC应在[0,1]范围: {auc}"
        
        cv_result = cross_validate(X_train, y_train, RandomForestClassifier(random_state=42), cv=2)
        assert 'mean_score' in cv_result, "交叉验证结果缺失"
        
        data = [
            {'revenue': 1000000, 'tax_paid': 50000, 'industry': 'IT', 'risk': 0},
            {'revenue': 500000, 'tax_paid': 10000, 'industry': 'Manufacturing', 'risk': 1},
            {'revenue': 2000000, 'tax_paid': 100000, 'industry': 'IT', 'risk': 0},
            {'revenue': 300000, 'tax_paid': 5000, 'industry': 'Retail', 'risk': 1},
            {'revenue': 1500000, 'tax_paid': 75000, 'industry': 'IT', 'risk': 0},
            {'revenue': 400000, 'tax_paid': 8000, 'industry': 'Manufacturing', 'risk': 1},
        ]
        result = tax_risk_classification_pipeline(data)
        assert 'model' in result and 'metrics' in result, "完整流程结果缺失"
        assert result['metrics']['accuracy'] > 0, "准确率应大于0"
        
        print("✅ ML1 所有测试通过！")
        
    except ImportError as e:
        print(f"⚠️  缺少依赖: {e}")
        print("请安装: pip install pandas numpy scikit-learn")
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        raise
    except Exception as e:
        print(f"❌ 错误: {e}")
        raise


if __name__ == "__main__":
    _run_self_tests()

