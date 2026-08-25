#!/usr/bin/env python3
"""Validate 蓝胖子 output workbooks with the Python standard library."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
HEADERS = {
    "专辑汇总": ["专辑ID", "专辑名称", "视频生成数量", "单条视频图片数量", "最终图片总量", "专辑统一风格"],
    "图片提示词明细": ["专辑ID", "专辑名称", "视频编号", "图片编号", "建议时长(秒)", "图片提示词"],
    "Sheet1任务汇总": ["任务ID", "任务名称", "任务模式", "生成数量", "海报总数", "统一风格说明"],
    "Sheet2商品海报提示词明细": ["任务ID", "任务名称", "海报编号", "是否带文字", "图片比例", "图片提示词"],
}


def col_index(ref: str) -> int:
    value = 0
    for char in re.match(r"[A-Z]+", ref).group(0):
        value = value * 26 + ord(char) - 64
    return value - 1


def read_xlsx(path: Path) -> dict[str, list[list[str]]]:
    with zipfile.ZipFile(path) as archive:
        strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            strings = ["".join(n.text or "" for n in item.iter(f"{{{MAIN}}}t")) for item in root]

        book = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {r.attrib["Id"]: r.attrib["Target"] for r in rels.findall(f"{{{PKG_REL}}}Relationship")}
        result: dict[str, list[list[str]]] = {}
        for sheet in book.find(f"{{{MAIN}}}sheets") or []:
            target = targets[sheet.attrib[f"{{{DOC_REL}}}id"]].lstrip("/")
            target = target if target.startswith("xl/") else str(PurePosixPath("xl") / target)
            root = ET.fromstring(archive.read(str(PurePosixPath(target))))
            rows: list[list[str]] = []
            for row in root.findall(f".//{{{MAIN}}}row"):
                cells: dict[int, str] = {}
                for cell in row.findall(f"{{{MAIN}}}c"):
                    kind = cell.attrib.get("t")
                    if kind == "inlineStr":
                        value = "".join(n.text or "" for n in cell.iter(f"{{{MAIN}}}t"))
                    else:
                        node = cell.find(f"{{{MAIN}}}v")
                        value = node.text if node is not None and node.text is not None else ""
                        if kind == "s" and value:
                            value = strings[int(value)]
                    cells[col_index(cell.attrib.get("r", "A1"))] = value
                rows.append([cells.get(i, "") for i in range(max(cells, default=-1) + 1)])
            result[sheet.attrib["name"]] = rows
        return result


def integer(value: str, label: str, errors: list[str]) -> int:
    try:
        return int(float(value))
    except ValueError:
        errors.append(f"{label} 应为整数，实际为 {value!r}")
        return 0


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        sheets = read_xlsx(path)
    except (OSError, KeyError, AttributeError, zipfile.BadZipFile, ET.ParseError) as exc:
        return [f"无法读取有效的 .xlsx 文件：{exc}"], []

    if not set(sheets) & set(HEADERS):
        return ["未找到任何蓝胖子固定输出 Sheet"], []
    for left, right in [("专辑汇总", "图片提示词明细"), ("Sheet1任务汇总", "Sheet2商品海报提示词明细")]:
        if (left in sheets) != (right in sheets):
            errors.append(f"{left} 与 {right} 必须成对出现")
    extras = set(sheets) - set(HEADERS)
    if extras:
        errors.append(f"存在不允许的额外 Sheet：{', '.join(sorted(extras))}")
    for name in set(sheets) & set(HEADERS):
        actual = (sheets[name][0] + [""] * 6)[:6] if sheets[name] else []
        if actual != HEADERS[name]:
            errors.append(f"{name} 表头错误：{actual}")

    if {"专辑汇总", "图片提示词明细"} <= set(sheets):
        summary = [r + [""] * 6 for r in sheets["专辑汇总"][1:] if any(r)]
        detail = [r + [""] * 6 for r in sheets["图片提示词明细"][1:] if any(r)]
        counts = Counter((r[0], r[1]) for r in detail)
        video_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
        for line, row in enumerate(detail, 2):
            video_counts[(row[0], row[1])][row[2]] += 1
            if not re.fullmatch(r"\d{2,}", row[2]) or not re.fullmatch(r"\d{2,}", row[3]):
                errors.append(f"图片提示词明细第 {line} 行编号必须是至少两位数字文本")
            try:
                if not 5 <= float(row[4]) <= 8:
                    warnings.append(f"图片提示词明细第 {line} 行建议时长不在 5–8 秒内")
            except ValueError:
                errors.append(f"图片提示词明细第 {line} 行建议时长无效")
            if not row[5].strip():
                errors.append(f"图片提示词明细第 {line} 行提示词为空")
            if re.search(r"同上|保持上一张|与前图一致|延续上一场|相同风格继续", row[5]):
                errors.append(f"图片提示词明细第 {line} 行不是独立完整提示词")
        for line, row in enumerate(summary, 2):
            key = (row[0], row[1])
            videos = integer(row[2], f"专辑汇总第 {line} 行视频生成数量", errors)
            images = integer(row[3], f"专辑汇总第 {line} 行单条视频图片数量", errors)
            total = integer(row[4], f"专辑汇总第 {line} 行最终图片总量", errors)
            if total != videos * images or counts[key] != total:
                errors.append(f"专辑 {row[0]!r} 的汇总数量与明细不一致")
            if len(video_counts[key]) != videos or any(n != images for n in video_counts[key].values()):
                errors.append(f"专辑 {row[0]!r} 的视频数或每条视频图片数不一致")

    if {"Sheet1任务汇总", "Sheet2商品海报提示词明细"} <= set(sheets):
        summary = [r + [""] * 6 for r in sheets["Sheet1任务汇总"][1:] if any(r)]
        detail = [r + [""] * 6 for r in sheets["Sheet2商品海报提示词明细"][1:] if any(r)]
        counts = Counter((r[0], r[1]) for r in detail)
        for line, row in enumerate(detail, 2):
            if not re.fullmatch(r"\d{2,}", row[2]):
                errors.append(f"商品海报明细第 {line} 行海报编号必须是至少两位数字文本")
            if row[3] not in {"是", "否"}:
                errors.append(f"商品海报明细第 {line} 行是否带文字只能是“是”或“否”")
            if row[4] not in {"9:16", "4:5", "1:1", "16:9"}:
                errors.append(f"商品海报明细第 {line} 行图片比例无效：{row[4]!r}")
            if not row[5].strip():
                errors.append(f"商品海报明细第 {line} 行提示词为空")
            if row[3] == "否" and "不得出现任何文字" not in row[5]:
                warnings.append(f"商品海报明细第 {line} 行未明确写入无文字约束")
            if row[3] == "是" and "严格逐字" not in row[5]:
                warnings.append(f"商品海报明细第 {line} 行未明确写入文案逐字准确约束")
        for line, row in enumerate(summary, 2):
            key = (row[0], row[1])
            count = integer(row[3], f"任务汇总第 {line} 行生成数量", errors)
            total = integer(row[4], f"任务汇总第 {line} 行海报总数", errors)
            if row[2] != "商品海报":
                errors.append(f"任务汇总第 {line} 行任务模式必须是“商品海报”")
            if total != count or counts[key] != total:
                errors.append(f"任务 {row[0]!r} 的汇总数量与明细不一致")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="校验蓝胖子生成的 Excel 固定结构")
    parser.add_argument("workbook", type=Path)
    args = parser.parse_args()
    errors, warnings = validate(args.workbook)
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    print(f"{'FAIL' if errors else 'PASS'}: {len(errors)} 个错误，{len(warnings)} 个警告")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
