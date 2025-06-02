
from typing import List, Tuple
from docx.text.paragraph import Paragraph
from docx.document import Document
from docx.table import _Cell, Table
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.shared import RGBColor


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