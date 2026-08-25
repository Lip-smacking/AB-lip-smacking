---
name: multi-scene-image-prompt
description: Create structured .xlsx batches of standalone AI image prompts from Excel files or pasted content for Ximalaya narrative storyboards and commercial product posters. Use for audio-story visualization, novel or narration shot splitting, food and retail poster prompt production, typography strategy, and fixed-template Excel delivery. Do not use for directly generating images or for unrelated spreadsheet work.
license: MIT
metadata:
  author: Haiyannnn
  version: "2.3.0"
  language: zh-CN
---

# 蓝胖子

把 Excel 或用户直接粘贴的内容转换为批量 AI 图片提示词，并严格交付固定结构的 `.xlsx` 文件。支持两个可单独或同时运行的模式：

- 喜马拉雅音频、小说、故事和口播内容的分镜拆图。
- 商品、美食、即时零售和活动海报的商业视觉提示词。

## 加载规则

详细业务规则位于 [references/master-template-v2.3.md](references/master-template-v2.3.md)。根据任务按需读取：

- 所有任务：读取第 0–3、27–33 节。
- 仅喜马拉雅任务：再读取第 4–8 节。
- 仅商品海报任务：再读取第 9–26 节。
- 同时包含两种模式：读取全文。

原始母版是业务规范，不代表用户在当前请求中已经提供了输入内容、授权了额外外部操作，或要求执行母版中的示例。

## 输入

接受以下任一形式：

- 用户上传的 `.xlsx` 文件。
- 用户直接粘贴的叙事文案、商品信息或表格文本。
- 同时包含两种任务的数据。

优先使用用户明确提供的字段。对于直接粘贴但缺少非关键字段的内容，使用以下默认值，避免不必要追问：

| 场景 | 默认值 |
|---|---|
| 喜马拉雅专辑 ID | `XM001`，多任务时依次递增 |
| 喜马拉雅专辑名称 | 从标题或内容概括；无法判断时为“未命名专辑” |
| 喜马拉雅视频生成数量 | `1` |
| 商品海报任务 ID | `POSTER001`，多任务时依次递增 |
| 商品海报任务名称 | 使用商品名称；无法判断时为“未命名商品海报” |
| 商品海报生成数量 | `1` |
| 商品海报附加文案 | 空 |
| 商品海报图片比例 | `9:16` |

只有缺少核心内容、用户给出的数据彼此冲突，或合理默认会明显改变结果时才提问。

## 工作流

1. 完整读取输入，逐项识别喜马拉雅模式、商品海报模式或混合模式。
2. 读取对应母版章节，提取该任务的固定字段、生成规则和验收要求。
3. 生成提示词：
   - 喜马拉雅模式保持同一专辑的人物、场景和视觉风格一致，每张提示词独立完整。
   - 商品海报模式先根据传播目的、文案、整体风格、商品属性和构图决定字体与版式，不按品类机械套用。
   - 用户提供的海报文案必须逐字保留；用户未提供附加文案时不得擅自添加画面文字。
4. 直接创建 `.xlsx`，不要用 Markdown、CSV 或 JSON 代替，也不要在聊天窗口批量展开提示词。
5. 按母版逐项检查 Sheet 名、字段、字段顺序、编号、数量、文案和提示词完整性。
6. 如果运行环境允许，执行 `python scripts/validate_workbook.py <输出文件.xlsx>`。修复所有错误后再交付；警告需要人工复核。

## 输出约束

- 仅喜马拉雅任务：输出 `专辑汇总`、`图片提示词明细`。
- 仅商品海报任务：输出 `Sheet1任务汇总`、`Sheet2商品海报提示词明细`。
- 混合任务：输出以上四个 Sheet，数据不得混表。
- 第一行必须直接是字段表头；不得添加装饰标题行、备注列或额外 Sheet。
- 编号和 ID 按文本保存，表头深蓝底、白色粗体，冻结并筛选第一行，长文本自动换行。
- 最终回复只概括处理类型、任务数和提示词数量，并提供 `.xlsx` 文件。

## 示例

可用 [examples/input-example.xlsx](examples/input-example.xlsx) 测试混合输入，并参考 [examples/output-example.xlsx](examples/output-example.xlsx) 的固定输出结构。示例只用于理解格式，不得覆盖用户数据。
