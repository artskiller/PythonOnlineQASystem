"""
AI专项套题 OCR1（OCR实战）- 答案版
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import re


def preprocess_image_grayscale(img_array) -> 'np.ndarray':
    """图像灰度化"""
    import cv2
    return cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)


def preprocess_image_binary(gray_img, threshold: int = 127) -> 'np.ndarray':
    """图像二值化"""
    import cv2
    _, binary = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)
    return binary


def preprocess_image_denoise(gray_img) -> 'np.ndarray':
    """图像去噪"""
    import cv2
    return cv2.fastNlMeansDenoising(gray_img)


def preprocess_image_resize(img, width: int = 800) -> 'np.ndarray':
    """图像缩放"""
    import cv2
    h, w = img.shape[:2]
    scale = width / w
    new_h = int(h * scale)
    return cv2.resize(img, (width, new_h), interpolation=cv2.INTER_AREA)


def ocr_with_paddleocr(img_path: str) -> List[Dict]:
    """使用PaddleOCR识别图像"""
    try:
        from paddleocr import PaddleOCR
        
        ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
        result = ocr.ocr(img_path, cls=True)
        
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
    """使用Tesseract识别图像"""
    try:
        import pytesseract
        from PIL import Image
        
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img, lang='chi_sim')
        
        return text.strip()
        
    except ImportError:
        print("⚠️  Tesseract未安装，跳过此测试")
        return ""


def extract_invoice_number(text: str) -> Optional[str]:
    """从OCR文本中提取发票号码"""
    match = re.search(r"发票号码?[:：]?\s*(\d{8,12})", text)
    return match.group(1) if match else None


def extract_invoice_code(text: str) -> Optional[str]:
    """从OCR文本中提取发票代码"""
    match = re.search(r"发票代码[:：]?\s*(\d{10,12})", text)
    return match.group(1) if match else None


def extract_invoice_date(text: str) -> Optional[str]:
    """从OCR文本中提取开票日期"""
    match = re.search(r"开票日期[:：]?\s*(\d{4})年(\d{1,2})月(\d{1,2})日", text)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    match = re.search(r"开票日期[:：]?\s*(\d{4}-\d{2}-\d{2})", text)
    return match.group(1) if match else None


def extract_invoice_amount(text: str) -> Optional[float]:
    """从OCR文本中提取金额"""
    match = re.search(r"(?:价税合计|合计金额|金额)[:：]?\s*[¥￥]?\s*(\d+(?:\.\d+)?)", text)
    return float(match.group(1)) if match else None


def correct_ocr_common_errors(text: str) -> str:
    """纠正OCR常见错误"""
    text = text.replace("，", ",").replace("：", ":")
    
    def fix_o_in_numbers(match):
        return match.group(0).replace('O', '0').replace('o', '0')
    
    text = re.sub(r"\d[\dOo\.]+", fix_o_in_numbers, text)
    
    return text


def validate_invoice_number(number: str) -> bool:
    """校验发票号码格式"""
    return bool(re.match(r"^\d{8,12}$", number))


def validate_invoice_code(code: str) -> bool:
    """校验发票代码格式"""
    return bool(re.match(r"^\d{10,12}$", code))


def validate_invoice_date(date: str) -> bool:
    """校验日期格式"""
    import datetime
    
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return False
    
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def batch_invoice_ocr_pipeline(ocr_results: List[str]) -> List[Dict]:
    """发票批量识别流程"""
    results = []
    
    for text in ocr_results:
        corrected_text = correct_ocr_common_errors(text)
        
        number = extract_invoice_number(corrected_text)
        code = extract_invoice_code(corrected_text)
        date = extract_invoice_date(corrected_text)
        amount = extract_invoice_amount(corrected_text)
        
        errors = []
        if number and not validate_invoice_number(number):
            errors.append("发票号码格式错误")
        if code and not validate_invoice_code(code):
            errors.append("发票代码格式错误")
        if date and not validate_invoice_date(date):
            errors.append("日期格式错误")
        if amount is not None and amount <= 0:
            errors.append("金额必须大于0")
        
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
        
        text1 = "发票号码：12345678 发票代码：1234567890 开票日期：2024年03月15日 价税合计：¥113.50"
        
        number = extract_invoice_number(text1)
        assert number == "12345678", f"发票号提取错误: {number}"
        
        code = extract_invoice_code(text1)
        assert code == "1234567890", f"发票代码提取错误: {code}"
        
        date = extract_invoice_date(text1)
        assert date == "2024-03-15", f"日期提取错误: {date}"
        
        amount = extract_invoice_amount(text1)
        assert amount == 113.50, f"金额提取错误: {amount}"
        
        text2 = "发票号：123456O8"
        corrected = correct_ocr_common_errors(text2)
        assert "12345608" in corrected, f"OCR纠错失败: {corrected}"
        
        assert validate_invoice_number("12345678") == True
        assert validate_invoice_number("123") == False
        
        assert validate_invoice_code("1234567890") == True
        assert validate_invoice_code("123") == False
        
        assert validate_invoice_date("2024-03-15") == True
        assert validate_invoice_date("2024-13-01") == False
        
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

