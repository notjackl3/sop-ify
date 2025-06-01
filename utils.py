
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


def extract_styles(block):
    styles = []
    for run in block.runs:
        text = run.text
        if not text.strip():
            continue
        STYLES_TO_CHECK = {
            "Bold": run.bold,
            "Italic": run.italic,
            "Underline": run.underline,
            "Color": run.font.color.rgb if run.font.color and run.font.color.rgb else RGBColor(0, 0, 0),
            "Size": run.font.size
        }
        styles.append((text, STYLES_TO_CHECK))
    return styles


def manage_space(prev_text, next_text):
    if not prev_text:
        return next_text or ""
    if not next_text:
        return prev_text
    if not prev_text.endswith(" ") and not next_text.startswith((" ", ".")):
        return prev_text + " " + next_text
    return prev_text + next_text
