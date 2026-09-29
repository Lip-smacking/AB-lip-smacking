# 蓝胖子（dynamic-prompt-planner）

蓝胖子是一套动态提示词规划 Skill，可在 Codex、Claude Code、Cursor、WorkBuddy 和豆包工作中使用。它会先判断任务类型，再从 ICIO 模块中选择最精简、最高效的组合，把模糊想法整理成可直接复制使用的提示词。

## 能做什么

- 诊断商业、创意、技术、分析和复杂综合任务。
- 在人格魅力型、逻辑执行型、战略分析型、全能大师型框架中动态选择。
- 默认减少追问和框架术语，降低输入与理解成本。
- 支持快速生成，也支持逐步共建与教学。
- 使用标准 `SKILL.md` 结构，保留 Codex、Claude Code、Cursor 的使用方式，并新增 WorkBuddy、豆包工作说明。

## WorkBuddy 安装

1. [下载蓝胖子导入包 ZIP](https://raw.githubusercontent.com/Lip-smacking/AB-lip-smacking/main/downloads/dynamic-prompt-planner.zip)。
2. 在 WorkBuddy 打开「专家·技能·连接器 → 技能 → 添加技能 → 上传技能」，选择刚下载的 ZIP。
3. 导入并启用后，在对话中说：“使用蓝胖子，把下面的想法整理成可直接使用的提示词：……”

## 豆包工作使用

1. 下载上面的 [蓝胖子导入包 ZIP](https://raw.githubusercontent.com/Lip-smacking/AB-lip-smacking/main/downloads/dynamic-prompt-planner.zip)。
2. 在豆包工作的技能管理页查找「上传技能」入口，选择 ZIP 并启用；具体入口以当前客户端界面为准。
3. 在工作任务中说：“使用蓝胖子，把我的需求整理成一份可复制的提示词：……”

如果当前版本没有上传入口，可打开 [SKILL.md](SKILL.md)，将内容粘贴到新对话，再附上你的需求。这是单次使用；需要完整框架说明时，再附上 [ICIO 参考资料](references/icio-frameworks.md)。

## Codex、Claude Code、Cursor 安装

可用 Git 安装；选择对应平台执行：

Codex：

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.agents/skills/dynamic-prompt-planner
```

Claude Code：

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.claude/skills/dynamic-prompt-planner
```

Cursor：

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.cursor/skills/dynamic-prompt-planner
```

也可以在 GitHub 页面选择 **Code → Download ZIP**，解压后将文件夹重命名为 `dynamic-prompt-planner`，再放入对应平台的 skills 目录。

## 使用

WorkBuddy 或豆包工作：

```text
使用蓝胖子：帮我把这个产品创意整理成一份适合 AI 执行的提示词。
```

Codex：

```text
$dynamic-prompt-planner 把这个产品创意整理成一份适合 AI 执行的提示词。
```

Claude Code 或 Cursor：

```text
/dynamic-prompt-planner 帮我优化下面这份提示词，减少废话并补齐关键约束。
```

也可以直接说“帮我设计一份用于市场分析的提示词”。

## 目录

```text
.
├── SKILL.md
├── agents/openai.yaml
├── downloads/dynamic-prompt-planner.zip
└── references/icio-frameworks.md
```

## 作者与许可

作者：Haiyannnn（GitHub：[@Lip-smacking](https://github.com/Lip-smacking)）

本项目采用 [MIT License](LICENSE)。允许个人和商业使用、修改与再发布，但需保留版权和许可声明。
