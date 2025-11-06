#!/bin/bash
# Web应用安全测试脚本

echo "============================================================"
echo "🔒 Web应用安全测试"
echo "============================================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Web应用是否运行
echo "1️⃣  检查Web应用状态..."
if curl -s http://localhost:8080/api/questions > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Web应用正在运行${NC}"
else
    echo -e "${RED}❌ Web应用未运行${NC}"
    echo ""
    echo "请先启动Web应用："
    echo "  cd web && python app.py"
    exit 1
fi

echo ""
echo "2️⃣  测试危险代码被阻止..."

# 测试1: 尝试导入os模块
echo -n "   测试: import os ... "
RESPONSE=$(curl -s -X POST http://localhost:8080/api/run \
    -H "Content-Type: application/json" \
    -d '{"code":"import os\nprint(os.getcwd())"}')

if echo "$RESPONSE" | grep -q '"success": false'; then
    echo -e "${GREEN}✅ 被阻止${NC}"
else
    echo -e "${RED}❌ 未被阻止！${NC}"
fi

# 测试2: 尝试使用eval
echo -n "   测试: eval() ... "
RESPONSE=$(curl -s -X POST http://localhost:8080/api/run \
    -H "Content-Type: application/json" \
    -d '{"code":"eval(\"1+1\")"}')

if echo "$RESPONSE" | grep -q '"success": false'; then
    echo -e "${GREEN}✅ 被阻止${NC}"
else
    echo -e "${RED}❌ 未被阻止！${NC}"
fi

# 测试3: 尝试打开文件
echo -n "   测试: open() ... "
RESPONSE=$(curl -s -X POST http://localhost:8080/api/run \
    -H "Content-Type: application/json" \
    -d '{"code":"open(\"/etc/passwd\")"}')

if echo "$RESPONSE" | grep -q '"success": false'; then
    echo -e "${GREEN}✅ 被阻止${NC}"
else
    echo -e "${RED}❌ 未被阻止！${NC}"
fi

echo ""
echo "3️⃣  测试安全代码正常执行..."

# 测试4: 正常的print
echo -n "   测试: print() ... "
RESPONSE=$(curl -s -X POST http://localhost:8080/api/run \
    -H "Content-Type: application/json" \
    -d '{"code":"print(\"Hello, World!\")"}')

if echo "$RESPONSE" | grep -q '"success": true'; then
    echo -e "${GREEN}✅ 正常执行${NC}"
else
    echo -e "${RED}❌ 执行失败${NC}"
fi

# 测试5: 数学运算
echo -n "   测试: 数学运算 ... "
RESPONSE=$(curl -s -X POST http://localhost:8080/api/run \
    -H "Content-Type: application/json" \
    -d '{"code":"import math\nprint(math.pi)"}')

if echo "$RESPONSE" | grep -q '"success": true'; then
    echo -e "${GREEN}✅ 正常执行${NC}"
else
    echo -e "${RED}❌ 执行失败${NC}"
fi

echo ""
echo "4️⃣  测试速率限制..."

# 快速发送多个请求
echo -n "   发送35个请求（限制30/分钟）... "
BLOCKED=0
for i in {1..35}; do
    RESPONSE=$(curl -s -X POST http://localhost:8080/api/run \
        -H "Content-Type: application/json" \
        -d '{"code":"print(1)"}')
    
    if echo "$RESPONSE" | grep -q '"rate_limit": true'; then
        BLOCKED=1
        break
    fi
done

if [ $BLOCKED -eq 1 ]; then
    echo -e "${GREEN}✅ 速率限制生效${NC}"
else
    echo -e "${YELLOW}⚠️  速率限制未触发（可能需要更多请求）${NC}"
fi

echo ""
echo "============================================================"
echo "✅ Web应用安全测试完成"
echo "============================================================"
echo ""
echo "详细安全说明："
echo "  - docs/SECURITY.md"
echo "  - docs/SECURITY_FIX_SUMMARY.md"
echo "  - web/security/README.md"
echo ""

