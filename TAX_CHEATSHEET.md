# 📊 财税知识速查卡

> 面试必备：个税、增值税、发票处理核心知识点

---

## 🧮 个人所得税（Individual Income Tax）

### 税率表（综合所得年度汇算）

| 级数 | 应纳税所得额（元） | 税率 | 速算扣除（元） |
|-----|------------------|------|--------------|
| 1 | 不超过 36,000 | 3% | 0 |
| 2 | 超过 36,000 至 144,000 | 10% | 2,520 |
| 3 | 超过 144,000 至 300,000 | 20% | 16,920 |
| 4 | 超过 300,000 至 420,000 | 25% | 31,920 |
| 5 | 超过 420,000 至 660,000 | 30% | 52,920 |
| 6 | 超过 660,000 至 960,000 | 35% | 85,920 |
| 7 | 超过 960,000 | 45% | 181,920 |

### 计算公式

```python
# 应纳税额 = 应纳税所得额 × 税率 - 速算扣除
def calc_iit(taxable: float) -> float:
    """个税计算"""
    brackets = [
        (36000, 0.03, 0),
        (144000, 0.10, 2520),
        (300000, 0.20, 16920),
        (420000, 0.25, 31920),
        (660000, 0.30, 52920),
        (960000, 0.35, 85920),
        (float('inf'), 0.45, 181920),
    ]
    for top, rate, quick in brackets:
        if taxable <= top:
            return round(taxable * rate - quick, 2)
    return 0.0
```

### 关键概念

- **应纳税所得额** = 收入 - 费用扣除（60,000/年）- 专项扣除 - 专项附加扣除
- **速算扣除** = 本级速算扣除 + (本级税率 - 上级税率) × 上级累计金额
- **边界值处理**：注意 `<=` 还是 `<`（通常用 `<=`）

### 常见陷阱

```python
# ❌ 错误1：忘记速算扣除
tax = taxable * 0.20  # 错误！

# ✅ 正确
tax = taxable * 0.20 - 16920

# ❌ 错误2：档位判断错误
if taxable > 36000:  # 应该用 <=
    ...

# ✅ 正确
if taxable <= 36000:
    tax = taxable * 0.03
elif taxable <= 144000:
    tax = taxable * 0.10 - 2520
```

---

## 💰 增值税（Value Added Tax, VAT）

### 税率表

| 类型 | 税率 | 适用范围 |
|------|------|---------|
| 基本税率 | 13% | 销售货物、加工修理修配劳务、有形动产租赁 |
| 低税率1 | 9% | 交通运输、邮政、建筑、不动产租赁、销售不动产 |
| 低税率2 | 6% | 现代服务、金融服务、生活服务、销售无形资产 |
| 简易征收 | 3% | 小规模纳税人 |
| 零税率 | 0% | 出口货物、国际运输服务 |

### 计算公式

#### 1. 含税金额 → 不含税金额 + 税额

```python
# 公式：不含税金额 = 含税金额 / (1 + 税率)
#      税额 = 含税金额 - 不含税金额

def split_vat(amount_with_tax: float, rate: float) -> tuple[float, float]:
    """拆分含税金额"""
    net = amount_with_tax / (1 + rate)
    tax = amount_with_tax - net
    return round(net, 2), round(tax, 2)

# 示例
amount = 113.0  # 含税金额
rate = 0.13     # 13% 税率
net, tax = split_vat(amount, rate)
# net = 100.0, tax = 13.0
```

#### 2. 不含税金额 → 含税金额

```python
# 公式：含税金额 = 不含税金额 × (1 + 税率)

def add_vat(net_amount: float, rate: float) -> float:
    """计算含税金额"""
    return round(net_amount * (1 + rate), 2)

# 示例
net = 100.0
rate = 0.13
amount = add_vat(net, rate)  # 113.0
```

#### 3. 应纳税额（销项税 - 进项税）

```python
def net_vat(invoices: list[dict]) -> float:
    """计算应纳增值税额"""
    net = 0.0
    for inv in invoices:
        amount = float(inv['amount'])  # 含税金额
        rate = float(inv['rate'])
        tax = amount - amount / (1 + rate)  # 税额
        
        if inv['type'] == 'sale':  # 销项
            net += tax
        else:  # 进项
            net -= tax
    
    return round(net, 2)
```

### 常见陷阱

```python
# ❌ 错误1：直接用含税金额乘税率
tax = amount * rate  # 错误！

# ✅ 正确：先换算成不含税
tax = amount - amount / (1 + rate)

# ❌ 错误2：公式记反
net = amount * (1 + rate)  # 错误！这是加税

# ✅ 正确：除以 (1 + rate)
net = amount / (1 + rate)

# ❌ 错误3：进项税忘记减
net_tax = sale_tax + purchase_tax  # 错误！

# ✅ 正确：销项 - 进项
net_tax = sale_tax - purchase_tax
```

---

## 🧾 发票处理

### 发票号码格式

```python
# 发票号码：8-12位数字
invoice_no_pattern = r"\d{8,12}"

# 示例
"12345678"      # 8位 ✓
"123456789012"  # 12位 ✓
"1234567"       # 7位 ✗
```

### 纳税人识别号（税号）

```python
# 税号：15-20位大写字母和数字
tax_no_pattern = r"[A-Z0-9]{15,20}"

# 示例
"91350100M0001XU43T"  # 18位 ✓
"123456789012345"     # 15位数字 ✓
```

### 统一社会信用代码

```python
# 18位大写字母和数字
usci_pattern = r"[0-9A-Z]{18}"

def is_valid_usci(code: str) -> bool:
    """校验统一社会信用代码"""
    return re.fullmatch(r"[0-9A-Z]{18}", code) is not None
```

### 发票文本解析

```python
import re

# 正则模式
LINE_RE = re.compile(
    r"发票号:(?P<no>\d{8,12})\s+"
    r"税号:(?P<taxno>[A-Z0-9]{15,20})\s+"
    r"金额:(?P<amt>\d+(?:\.\d+)?)"
)

def parse_invoice(text: str) -> dict | None:
    """解析发票文本"""
    m = LINE_RE.search(text)
    if not m:
        return None
    
    d = m.groupdict()
    d['amt'] = float(d['amt'])  # 转换金额
    return d

# 示例
text = "发票号:12345678 税号:91350100M0001XU43T 金额:113.00"
result = parse_invoice(text)
# {'no': '12345678', 'taxno': '91350100M0001XU43T', 'amt': 113.0}
```

---

## 🔐 数据合规

### 账号脱敏

```python
import re

def mask_account(text: str) -> str:
    """脱敏账号，保留末4位"""
    # 匹配 10-19 位连续数字
    return re.sub(
        r"(\d{6,15})(\d{4})",
        lambda m: "*" * len(m.group(1)) + m.group(2),
        text
    )

# 示例
mask_account("账号 6222021234567890")
# "账号 ************7890"
```

### Luhn 校验（银行卡/信用卡）

```python
def luhn_check(code: str) -> bool:
    """Luhn 校验算法"""
    s = 0
    alt = False
    for ch in reversed(code):
        if not ch.isdigit():
            return False
        d = ord(ch) - 48  # 转数字
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        s += d
        alt = not alt
    return s % 10 == 0

# 示例
luhn_check("79927398713")  # True
```

---

## 💵 高精度计算

### Decimal 使用

```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, localcontext

# 1. 基本使用
amount = Decimal("113.00")
rate = Decimal("0.13")
tax = amount * rate / (Decimal("1") + rate)

# 2. 四舍五入
with localcontext() as ctx:
    ctx.rounding = ROUND_HALF_UP  # 四舍五入
    result = tax.quantize(Decimal("0.00"))

# 3. 银行家舍入（.5 时舍入到最近的偶数）
with localcontext() as ctx:
    ctx.rounding = ROUND_HALF_EVEN
    result = tax.quantize(Decimal("0.00"))
```

### 舍入模式对比

```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

def compare_rounding(value: str) -> tuple[str, str]:
    """对比两种舍入方式"""
    d = Decimal(value)
    
    # 银行家舍入
    banker = d.quantize(Decimal("0.00"), rounding=ROUND_HALF_EVEN)
    
    # 四舍五入
    halfup = d.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    
    return str(banker), str(halfup)

# 示例
compare_rounding("2.125")  # ('2.12', '2.13')  # .5 舍到偶数
compare_rounding("2.135")  # ('2.14', '2.14')  # .5 舍到偶数
```

---

## 📅 日期处理

### 月末计算

```python
import pandas as pd

# 方法1：使用 MonthEnd
date = pd.to_datetime("2024-03-15")
month_end = date + pd.offsets.MonthEnd(0)  # 2024-03-31

# 方法2：下月初 - 1天
from datetime import datetime, timedelta
date = datetime(2024, 3, 15)
next_month = date.replace(day=1) + timedelta(days=32)
month_end = next_month.replace(day=1) - timedelta(days=1)
```

### 期间格式

```python
# YYYY-MM 格式
period = date.strftime("%Y-%m")  # "2024-03"

# pandas
df['period'] = pd.to_datetime(df['date']).dt.to_period('M')
```

---

## 🧪 测试用例

### 个税测试

```python
assert calc_iit(30000) == round(30000 * 0.03, 2)  # 900.0
assert calc_iit(200000) == round(200000 * 0.20 - 16920, 2)  # 23080.0
assert calc_iit(36000) == round(36000 * 0.03, 2)  # 边界值
assert calc_iit(36001) == round(36001 * 0.10 - 2520, 2)  # 边界值+1
```

### 增值税测试

```python
# 含税 113，税率 13%
net, tax = split_vat(113.0, 0.13)
assert net == 100.0
assert tax == 13.0

# 应纳税额
invoices = [
    {"type": "sale", "amount": 113, "rate": 0.13},     # 销项 13
    {"type": "purchase", "amount": 106, "rate": 0.06}, # 进项 6
]
assert net_vat(invoices) == round(13 - 6, 2)  # 7.0
```

---

**快速记忆口诀**：

- 个税：**档位找税率，别忘速算扣**
- 增值税：**含税要除，不含要乘，销减进得净**
- 发票：**号码数字，税号字母数字，金额带小数**
- 脱敏：**保留末四，其余星号**
- 精度：**Decimal 计算，quantize 舍入**

