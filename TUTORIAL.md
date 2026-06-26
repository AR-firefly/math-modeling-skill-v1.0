# 📖 新手教程

这套 skill 不是一个"代码库"——它是**方法论 + 代码 + 写作模板**的组合。本文档教你：

- 10 分钟快速体验
- 在 Claude Code 中调用 `/math-modeling` 技能
- 用自己的竞赛题跑完整流程
- 什么时候该读哪篇方法论文档

---

## 一、10 分钟快速体验

不用理解所有文件，先跑起来看看它能做什么。

```bash
# 1. 进入项目目录
cd math-modeling-skill-v1.0

# 2. 安装依赖
pip install -r requirements.txt

# 3. 一键运行（安装+求解+论文生成+汇总）
python run_all.py
```

约 1-2 分钟后你会看到：

- 终端输出：Phase1-4 的求解结果和指标
- `examples/results/` 目录：各阶段求解结果
- `examples/sample_output/` 目录：自动生成的示例论文

**这一步跑的是纯随机数据**，与任何竞赛题目无关。只是为了让你看到从"问题求解"到"论文生成"的全流程长什么样。

---

## 二、作为 Claude Code Skill 使用

### 2.1 配置

在 Claude Code 配置文件（`~/.claude/settings.json`）中添加：

```json
{
  "skills": {
    "math-modeling": "/path/to/math-modeling-skill-v1.0"
  }
}
```

把路径换成你机器上的实际路径，比如 Windows 下：

```json
{
  "skills": {
    "math-modeling": "C:\\Users\\YourName\\math-modeling-skill-v1.0"
  }
}
```

### 2.2 调用

在 Claude Code 对话中输入：

```
/math-modeling
```

Skill 加载后，Claude 会按照 skill.md 的 9 阶段流程与你协作：

```
Phase 0: 问题理解 → 先确认题目类型和规模
Phase 1: 头脑风暴 → AI 给 2-3 种技术路线
Phase 2: 制定计划 → 出详细计划，你审核
Phase 3: 资源调查 → 检查已有代码/技能
Phase 4: 实现求解 → 按 examples/ 模板写代码
Phase 5: 简化优化 → 审查代码质量
Phase 6: 验证确认 → 跑真实数据看输出
Phase 7: 论文生成 → 配置 PaperConfig → 生成论文
Phase 8: 自评验收 → 对照写作心法检查
```

**关键点：** 这不是 AI 全程自动跑——每个阶段需要你审核确认。Phase 0-2 是聊天讨论阶段，Phase 4 之后才是写代码阶段。

### 2.3 用 skill 跑示例

进入 Claude Code 后：

```
/math-modeling

我想先跑一遍示例数据，看看流程怎么走。
```

Claude 会引导你走一遍完整流程。熟悉之后再换成自己的赛题。

---

## 三、套用自己的竞赛题

这是你拿到一套新赛题后的标准操作流程：

### Step 1：读题和分类

用 /math-modeling 的 Phase 0-1，先和 AI 讨论：

- 这是哪种题型？优化/预测/评价/图论？
- 数据规模多大？有哪些约束条件？
- 读完 `methodology/算法选型指南.md`，看哪种算法适合

### Step 2：配置参数

打开 `examples/config.py`，把题目中的坐标、参数、任务数据填进去。文件里有注释说明每一行是干什么的。

### Step 3：调整算法（如需要）

`examples/` 下有 4 个阶段的示例算法。你可以：

- 直接复用（如果问题匹配）
- 替换成自己的算法（保持输入输出格式一致即可）
- 增减阶段（不是所有题目都需要 4 个阶段）

### Step 4：运行

```bash
cd examples && python main.py
```

运行结果会存到 `examples/results/`。

### Step 5：生成论文

配好 `PaperConfig`（学校名、标题等信息），然后：

```bash
python ../src/math_modeling/paper_generator.py
```

生成的论文在 `examples/sample_output/`。

### Step 6：按写作规范审查

打开 `methodology/写作心法.md`，逐项检查论文质量：

- 摘要是不是"总分总"结构？
- 模型描述有没有公式和变量定义？
- 图表有没有引用说明？
- 结果有没有灵敏度分析？

---

## 四、方法论阅读路线图

4 篇方法论文档不要一次性读完——按阶段读：

| 当前阶段             | 该读什么                      | 为什么读                                           |
| -------------------- | ----------------------------- | -------------------------------------------------- |
| 第一次接触这套 skill | `methodology/AI协作心法.md`   | 理解人机怎么分工、安全边界在哪、怎么避免被 AI 带跑 |
| 准备开始解题         | `methodology/分步工作流.md`   | 知道 8 个阶段谁做什么、输入输出是什么              |
| 需要选算法           | `methodology/算法选型指南.md` | 决策树告诉你什么时候用遗传算法、什么时候用模拟退火 |
| 正在写论文           | `methodology/写作心法.md`     | 标题怎么写、摘要怎么搭、模型怎么描述——直接套模板   |

简单说：**协作心法先读（一次）、分步工作流做时翻（反复）、算法选型遇问题查（按需）、写作心法写完审（最终关）。**

---

## 五、FAQ

### Q：依赖装不上怎么办？

```bash
pip install -r requirements.txt
```

如果报错，检查 Python 版本 >= 3.9。如果是 Windows 上 numpy 装不上，试试：

```bash
pip install numpy --only-binary=:all:
```

### Q：跑出来的结果不对？

先用随机数据跑一遍确认环境正常。如果是用自己的数据，检查 `config.py` 里的参数是否正确。

### Q：我想用自己的算法替换示例代码？

可以。保持输入输出接口一致就行——`main.py` 会依次调用各阶段的 solver，每个 solver 读 config 写 results，互不依赖。你只需要改对应的 solver 文件。

### Q：这个 skill 适合美赛还是国赛？

都适合。美赛侧重模型创新和英文写作，国赛侧重求解精度和论文规范——方法论文档覆盖的是两者通用的部分。美赛用户额外注意 `methodology/写作心法.md` 里的摘要和结构规范。

### Q：怎么提交最终的论文？

`paper_generator.py` 生成的是 `.docx` 文件。直接提交即可。如果需要转 PDF，在 Word 里另存为 PDF，或使用工具转换。

---

📖 回到 [README](README.md)
