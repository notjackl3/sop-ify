
from typing import List, Tuple
from docx.text.paragraph import Paragraph
from docx.document import Document
from docx.table import _Cell, Table
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.shared import RGBColor
from difflib import SequenceMatcher
from itertools import zip_longest


def iter_block_items(parent):
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            table = Table(child, parent)
            for row in table.rows:
                for cell in row.cells:
                    yield from iter_block_items(cell)
                    

def get_nested_attr(obj, attr_path):
    attrs = attr_path.split('.')
    for attr in attrs:
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    return obj


def extract_styles(paragraph):
    merged_runs = []
    last_style = None
    current_text = ""
    
    if paragraph:
        for run in paragraph.runs:
            style = {
                "bold": run.bold,
                "italic": run.italic,
                "underline": run.underline,
                "color": run.font.color.rgb if run.font.color else None,
                "size": run.font.size
            }

            if style == last_style:
                current_text += run.text
            else:
                if current_text:
                    merged_runs.append((current_text, last_style))
                current_text = run.text
                last_style = style

        if current_text:
            merged_runs.append((current_text, last_style))

    return merged_runs



def manage_space(prev_text, next_text):
    if not prev_text:
        return next_text or ""
    if not next_text:
        return prev_text
    if not prev_text.endswith(" ") and not next_text.startswith((" ", ".")):
        return prev_text + " " + next_text
    return prev_text + next_text


def identify_changes(old: List[Tuple], new: List[Tuple]) -> Tuple[List, List, List, List]:
    matched = []
    changed = []
    added = []
    deleted = []

    used_new_indices = set()
    used_old_indices = set()

    for i, old_item in enumerate(old):
        for j, new_item in enumerate(new):
            if j in used_new_indices:
                continue
            if old_item == new_item:
                matched.append(old_item)
                used_new_indices.add(j)
                used_old_indices.add(i)
                break

    for i, old_item in enumerate(old):
        if i in used_old_indices:
            continue
        for j, new_item in enumerate(new):
            if j in used_new_indices:
                continue
            if old_item[0] == new_item[0]:
                changed.append((old_item, new_item))
                used_new_indices.add(j)
                used_old_indices.add(i)
                break

    for i, old_item in enumerate(old):
        if i not in used_old_indices:
            deleted.append(old_item)

    for j, new_item in enumerate(new):
        if j not in used_new_indices:
            added.append(new_item)

    return matched, changed, added, deleted


def align_blocks(old_blocks, new_blocks):
    old_texts = [blk.text.strip() for blk in old_blocks]
    new_texts = [blk.text.strip() for blk in new_blocks]

    matcher = SequenceMatcher(None, old_texts, new_texts)
    aligned_pairs = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        for old_i, new_i in zip_longest(range(i1, i2), range(j1, j2)):
            old_blk = old_blocks[old_i] if old_i is not None and old_i < len(old_blocks) else None
            new_blk = new_blocks[new_i] if new_i is not None and new_i < len(new_blocks) else None
            aligned_pairs.append((old_blk, new_blk))

    return aligned_pairs


def split_and_style(text, style):
    if not text:
        return []
    sections = [x for x in text.split(" ") if x]
    return [(x, {k: v for k, v in style.items() if v}) for x in sections]