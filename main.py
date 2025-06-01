from docx import Document
from docx.shared import Cm
from utils import iter_block_items, get_nested_attr
from section import Section
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import difflib


# name, attribute
ATTRIBUTES_TO_CHECK = [
    ("bold", "bold"),
    ("italic", "italic"),
    ("underline", "underline"),
    ("font color", "font.color.rgb"),
    ("font size", "font.size")
]


document = Document()

old_document = Document("documents/How to Organise Weekly Knowledge Sharing Sessions.docx")
new_document = Document("documents/How to Organise Weekly Knowledge Sharing Sessions2.docx")

old_content = [para.text for para in old_document.paragraphs if para.text != ""]
new_content = [para.text for para in new_document.paragraphs if para.text != ""]

diff = difflib.unified_diff(old_content, new_content)
changes = []
for line in diff:
    if line.startswith('-') and not line.startswith('---'):
        changes.append(f"🔴 Removed: {line[1:].strip()}")
    elif line.startswith('+') and not line.startswith('+++'):
        changes.append(f"🟢 Added: {line[1:].strip()}")

for old_block, new_block in zip(iter_block_items(old_document), iter_block_items(new_document)):    
    for old_run, new_run in zip(old_block.runs, new_block.runs):
        print(f"old section: {old_run.text}")
        print(f"new section: {new_run.text}")
        attr_changes = []
        if old_run.text == new_run.text: 
            for label, attr_path in ATTRIBUTES_TO_CHECK:
                old_attr = get_nested_attr(old_run, attr_path)
                new_attr = get_nested_attr(new_run, attr_path)
                if old_attr != new_attr:
                    attr_changes.append((label, new_run.text, old_attr, new_attr))
        
        for change in attr_changes:
            if change[2] and change[3]:
                changes.append(f"🟡 Changed [{change[0]}] {change[1]}: {change[2]} --> {change[3]}")
            elif change[3]:
                changes.append(f"🟡 Added [{change[0]}] {change[1]}: {change[3]}")
            else:
                changes.append(f"🟡 Removed [{change[0]}] {change[1]}: {change[2]}")
    

for change in changes:
    print(change + "\n")

    # if block.style.name:
    #     print("Block style name:", block.style.name)  
    # for run in block.runs:
    #     if run.text:
    #         print("Text:", run.text)
    #     if run.bold:
    #         print("Bold:", run.bold)
    #     if run.italic:
    #         print("Italic:", run.italic)
    #     if run.underline:
    #         print("Underline:", run.underline)
    #     if run.font.color.rgb:
    #         rgb = run.font.color.rgb  # This is an RGBColor object
    #         hex_color = "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])
    #         print("Font color:", hex_color)
    #     if run.font.size:
    #         print("Font size:", run.font.size)  

# document.save('output.docx')

