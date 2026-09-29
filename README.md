# 蓝胖子（dynamic-prompt-planner）

蓝胖子是一套动态提示词规划 Skill。它会先判断任务类型，再从 ICIO 模块中选择最精简、最高效的组合，把模糊想法整理成可直接复制使用的提示词。

## 能做什么

- 诊断商业、创意、技术、分析和复杂综合任务。
- 在人格魅力型、逻辑执行型、战略分析型、全能大师型框架中动态选择。
- 默认减少追问和框架术语，降低输入与理解成本。
- 支持快速生成，也支持逐步共建与教学。
- 兼容 Codex、Claude Code 和 Cursor。

## 安装

需要 Git。选择对应平台执行：

### Codex

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.agents/skills/dynamic-prompt-planner
```

### Claude Code

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.claude/skills/dynamic-prompt-planner
```

### Cursor

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.cursor/skills/dynamic-prompt-planner
```

也可以在 GitHub 页面选择 **Code → Download ZIP**，解压后将文件夹重命名为 `dynamic-prompt-planner`，再放入对应平台的 skills 目录。

## 使用

Codex：

```text
$dynamic-prompt-planner 把这个产品创意整理成一份适合 AI 执行的提示词。
```

Claude Code 或 Cursor：

```text
/dynamic-prompt-planner 帮我优化下面这份提示词，减少废话并补齐关键约束。
```

也可以直接说“帮我设计一份用于市场分析的提示词”，让平台根据 Skill 描述自动调用。

## 目录

```text
.
├── SKILL.md
├── agents/openai.yaml
└── references/icio-frameworks.md
```

## 作者与许可

作者：Haiyannnn（GitHub：[@Lip-smacking](https://github.com/Lip-smacking)）

本项目采用 [MIT License](LICENSE)。允许个人和商业使用、修改与再发布，但需保留版权和许可声明。
