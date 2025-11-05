"""
AI专项套题 ML1（机器学习基础）- 空白版

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
    """
    类别编码：One-Hot编码
    
    示例：
        ['A', 'B', 'A', 'C'] -> [[1,0,0], [0,1,0], [1,0,0], [0,0,1]]
    
    提示：使用 sklearn.preprocessing.OneHotEncoder
    """
    from sklearn.preprocessing import OneHotEncoder
    
    enc = OneHotEncoder(sparse_output=False)
    # TODO: 将 values 转为二维数组，fit_transform
    values_2d = np.array(values).reshape(-1, 1)
    return enc.fit_transform(values_2d)


def encode_categorical_label(values: List[str]) -> np.ndarray:
    """
    类别编码：Label编码（转为整数）
    
    示例：
        ['high', 'low', 'medium', 'high'] -> [0, 1, 2, 0]
    
    提示：使用 sklearn.preprocessing.LabelEncoder
    """
    from sklearn.preprocessing import LabelEncoder
    
    enc = LabelEncoder()
    # TODO: fit_transform
    return ____


def normalize_standard(X: np.ndarray) -> np.ndarray:
    """
    标准化：(x - mean) / std
    
    提示：使用 sklearn.preprocessing.StandardScaler
    """
    from sklearn.preprocessing import StandardScaler
    
    scaler = StandardScaler()
    # TODO: fit_transform
    return ____


def normalize_minmax(X: np.ndarray, feature_range: Tuple[float, float] = (0, 1)) -> np.ndarray:
    """
    Min-Max归一化：缩放到指定范围
    
    提示：使用 sklearn.preprocessing.MinMaxScaler
    """
    from sklearn.preprocessing import MinMaxScaler
    
    scaler = MinMaxScaler(feature_range=____)
    return scaler.fit_transform(____)


def create_bins(values: List[float], n_bins: int = 5) -> np.ndarray:
    """
    数值分箱：将连续值分为n个区间
    
    示例：
        [1, 5, 10, 15, 20], n_bins=3 -> [0, 0, 1, 2, 2]
    
    提示：使用 pandas.cut 或 sklearn.preprocessing.KBinsDiscretizer
    """
    import pandas as pd
    
    # TODO: 使用 pd.cut，返回编码后的整数
    result = pd.cut(values, bins=____, labels=False)
    return result.values


def train_logistic_regression(X_train: np.ndarray, y_train: np.ndarray) -> object:
    """
    训练逻辑回归分类器
    
    提示：使用 sklearn.linear_model.LogisticRegression
    """
    from sklearn.linear_model import LogisticRegression
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    # TODO: fit
    model.fit(____, ____)
    return model


def train_random_forest(X_train: np.ndarray, y_train: np.ndarray, n_estimators: int = 100) -> object:
    """
    训练随机森林分类器
    
    提示：使用 sklearn.ensemble.RandomForestClassifier
    """
    from sklearn.ensemble import RandomForestClassifier
    
    model = RandomForestClassifier(n_estimators=____, random_state=42)
    model.fit(____, ____)
    return model


def evaluate_classifier(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    评估分类器：计算准确率、精确率、召回率、F1
    
    返回：{'accuracy': 0.85, 'precision': 0.80, 'recall': 0.90, 'f1': 0.85}
    
    提示：
    - accuracy_score
    - precision_recall_fscore_support (average='binary' 或 'weighted')
    """
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    
    accuracy = accuracy_score(____, ____)
    precision, recall, f1, _ = precision_recall_fscore_support(
        ____, ____, average='binary', zero_division=0
    )
    
    return {
        'accuracy': round(accuracy, 4),
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1': round(f1, 4),
    }


def compute_auc(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """
    计算AUC（Area Under ROC Curve）
    
    参数：
        y_true: 真实标签 (0/1)
        y_prob: 预测概率（正类的概率）
    
    提示：使用 sklearn.metrics.roc_auc_score
    """
    from sklearn.metrics import roc_auc_score
    
    # TODO: 计算AUC
    return round(roc_auc_score(____, ____), 4)


def cross_validate(X: np.ndarray, y: np.ndarray, model, cv: int = 5) -> Dict[str, float]:
    """
    交叉验证
    
    返回：{'mean_score': 0.85, 'std_score': 0.03}
    
    提示：使用 sklearn.model_selection.cross_val_score
    """
    from sklearn.model_selection import cross_val_score
    
    scores = cross_val_score(model, ____, ____, cv=____, scoring='accuracy')
    
    return {
        'mean_score': round(scores.mean(), 4),
        'std_score': round(scores.std(), 4),
    }


# ========== 实战：税务风险分类 ==========

def tax_risk_classification_pipeline(data: List[Dict]) -> Dict:
    """
    税务风险分类完整流程
    
    输入数据示例：
    [
        {'revenue': 1000000, 'tax_paid': 50000, 'industry': 'IT', 'risk': 0},
        {'revenue': 500000, 'tax_paid': 10000, 'industry': 'Manufacturing', 'risk': 1},
        ...
    ]
    
    流程：
    1. 特征工程：提取数值特征、编码类别特征
    2. 数据分割：train_test_split
    3. 特征归一化
    4. 训练模型
    5. 评估模型
    
    返回：{'model': model, 'metrics': {...}}
    """
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    
    # 1. 转为DataFrame
    df = pd.DataFrame(data)
    
    # 2. 特征工程
    # 数值特征：revenue, tax_paid
    # 派生特征：tax_rate = tax_paid / revenue
    df['tax_rate'] = df['tax_paid'] / df['revenue']
    
    # 类别特征编码
    le = LabelEncoder()
    df['industry_encoded'] = le.fit_transform(df['industry'])
    
    # 3. 准备X, y
    feature_cols = ['revenue', 'tax_paid', 'tax_rate', 'industry_encoded']
    X = df[feature_cols].values
    y = df['risk'].values
    
    # 4. 数据分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=____, random_state=42  # TODO: 填入测试集比例，通常0.2或0.3
    )
    
    # 5. 特征归一化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(____)  # TODO
    X_test_scaled = scaler.transform(____)  # TODO: 注意用transform而非fit_transform
    
    # 6. 训练模型
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(____, ____)  # TODO
    
    # 7. 预测与评估
    y_pred = model.predict(____)  # TODO
    
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
        
        # 测试1：One-Hot编码
        values = ['A', 'B', 'A', 'C']
        encoded = encode_categorical_onehot(values)
        assert encoded.shape == (4, 3), f"One-Hot shape错误: {encoded.shape}"
        
        # 测试2：Label编码
        labels = encode_categorical_label(['high', 'low', 'medium', 'high'])
        assert len(labels) == 4 and labels[0] == labels[3], "Label编码错误"
        
        # 测试3：标准化
        X = np.array([[1, 2], [3, 4], [5, 6]])
        X_scaled = normalize_standard(X)
        assert abs(X_scaled.mean()) < 0.01, "标准化均值应接近0"
        
        # 测试4：Min-Max归一化
        X_minmax = normalize_minmax(X, (0, 1))
        assert X_minmax.min() >= 0 and X_minmax.max() <= 1, "Min-Max范围错误"
        
        # 测试5：分箱
        bins = create_bins([1, 5, 10, 15, 20], n_bins=3)
        assert len(bins) == 5, "分箱数量错误"
        
        # 测试6：训练模型
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0, 0, 1, 1])
        model = train_logistic_regression(X_train, y_train)
        assert hasattr(model, 'predict'), "模型应有predict方法"
        
        # 测试7：评估
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([0, 1, 1, 1])
        metrics = evaluate_classifier(y_true, y_pred)
        assert 'accuracy' in metrics and 'f1' in metrics, "评估指标缺失"
        
        # 测试8：AUC
        y_prob = np.array([0.1, 0.4, 0.6, 0.9])
        auc = compute_auc(y_true, y_prob)
        assert 0 <= auc <= 1, f"AUC应在[0,1]范围: {auc}"
        
        # 测试9：交叉验证
        cv_result = cross_validate(X_train, y_train, RandomForestClassifier(random_state=42), cv=2)
        assert 'mean_score' in cv_result, "交叉验证结果缺失"
        
        # 测试10：完整流程
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

