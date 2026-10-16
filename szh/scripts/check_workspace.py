"""Read-only OAPT_A plan checks; passing is not evidence of daily completion."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
import hashlib
import json
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent.parent
MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORD = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ERRORS: list[str] = []
SUPPORT = (
    "README.md", "AGENTS.md", "TASK.md", "algorithm/README.md",
    "docs/README.md", "docs/workflow.md", "docs/workspace-layout.md",
    "docs/templates/daily-record.md", "docs/Next-Session-Prompt.md",
    "docs/records/workspace-setup-2026-10-17.md",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def column_name(number: int) -> str:
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def cell_position(address: str) -> tuple[int, int]:
    match = re.fullmatch(r"([A-Z]+)([0-9]+)", address)
    if match is None:
        raise ValueError(f"Unsupported cell address: {address}")
    column = 0
    for letter in match.group(1):
        column = 26 * column + ord(letter) - 64
    return column, int(match.group(2))


def translate_shared(formula: str, origin: str, destination: str) -> str:
    """Expand A1 references in this workbook's shared formulas, preserving $ and strings."""
    source_column, source_row = cell_position(origin)
    target_column, target_row = cell_position(destination)
    token = re.compile(r"(?<![A-Za-z0-9_])([\$]?)([A-Z]{1,3})([\$]?)([0-9]+)(?![A-Za-z0-9_!(])")

    def shift(match: re.Match) -> str:
        absolute_column, letters, absolute_row, digits = match.groups()
        column, row = cell_position(letters + digits)
        if not absolute_column:
            column += target_column - source_column
        if not absolute_row:
            row += target_row - source_row
        if column < 1 or row < 1:
            raise ValueError("Shared formula produced an invalid reference")
        return absolute_column + column_name(column) + absolute_row + str(row)

    parts = re.split(r'("(?:[^\"]|\"\")*")', formula)
    return "".join(part if i % 2 else token.sub(shift, part) for i, part in enumerate(parts))


def local_path(raw: str, prefix: str) -> Path:
    """Require workspace-owned relative paths, including on Windows."""
    normalized = raw.replace("\\", "/")
    require(normalized.startswith(prefix), f"Path must start with {prefix}: {raw}")
    if ":" in normalized or normalized.startswith("/") or ".." in normalized.split("/"):
        raise ValueError(f"Unsafe planned path: {raw}")
    resolved = (ROOT / normalized).resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"Planned path escapes workspace: {raw}")
    return resolved


def source_section(fields: dict, failure: str) -> str:
    def escape(value: object) -> str:
        return (str(value).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace("|", "&#124;").replace("\n", "<br>"))

    lines = ["<!-- source-plan:start -->", "", "| 列 | 源计划字段 | 原值 |",
             "| --- | --- | --- |"]
    for index, (key, value) in enumerate(fields.items()):
        rendered = escape(value) if value != "" else "（空白）"
        lines.append(f"| {chr(65 + index)} | {escape(key)} | {rendered} |")
    lines.extend(("", "DOCX 对应日的失败处理（保留 Excel N 列原有空白）：", "",
                  "> " + failure, "", "<!-- source-plan:end -->"))
    return "\n".join(lines)


def check_links(path: Path) -> None:
    # Current entry documents only; historical files are not recursively linted.
    for match in re.finditer(r"(?<!!)\[[^\]]+\]\((<[^>]*>|[^)]+)\)", read_text(path)):
        target = match.group(1).strip().strip("<>")
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
            continue
        target = unquote(target.split("#", 1)[0])
        if target:
            require((path.parent / target).exists(),
                    f"Broken link in {path.relative_to(ROOT)}: {target}")


def check_structure(manifest: dict, selected: str | None, deliverables: bool) -> int:
    tasks = manifest["tasks"]
    require(manifest["schema_version"] == "1.0.0", "Unsupported manifest version")
    require([t["day"] for t in tasks] == list(range(1, 51)), "Expected ordered days 1..50")
    require([t["id"] for t in tasks] == [f"D{n:02}" for n in range(1, 51)],
            "Expected unique D01..D50 IDs")
    require(len(manifest["source_columns"]) == 14, "Expected 14 source columns A:N")
    require(manifest["workbook"]["overview_mapping"] ==
            dict(zip("BCDEFGHIJKLMN", "ABCDEFGHOPSTU")), "Unexpected overview mapping")
    require(manifest["workbook"]["gantt_columns"] == ["O", "BL"], "Unexpected Gantt columns")
    available = {p.name for p in (ROOT / "docs/tasks").glob("D*.md")}
    require(available == {f"D{n:02}.md" for n in range(1, 51)},
            "Daily plan files must be exactly D01.md..D50.md")
    index = read_text(ROOT / "TASK.md")
    count = 0
    for task in tasks:
        n = task["day"]
        task_id = task["id"]
        require(task["excel_row"] == n + 4 and task["overview_row"] == n + 5,
                f"{task_id}: wrong workbook row mapping")
        require(task["source_block"] == 116 + 12 * (n - 1), f"{task_id}: wrong DOCX block")
        require(task["plan"] == f"docs/tasks/{task_id}.md", f"{task_id}: unexpected plan path")
        fields = task["source_fields"]
        require(list(fields) == manifest["source_columns"], f"{task_id}: source column drift")
        values = list(fields.values())
        require(values[0] == n and values[3] == f"A:block-{task['source_block']}",
                f"{task_id}: source ID mismatch")
        blocks = task["source_docx_blocks"]
        require(len(blocks) == 12 and blocks[0] == values[4], f"{task_id}: DOCX excerpt mismatch")
        require(values[5] == "\n".join([blocks[0], *blocks[4:8]]),
                f"{task_id}: source operations mismatch")
        require(date.fromisoformat(values[1]).weekday() < 5, f"{task_id}: weekend plan date")
        require(task["evidence_pattern"] == f"records/{task_id}/<run-id>/",
                f"{task_id}: unexpected evidence path")
        for dependency in task["prerequisites"]:
            require(bool(re.fullmatch(r"D\d{2}", dependency)) and 1 <= int(dependency[1:]) < n,
                    f"{task_id}: invalid prerequisite {dependency}")
        paths = [(p, local_path(p, "algorithm/")) for p in task["deliverables"]]
        require(bool(paths), f"{task_id}: no deliverables")
        if task["test"]:
            local_path(task["test"], "algorithm/tests/")
        require(f"[{task_id}]({task['plan']})" in index, f"{task_id}: missing TASK index link")
        if selected and selected != task_id:
            continue
        count += 1
        path = local_path(task["plan"], "docs/tasks/")
        if not path.is_file():
            ERRORS.append(f"{task_id}: missing daily plan")
            continue
        content = read_text(path)
        expected = source_section(fields, blocks[-1])
        require(content.count("<!-- source-plan:start -->") == 1 and
                content.count("<!-- source-plan:end -->") == 1 and expected in content,
                f"{task_id}: source excerpt drift")
        for heading in ("开始入口与前置输入", "原始计划摘录", "本日实施步骤",
                        "交付路径与职责", "测试与验收", "证据、进度回填与交接"):
            require(f"## {heading}" in content, f"{task_id}: missing {heading}")
        require(all(f"\n{i}. " in content for i in range(1, 5)),
                f"{task_id}: fewer than four implementation steps")
        for raw, planned in paths:
            require(f"`{raw}`" in content, f"{task_id}: deliverable not in document: {raw}")
            if deliverables:
                nonempty = (planned.is_file() and planned.stat().st_size > 0) or (
                    planned.is_dir() and any(p.is_file() and p.stat().st_size > 0
                                             for p in planned.rglob("*")))
                require(nonempty, f"{task_id}: absent/empty planned deliverable: {raw}")
        if task["test"]:
            raw = task["test"]
            require(f"-p no:cacheprovider {raw} -q" in content,
                    f"{task_id}: behavior-test command missing")
            if deliverables:
                test_path = local_path(raw, "algorithm/tests/")
                require(test_path.is_file() and test_path.stat().st_size > 0,
                        f"{task_id}: absent/empty behavior test: {raw}")
        check_links(path)
    for name in SUPPORT:
        path = ROOT / name
        require(path.is_file(), f"Missing support document: {name}")
        if path.is_file():
            check_links(path)
    return count


def workbook_cells(path: Path, names: tuple[str, ...]) -> tuple[dict, date]:
    with zipfile.ZipFile(path) as archive:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rels = {r.attrib["Id"]: r.attrib["Target"] for r in relationships}
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in item.iter(f"{{{MAIN}}}t")) for item in root]
        properties = workbook.find(f"{{{MAIN}}}workbookPr")
        use_1904 = properties is not None and properties.get("date1904", "0") in ("1", "true")
        epoch = date(1904, 1, 1) if use_1904 else date(1899, 12, 30)
        result = {}
        for sheet in workbook.find(f"{{{MAIN}}}sheets"):
            name = sheet.attrib["name"]
            if name not in names:
                continue
            target = rels[sheet.attrib[f"{{{REL}}}id"]]
            xml_path = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
            xml = ET.fromstring(archive.read(xml_path))
            cells = {}
            shared_formulas = {}
            shared_followers = []
            for cell in xml.iter(f"{{{MAIN}}}c"):
                value_node = cell.find(f"{{{MAIN}}}v")
                raw = value_node.text if value_node is not None else None
                kind = cell.get("t")
                value: object = "" if raw is None else raw
                if kind == "s" and raw is not None:
                    value = shared[int(raw)]
                elif kind == "inlineStr":
                    value = "".join(t.text or "" for t in cell.iter(f"{{{MAIN}}}t"))
                elif raw is not None and kind in (None, "n"):
                    number = float(raw)
                    value = int(number) if number.is_integer() else number
                elif kind == "b" and raw is not None:
                    value = raw == "1"
                formula = cell.find(f"{{{MAIN}}}f")
                cells[cell.attrib["r"]] = (value, None if formula is None else formula.text)
                if formula is not None and formula.get("t") == "shared":
                    group = formula.attrib["si"]
                    if formula.text:
                        shared_formulas[group] = (cell.attrib["r"], formula.text)
                    else:
                        shared_followers.append((cell.attrib["r"], group))
            for address, group in shared_followers:
                origin, formula = shared_formulas[group]
                cells[address] = (cells[address][0], translate_shared(formula, origin, address))
            result[name] = cells
        return result, epoch


def check_sources(manifest: dict) -> None:
    source_base = ROOT.parent.parent.resolve()
    docx_blocks = None
    require({s["role"] for s in manifest["documents"]} == {"A", "B", "C", "unified"},
            "Expected four original DOCX sources")
    for source in manifest["documents"]:
        path = (ROOT / source["path"]).resolve()
        if path.parent != source_base or not path.name.startswith("OAPT_") or path.suffix != ".docx":
            raise ValueError(f"Unexpected source document path: {source['path']}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"],
                f"Source DOCX changed: {path.name}; review baseline before updating")
        if source["role"] == "A":
            with zipfile.ZipFile(path) as archive:
                body = ET.fromstring(archive.read("word/document.xml")).find(f"{{{WORD}}}body")
            blocks = ["".join(t.text or "" for t in child.iter(f"{{{WORD}}}t")).strip() for child in body]
            docx_blocks = [block for block in blocks if block]
    book = manifest["workbook"]
    path = (ROOT / book["path"]).resolve()
    if path.parent != ROOT.parent or not path.name.startswith("OAPT_") or path.suffix != ".xlsx":
        raise ValueError("Unexpected workbook source path")
    sheets, epoch = workbook_cells(path, (book["sheet"], book["overview_sheet"]))
    daily = sheets[book["sheet"]]
    overview = sheets[book["overview_sheet"]]
    for i, header in enumerate(manifest["source_columns"]):
        require(daily.get(f"{chr(65+i)}4", ("", None))[0] == header,
                f"Workbook source header changed: {chr(65+i)}4")
    for task in manifest["tasks"]:
        task_id = task["id"]
        row = task["excel_row"]
        for i, expected in enumerate(task["source_fields"].values()):
            address = f"{chr(65+i)}{row}"
            value, formula = daily.get(address, ("", None))
            if i in (1, 2) and isinstance(value, (int, float)):
                value = (epoch + timedelta(days=value)).isoformat()
            elif i in (1, 2) and isinstance(value, str) and "T" in value:
                value = datetime.fromisoformat(value).date().isoformat()
            require(value == expected and formula is None,
                    f"{task_id}: workbook source mismatch at {address}")
        overview_row = task["overview_row"]
        require(overview.get(f"A{overview_row}", ("", None))[1] == '"A"',
                f"{task_id}: overview owner formula mismatch")
        for target, source in book["overview_mapping"].items():
            address = f"{target}{overview_row}"
            formula = overview.get(address, ("", None))[1] or ""
            normalized = formula.lstrip("=").replace("'", "").replace("$", "")
            expected = f"{book['sheet']}!{source}{row}"
            require(normalized == expected, f"{task_id}: overview formula mismatch at {address}")
        for column in range(15, 65):
            label = column_name(column)
            address = f"{label}{overview_row}"
            formula = overview.get(address, ("", None))[1] or ""
            expected = (f'IF(AND($C{overview_row}<>"",$D{overview_row}<>"",'
                        f'{label}$4>=$C{overview_row},{label}$4<=$D{overview_row}),"■","")')
            require(formula == expected, f"{task_id}: Gantt formula mismatch at {address}")
        if docx_blocks is not None:
            start = task["source_block"] - 1
            require(docx_blocks[start:start+12] == task["source_docx_blocks"],
                    f"{task_id}: original DOCX block mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", help="Check one daily document, e.g. D01 or D1")
    parser.add_argument("--deliverables", action="store_true",
                        help="Require selected day's planned deliverables and test to be nonempty")
    parser.add_argument("--sources", action="store_true",
                        help="Read original DOCX/XLSX and compare source fields and A overview formulas")
    args = parser.parse_args()
    selected = None
    if args.day:
        match = re.fullmatch(r"D0?([1-9]|[1-4][0-9]|50)", args.day.upper())
        if not match:
            parser.error("--day must be D01..D50")
        selected = f"D{int(match.group(1)):02}"
    if args.deliverables and not selected:
        parser.error("--deliverables requires --day; existence is not proof of completion")
    try:
        manifest = json.loads(read_text(ROOT / "docs/tasks/manifest.json"))
        count = check_structure(manifest, selected, args.deliverables)
        if args.sources:
            check_sources(manifest)
    except (OSError, ValueError, KeyError, TypeError, IndexError, ET.ParseError, zipfile.BadZipFile) as exc:
        ERRORS.append(f"Cannot complete checks: {exc}")
        count = 0
    if ERRORS:
        for error in ERRORS[:20]:
            print("FAIL: " + error)
        if len(ERRORS) > 20:
            print(f"... {len(ERRORS) - 20} additional issue(s) omitted.")
        print(f"FAILED: {len(ERRORS)} issue(s); no files or progress were changed.")
        return 1
    print(f"PASS: {count} daily plan(s), 50-day manifest/index and current document links.")
    if args.sources:
        print("PASS: 4 original DOCX, 700 A:N values, 50 source blocks, 650 summary references, "
              "2500 Gantt formulas and 50 owner formulas.")
    if args.deliverables:
        print("PASS: planned deliverables/test exist and are nonempty; behavior was not tested.")
    print("Read-only check; no daily completion or Excel progress is asserted.")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
