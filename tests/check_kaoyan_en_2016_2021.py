#!/usr/bin/env python3
"""Validate the static English II reading pages added for 2016-2021."""

from html.parser import HTMLParser
from pathlib import Path
import re
from typing import List, Optional, Set, Tuple


ROOT = Path(__file__).resolve().parents[1]
YEARS = range(2016, 2022)


class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: List[str] = []
        self.question_numbers: List[int] = []
        self._classes: Set[str] = set()

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        self._classes = set((values.get("class") or "").split())

    def handle_data(self, data: str) -> None:
        if "q-stem" in self._classes:
            match = re.match(r"\s*(\d{2})\.", data)
            if match:
                self.question_numbers.append(int(match.group(1)))


def check_page(year: int) -> List[str]:
    path = ROOT / "doc" / f"kaoyan-en-{year}-reading.html"
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]

    source = path.read_text(encoding="utf-8")
    parser = StructureParser()
    parser.feed(source)
    errors: List[str] = []
    expected = list(range(21, 41))

    if f"<title>{year}年英语二阅读真题 · 精读原文</title>" not in source:
        errors.append(f"{year}: title/year mismatch")
    if any(parser.ids.count(anchor) != 1 for anchor in ("t1", "t2", "t3", "t4")):
        errors.append(f"{year}: anchors t1-t4 must each occur once")
    if len(parser.ids) != len(set(parser.ids)):
        errors.append(f"{year}: duplicate ids")
    if parser.question_numbers != expected:
        errors.append(f"{year}: questions are {parser.question_numbers}, expected 21-40")
    answer_blocks = re.findall(r'<div class="q-ans">(.*?)</div>', source, re.S)
    answer_numbers = [int(n) for block in answer_blocks for n in re.findall(r'</span>(\d{2})', block)]
    if answer_numbers != expected:
        errors.append(f"{year}: answer labels are {answer_numbers}, expected 21-40")
    if "本周" in source or "已完成" in source:
        errors.append(f"{year}: contains personal progress markers")
    return errors


def main() -> int:
    errors = [error for year in YEARS for error in check_page(year)]
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    for year in YEARS:
        href = f"doc/kaoyan-en-{year}-reading.html"
        if index.count(href) != 2:
            errors.append(f"index: {href} occurs {index.count(href)} times, expected 2")

    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        return 1
    print("PASS: 6 pages, 24 passages, 120 questions/answers, 12 index links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
