"""
AI专项套题 OCR1（OCR实战）- 空白版

覆盖：
- 图像预处理（灰度化、二值化、去噪、倾斜校正）
- OCR识别（PaddleOCR/Tesseract）
- 字段提取与校验
- 实战：发票批量识别

依赖：opencv-python, pillow, paddleocr（或 pytesseract）
注意：本套题可选依赖，如无OCR库则跳过相关测试
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import re


def preprocess_image_grayscale(img_array) -> 'np.ndarray':
    """
    图像灰度化
    
    参数：
        img_array: BGR格式的图像数组（cv2.imread的结果）
    
    返回：
        灰度图像数组
    
    提示：使用 cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    """
    import cv2
    
    # TODO: 转换为灰度图
    return cv2.cvtColor(____, cv2.COLOR_BGR2GRAY)


def preprocess_image_binary(gray_img, threshold: int = 127) -> 'np.ndarray':
    """
    图像二值化
    
    参数：
        gray_img: 灰度图像
        threshold: 阈值
    
    返回：
        二值化图像
    
    提示：使用 cv2.threshold()
    """
    import cv2
    
    # TODO: 二值化
    _, binary = cv2.threshold(____, ____, 255, cv2.THRESH_BINARY)
    return binary


def preprocess_image_denoise(gray_img) -> 'np.ndarray':
    """
    图像去噪
    
    提示：使用 cv2.fastNlMeansDenoising()
    """
    import cv2
    
    # TODO: 去噪
    return cv2.fastNlMeansDenoising(____)


def preprocess_image_resize(img, width: int = 800) -> 'np.ndarray':
    """
    图像缩放（保持宽高比）
    
    参数：
        img: 原始图像
        width: 目标宽度
    
    返回：
        缩放后的图像
    
    提示：
    1. 计算缩放比例：scale = width / img.shape[1]
    2. 使用 cv2.resize()
    """
    import cv2
    
    h, w = img.shape[:2]
    scale = width / w
    new_h = int(h * scale)
    
    # TODO: 缩放
    return cv2.resize(____, (____, ____), interpolation=cv2.INTER_AREA)


def ocr_with_paddleocr(img_path: str) -> List[Dict]:
    """
    使用PaddleOCR识别图像
    
    返回格式：
    [
        {'text': '发票号', 'confidence': 0.95, 'box': [[x1,y1], [x2,y2], ...]},
        ...
    ]
    
    提示：
    1. 初始化：ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    2. 识别：result = ocr.ocr(img_path, cls=True)
    3. 解析结果
    """
    try:
        from paddleocr import PaddleOCR
        
        # TODO: 初始化OCR
        ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
        
        # TODO: 识别
        result = ocr.ocr(____, cls=True)
        
        # 解析结果
        parsed = []
        if result and result[0]:
            for line in result[0]:
                parsed.append({
                    'text': line[1][0],
                    'confidence': line[1][1],
                    'box': line[0],
                })
        
        return parsed
        
    except ImportError:
        print("⚠️  PaddleOCR未安装，跳过此测试")
        return []


def ocr_with_tesseract(img_path: str) -> str:
    """
    使用Tesseract识别图像
    
    返回：识别的文本
    
    提示：
    1. 使用PIL打开图像
    2. pytesseract.image_to_string(img, lang='chi_sim')
    """
    try:
        import pytesseract
        from PIL import Image
        
        # TODO: 打开图像
        img = Image.open(____)
        
        # TODO: 识别
        text = pytesseract.image_to_string(____, lang='chi_sim')
        
        return text.strip()
        
    except ImportError:
        print("⚠️  Tesseract未安装，跳过此测试")
        return ""


def extract_invoice_number(text: str) -> Optional[str]:
    """
    从OCR文本中提取发票号码（8-12位数字）
    
    示例：
        "发票号码：12345678" -> "12345678"
    
    提示：正则表达式 r"发票号码?[:：]?\s*(\d{8,12})"
    """
    # TODO: 正则提取
    match = re.search(r"发票号码?[:：]?\s*(\d{8,12})", text)
    return match.group(1) if match else None


def extract_invoice_code(text: str) -> Optional[str]:
    """
    从OCR文本中提取发票代码（10-12位数字）
    
    示例：
        "发票代码：1234567890" -> "1234567890"
    
    提示：正则表达式 r"发票代码[:：]?\s*(\d{10,12})"
    """
    # TODO: 正则提取
    match = re.search(r"____", text)
    return match.group(1) if match else None


def extract_invoice_date(text: str) -> Optional[str]:
    """
    从OCR文本中提取开票日期
    
    示例：
        "开票日期：2024年03月15日" -> "2024-03-15"
        "开票日期：2024-03-15" -> "2024-03-15"
    
    提示：
    1. 先匹配 YYYY年MM月DD日 格式
    2. 再匹配 YYYY-MM-DD 格式
    """
    # TODO: 匹配中文格式
    match = re.search(r"开票日期[:：]?\s*(\d{4})年(\d{1,2})月(\d{1,2})日", text)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    # TODO: 匹配标准格式
    match = re.search(r"开票日期[:：]?\s*(\d{4}-\d{2}-\d{2})", text)
    return match.group(1) if match else None


def extract_invoice_amount(text: str) -> Optional[float]:
    """
    从OCR文本中提取金额（价税合计）
    
    示例：
        "价税合计：¥113.50" -> 113.50
        "合计金额：113.50元" -> 113.50
    
    提示：正则表达式 r"(?:价税合计|合计金额|金额)[:：]?\s*[¥￥]?\s*(\d+(?:\.\d+)?)"
    """
    # TODO: 正则提取
    match = re.search(r"____", text)
    return float(match.group(1)) if match else None


def correct_ocr_common_errors(text: str) -> str:
    """
    纠正OCR常见错误
    
    常见错误：
    - 数字0与字母O混淆
    - 数字1与字母I/l混淆
    - 全角标点转半角
    
    提示：使用字符串替换
    """
    # TODO: 纠正错误
    # 全角转半角
    text = text.replace("，", ",").replace("：", ":")
    
    # 在数字块中，O -> 0
    def fix_o_in_numbers(match):
        return match.group(0).replace('O', '0').replace('o', '0')
    
    text = re.sub(r"\d[\dOo\.]+", fix_o_in_numbers, text)
    
    return text


def validate_invoice_number(number: str) -> bool:
    """
    校验发票号码格式（8-12位数字）
    
    提示：正则表达式 r"^\d{8,12}$"
    """
    # TODO: 校验
    return bool(re.match(r"____", number))


def validate_invoice_code(code: str) -> bool:
    """
    校验发票代码格式（10-12位数字）
    
    提示：正则表达式 r"^\d{10,12}$"
    """
    # TODO: 校验
    return bool(re.match(r"^\d{10,12}$", code))


def validate_invoice_date(date: str) -> bool:
    """
    校验日期格式（YYYY-MM-DD）并检查合理性
    
    提示：
    1. 正则匹配格式
    2. 使用 datetime.strptime 验证日期有效性
    """
    import datetime
    
    # TODO: 格式校验
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return False
    
    # TODO: 日期有效性校验
    try:
        datetime.datetime.strptime(____, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ========== 实战：发票批量识别 ==========

def batch_invoice_ocr_pipeline(ocr_results: List[str]) -> List[Dict]:
    """
    发票批量识别流程（使用模拟的OCR文本结果）
    
    输入：OCR识别的文本列表
    输出：结构化的发票数据列表
    
    流程：
    1. 纠正OCR错误
    2. 提取字段（发票号、代码、日期、金额）
    3. 校验字段
    4. 返回结构化数据
    
    返回格式：
    [
        {
            'number': '12345678',
            'code': '1234567890',
            'date': '2024-03-15',
            'amount': 113.50,
            'valid': True,
            'errors': []
        },
        ...
    ]
    """
    results = []
    
    for text in ocr_results:
        # 1. 纠正错误
        corrected_text = correct_ocr_common_errors(text)
        
        # 2. 提取字段
        number = extract_invoice_number(corrected_text)
        code = extract_invoice_code(corrected_text)
        date = extract_invoice_date(corrected_text)
        amount = extract_invoice_amount(corrected_text)
        
        # 3. 校验
        errors = []
        if number and not validate_invoice_number(number):
            errors.append("发票号码格式错误")
        if code and not validate_invoice_code(code):
            errors.append("发票代码格式错误")
        if date and not validate_invoice_date(date):
            errors.append("日期格式错误")
        if amount is not None and amount <= 0:
            errors.append("金额必须大于0")
        
        # 4. 构建结果
        results.append({
            'number': number,
            'code': code,
            'date': date,
            'amount': amount,
            'valid': len(errors) == 0,
            'errors': errors,
        })
    
    return results


def _run_self_tests():
    """自检"""
    try:
        import numpy as np
        
        # 测试1：文本提取
        text1 = "发票号码：12345678 发票代码：1234567890 开票日期：2024年03月15日 价税合计：¥113.50"
        
        number = extract_invoice_number(text1)
        assert number == "12345678", f"发票号提取错误: {number}"
        
        code = extract_invoice_code(text1)
        assert code == "1234567890", f"发票代码提取错误: {code}"
        
        date = extract_invoice_date(text1)
        assert date == "2024-03-15", f"日期提取错误: {date}"
        
        amount = extract_invoice_amount(text1)
        assert amount == 113.50, f"金额提取错误: {amount}"
        
        # 测试2：OCR错误纠正
        text2 = "发票号：123456O8"  # O应该是0
        corrected = correct_ocr_common_errors(text2)
        assert "12345608" in corrected, f"OCR纠错失败: {corrected}"
        
        # 测试3：校验
        assert validate_invoice_number("12345678") == True
        assert validate_invoice_number("123") == False
        
        assert validate_invoice_code("1234567890") == True
        assert validate_invoice_code("123") == False
        
        assert validate_invoice_date("2024-03-15") == True
        assert validate_invoice_date("2024-13-01") == False
        
        # 测试4：批量处理
        ocr_texts = [
            "发票号码：12345678 发票代码：1234567890 开票日期：2024-03-15 金额：113.50",
            "发票号码：87654321 发票代码：0987654321 开票日期：2024-03-16 金额：226.00",
        ]
        results = batch_invoice_ocr_pipeline(ocr_texts)
        assert len(results) == 2, "批量处理结果数量错误"
        assert results[0]['valid'] == True, "第一张发票应该有效"
        assert results[0]['amount'] == 113.50, "金额错误"
        
        print("✅ OCR1 所有测试通过！")
        print("💡 提示：图像处理和OCR识别测试需要实际图像文件，已跳过")
        
    except ImportError as e:
        print(f"⚠️  缺少依赖: {e}")
        print("请安装: pip install opencv-python pillow")
        print("可选: pip install paddleocr 或 pip install pytesseract")
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        raise
    except Exception as e:
        print(f"❌ 错误: {e}")
        raise


if __name__ == "__main__":
    _run_self_tests()

