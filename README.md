# 蓝胖子（multi-scene-image-prompt）

把 Excel 或直接粘贴的文案批量转换为 AI 图片提示词，并输出固定结构的 `.xlsx` 文件。支持喜马拉雅叙事分镜和商品海报两种模式，兼容 Codex、Claude Code 与 Cursor。

## 功能

- 自动识别喜马拉雅、小说、故事、口播等叙事拆图任务。
- 自动识别商品、美食、即时零售和活动海报任务。
- 保持叙事人物、场景和风格一致。
- 根据传播目的和画面内容自动决定海报字体与版式。
- 支持 Excel 输入和直接粘贴内容。
- 输出固定 Sheet、字段、编号和格式的 `.xlsx`。
- 附带无第三方依赖的工作簿结构校验器和输入、输出示例。

## 安装

需要 Git。选择你使用的平台执行一条命令：

### Codex

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.agents/skills/multi-scene-image-prompt
```

### Claude Code

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.claude/skills/multi-scene-image-prompt
```

### Cursor

```bash
git clone https://github.com/Lip-smacking/AB-lip-smacking.git ~/.cursor/skills/multi-scene-image-prompt
```

如果平台没有立即显示新 Skill，请重新启动对应应用。更新已安装版本时，在安装目录运行 `git pull`。

也可以从 GitHub 下载 ZIP，解压后将目录重命名为 `multi-scene-image-prompt`，再放入上述平台对应的 skills 目录。

## 使用

Codex：

```text
$multi-scene-image-prompt 把这个 Excel 转成图片提示词文件
```

Claude Code 或 Cursor：

```text
/multi-scene-image-prompt 根据下面的商品信息生成 5 张海报提示词……
```

也可以直接用自然语言描述任务，让平台根据 Skill 的描述自动调用。

## 示例与校验

- `examples/input-example.xlsx`：同时包含喜马拉雅和商品海报的示例输入。
- `examples/output-example.xlsx`：四个固定 Sheet 的示例输出。

验证生成结果：

```bash
python3 scripts/validate_workbook.py examples/output-example.xlsx
```

校验器只使用 Python 标准库，检查固定 Sheet、表头、编号、数量、比例和关键提示词约束。

## 目录

```text
.
├── SKILL.md
├── agents/openai.yaml
├── references/master-template-v2.3.md
├── scripts/validate_workbook.py
└── examples/
    ├── input-example.xlsx
    └── output-example.xlsx
```

## 作者与许可

作者：Haiyannnn（GitHub：[@Lip-smacking](https://github.com/Lip-smacking)）

本项目采用 [MIT License](LICENSE)。允许个人和商业使用、修改与再发布，但需保留版权和许可声明。
