#!/bin/bash
# 验证项目改造是否成功

set -e

echo "🔍 验证项目改造..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
PASSED=0
FAILED=0

# 检查函数
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} 文件存在: $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} 文件缺失: $1"
        ((FAILED++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} 目录存在: $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} 目录缺失: $1"
        ((FAILED++))
    fi
}

check_symlink() {
    if [ -L "$1" ]; then
        echo -e "${GREEN}✓${NC} 符号链接存在: $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} 符号链接缺失: $1"
        ((FAILED++))
    fi
}

check_command() {
    if $1 > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} 命令可执行: $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} 命令失败: $2"
        ((FAILED++))
    fi
}

echo "📚 检查核心文档..."
check_file "README.md"
check_file "LEARNING_PATH.md"
check_file "QUICK_START.md"
check_file "FAQ.md"
check_file "KNOWLEDGE_MAP.md"
check_file "CHANGELOG.md"
check_file "PROJECT_SUMMARY.md"
check_file "GETTING_STARTED.md"
echo ""

echo "🛠️ 检查学习工具..."
check_file "learn.py"
check_file "progress.py"
check_file "Makefile"
echo ""

echo "📁 检查目录结构..."
check_dir "exercises"
check_dir "exercises/01_basics"
check_dir "exercises/02_data"
check_dir "exercises/03_algorithm"
check_dir "exercises/04_concurrency"
check_dir "exercises/05_engineering"
check_dir "exercises/06_business"
check_dir "exercises/07_system"
check_dir "exercises/08_projects"
check_file "exercises/README.md"
echo ""

echo "🔗 检查符号链接（抽样）..."
check_symlink "exercises/01_basics/set_A_blank.py"
check_symlink "exercises/01_basics/set_A_answers.py"
check_symlink "exercises/01_basics/set_A_answers_annotated.py"
check_symlink "exercises/02_data/set_B_blank.py"
check_symlink "exercises/08_projects/set_Z_blank.py"
echo ""

echo "📜 检查脚本..."
check_file "scripts/organize_exercises.sh"
check_file "scripts/verify_setup.sh"
echo ""

echo "🧪 检查工具可执行性..."
check_command "python3 learn.py --help" "learn.py --help"
check_command "python3 progress.py --show" "progress.py --show"
echo ""

echo "📊 检查原始文件完整性..."
check_dir "interview_exercises"
check_file "interview_exercises/set_A_blank.py"
check_file "interview_exercises/run_all.py"
echo ""

# 统计符号链接数量
echo "🔢 统计符号链接..."
SYMLINK_COUNT=$(find exercises -type l | wc -l | tr -d ' ')
echo -e "${YELLOW}ℹ${NC}  符号链接总数: $SYMLINK_COUNT (预期: 84)"
if [ "$SYMLINK_COUNT" -eq 84 ]; then
    echo -e "${GREEN}✓${NC} 符号链接数量正确"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} 符号链接数量不正确"
    ((FAILED++))
fi
echo ""

# 总结
echo "=" 
echo "📊 验证结果"
echo "="
echo ""
echo -e "通过: ${GREEN}$PASSED${NC}"
echo -e "失败: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有检查通过！项目改造成功！${NC}"
    echo ""
    echo "下一步："
    echo "  1. 运行 'make setup' 初始化项目"
    echo "  2. 运行 'make learn' 开始学习"
    echo "  3. 运行 'make progress' 查看进度"
    exit 0
else
    echo -e "${RED}❌ 有 $FAILED 项检查失败，请检查项目设置${NC}"
    exit 1
fi

