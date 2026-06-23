# 🏆 数学建模全流程 Skill

> 从问题分析到论文生成的一站式数学建模竞赛工具箱

## 这是什么？

一套面向数学建模竞赛的完整工作流，覆盖：**问题分析 → 算法选型 → 代码求解 → 论文生成** 全流程。可作为 Claude Code Skill 使用，也可作为独立的 Python 代码库。

## 结构

```
math-modeling-skill/
│
├── skill.md                    ← Claude Code Skill 入口（全流程指南）
├── pyproject.toml              ← pip 安装配置
├── methodology/                ← 方法论文档（核心价值）
│   ├── AI协作心法.md           ← 人机协作哲学：沟通/安全/自检/Karpathy原则
│   ├── 分步工作流.md           ← 8阶段详细流程：每步谁做什么
│   ├── 写作心法.md             ← 论文写作规范：标题/摘要/模型格式/13节结构
│   └── 算法选型指南.md          ← 算法选择决策树+参数设定
│
├── src/math_modeling/          ← 论文生成框架（可pip install）
│   ├── __init__.py
│   ├── paper_generator.py      ← 参数化论文生成器（支持结果自动填入）
│   ├── formula_renderer.py     ← LaTeX → PNG 渲染
│   └── table_builder.py        ← 三线表构建器
│
├── examples/                   ← 示例代码（纯随机数据）
│   ├── config.py               ← 示例参数配置
│   ├── utils.py                ← 通用工具函数
│   ├── tsp_solver.py           ← Phase1: TSP(Held-Karp DP)
│   ├── vrptw_ga.py             ← Phase2: VRPTW(增强GA)
│   ├── nsga2.py                ← Phase3: NSGA-II+VNS
│   ├── layout_optimizer.py     ← Phase4: 两阶段布局优化
│   ├── main.py                 ← 全流程串联入口
│   ├── results/                ← 运行结果（自动生成，git忽略）
│   └── sample_output/          ← 示例论文（自动生成，git忽略）
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 这不是一套代码，这是一个方法论

这个项目与其他数学建模开源项目的区别：

**代码给你**：Phase1-4 的标准算法实现 + 论文生成框架
**方法论也给你**：怎么写论文（写作心法）、怎么选算法（选型指南）、**怎么和AI配合（协作心法）**

后者才是真正的价值——你学到的是完整的工作流，不是一段代码。

## 快速开始

### 一键运行（推荐）

```bash
pip install -r requirements.txt
python run_all.py
```

这一条命令自动完成：**安装依赖 → 模型求解 → 生成论文 → 汇总结果**。约1-2分钟。

### 分步运行

```bash
# 方式一：pip 安装（框架可作为 Python 包导入）
pip install -e .
# 之后可在任何地方：from math_modeling import PaperGenerator

# 方式二：直接安装依赖
pip install -r requirements.txt
```

```bash
# 1. 求解
cd examples && python main.py

# 2. 生成论文（自动检测并填入结果）
python ../src/math_modeling/paper_generator.py
```

### 接入自己的题目

1. 修改 `examples/config.py` 中的坐标、参数、任务数据
2. 运行 `python run_all.py`
3. 在 `PaperConfig` 中设置学校名、标题等信息

## 内含算法

| 阶段   | 算法                       | 适用场景        |
| ------ | -------------------------- | --------------- |
| Phase1 | Held-Karp DP / 最近邻      | 小规模TSP精确解 |
| Phase2 | GA + FFD装箱 + LPT + 2-opt | VRPTW/调度问题  |
| Phase3 | NSGA-II + VNS局部搜索      | 多目标优化      |
| Phase4 | 两阶段（TSP粗搜+GA精评）   | 布局/参数优化   |

## 安全声明

- 本项目**不包含**任何竞赛题目数据、学校内部模板或个人身份信息
- 所有示例数据纯随机生成，标注"仅用于演示"
- 用户使用时应替换为实际问题数据
- 遵守各竞赛的学术诚信规则

## 作为 Claude Code Skill 使用

将本仓库目录添加到 Claude Code 配置中：

```json
// .claude/settings.json
{
  "skills": {
    "math-modeling": "/path/to/math-modeling-skill"
  }
}
```

然后在对话中输入 `/math-modeling` 即可调用。

📖 **新手教程**：10 分钟上手 → Claude Code 技能调用 → 套用自己的赛题 → [TUTORIAL.md](TUTORIAL.md)

## License

AGPL-3.0

## 作者

AR-26710
