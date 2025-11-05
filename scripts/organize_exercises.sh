#!/bin/bash
# 组织练习文件到分级目录

set -e

echo "🔧 开始组织练习文件..."

# 第1阶段：基础入门 (A, K)
echo "📁 创建第1阶段链接..."
for suffix in blank answers answers_annotated; do
  ln -sf ../../interview_exercises/set_A_${suffix}.py exercises/01_basics/set_A_${suffix}.py
  ln -sf ../../interview_exercises/set_K_${suffix}.py exercises/01_basics/set_K_${suffix}.py
done

# 第2阶段：数据处理 (B, G)
echo "📁 创建第2阶段链接..."
for suffix in blank answers answers_annotated; do
  ln -sf ../../interview_exercises/set_B_${suffix}.py exercises/02_data/set_B_${suffix}.py
  ln -sf ../../interview_exercises/set_G_${suffix}.py exercises/02_data/set_G_${suffix}.py
done

# 第3阶段：算法思维 (C, I, O)
echo "📁 创建第3阶段链接..."
for suffix in blank answers answers_annotated; do
  ln -sf ../../interview_exercises/set_C_${suffix}.py exercises/03_algorithm/set_C_${suffix}.py
  ln -sf ../../interview_exercises/set_I_${suffix}.py exercises/03_algorithm/set_I_${suffix}.py
  ln -sf ../../interview_exercises/set_O_${suffix}.py exercises/03_algorithm/set_O_${suffix}.py
done

# 第4阶段：并发编程 (D, H, T)
echo "📁 创建第4阶段链接..."
for suffix in blank answers answers_annotated; do
  ln -sf ../../interview_exercises/set_D_${suffix}.py exercises/04_concurrency/set_D_${suffix}.py
  ln -sf ../../interview_exercises/set_H_${suffix}.py exercises/04_concurrency/set_H_${suffix}.py
  ln -sf ../../interview_exercises/set_T_${suffix}.py exercises/04_concurrency/set_T_${suffix}.py
done

# 第5阶段：工程实践 (L, N, P, M)
echo "📁 创建第5阶段链接..."
for suffix in blank answers answers_annotated; do
  ln -sf ../../interview_exercises/set_L_${suffix}.py exercises/05_engineering/set_L_${suffix}.py
  ln -sf ../../interview_exercises/set_N_${suffix}.py exercises/05_engineering/set_N_${suffix}.py
  ln -sf ../../interview_exercises/set_P_${suffix}.py exercises/05_engineering/set_P_${suffix}.py
  ln -sf ../../interview_exercises/set_M_${suffix}.py exercises/05_engineering/set_M_${suffix}.py
done

# 第6阶段：业务应用 (E, J, F, Q)
echo "📁 创建第6阶段链接..."
for suffix in blank answers answers_annotated; do
  ln -sf ../../interview_exercises/set_E_${suffix}.py exercises/06_business/set_E_${suffix}.py
  ln -sf ../../interview_exercises/set_J_${suffix}.py exercises/06_business/set_J_${suffix}.py
  ln -sf ../../interview_exercises/set_F_${suffix}.py exercises/06_business/set_F_${suffix}.py
  ln -sf ../../interview_exercises/set_Q_${suffix}.py exercises/06_business/set_Q_${suffix}.py
done

# 第7阶段：系统设计 (R, S, U, V, W, X, Y)
echo "📁 创建第7阶段链接..."
for suffix in blank answers answers_annotated; do
  ln -sf ../../interview_exercises/set_R_${suffix}.py exercises/07_system/set_R_${suffix}.py
  ln -sf ../../interview_exercises/set_S_${suffix}.py exercises/07_system/set_S_${suffix}.py
  ln -sf ../../interview_exercises/set_U_${suffix}.py exercises/07_system/set_U_${suffix}.py
  ln -sf ../../interview_exercises/set_V_${suffix}.py exercises/07_system/set_V_${suffix}.py
  ln -sf ../../interview_exercises/set_W_${suffix}.py exercises/07_system/set_W_${suffix}.py
  ln -sf ../../interview_exercises/set_X_${suffix}.py exercises/07_system/set_X_${suffix}.py
  ln -sf ../../interview_exercises/set_Y_${suffix}.py exercises/07_system/set_Y_${suffix}.py
done

# 第8阶段：综合项目 (Z, AA, AB)
echo "📁 创建第8阶段链接..."
for suffix in blank answers answers_annotated; do
  ln -sf ../../interview_exercises/set_Z_${suffix}.py exercises/08_projects/set_Z_${suffix}.py
  ln -sf ../../interview_exercises/set_AA_${suffix}.py exercises/08_projects/set_AA_${suffix}.py
  ln -sf ../../interview_exercises/set_AB_${suffix}.py exercises/08_projects/set_AB_${suffix}.py
done

echo ""
echo "✅ 符号链接创建完成！"
echo ""
echo "📊 目录结构："
echo "  exercises/01_basics/     - $(ls exercises/01_basics/ 2>/dev/null | wc -l | tr -d ' ') 个文件"
echo "  exercises/02_data/       - $(ls exercises/02_data/ 2>/dev/null | wc -l | tr -d ' ') 个文件"
echo "  exercises/03_algorithm/  - $(ls exercises/03_algorithm/ 2>/dev/null | wc -l | tr -d ' ') 个文件"
echo "  exercises/04_concurrency/ - $(ls exercises/04_concurrency/ 2>/dev/null | wc -l | tr -d ' ') 个文件"
echo "  exercises/05_engineering/ - $(ls exercises/05_engineering/ 2>/dev/null | wc -l | tr -d ' ') 个文件"
echo "  exercises/06_business/   - $(ls exercises/06_business/ 2>/dev/null | wc -l | tr -d ' ') 个文件"
echo "  exercises/07_system/     - $(ls exercises/07_system/ 2>/dev/null | wc -l | tr -d ' ') 个文件"
echo "  exercises/08_projects/   - $(ls exercises/08_projects/ 2>/dev/null | wc -l | tr -d ' ') 个文件"
echo ""
echo "🎉 现在可以按阶段学习了！"
echo "   例如：cd exercises/01_basics && python set_A_blank.py"

