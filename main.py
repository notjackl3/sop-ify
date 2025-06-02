from docx import Document
from docx.shared import Cm
from utils import iter_block_items,extract_styles, align_blocks, identify_changes
from section import Section
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import difflib
from itertools import zip_longest
import time


# name, attribute
ATTRIBUTES_TO_CHECK = [
    ("bold", "bold"),
    ("italic", "italic"),
    ("underline", "underline"),
    ("font color", "font.color.rgb"),
    ("font size", "font.size")
]

while True:
    print("⦿⦿⦿⦿⦿⦿⦿ Refreshing ⦿⦿⦿⦿⦿⦿⦿\n")
    document = Document()
    old_document = Document("documents/How to Organise Weekly Knowledge Sharing Sessions.docx")
    new_document = Document("documents/How to Organise Weekly Knowledge Sharing Sessions copy.docx")

    old_content = [para.text for para in old_document.paragraphs if para.text != ""]
    new_content = [para.text for para in new_document.paragraphs if para.text != ""]

    changes = []
    
    diff = difflib.unified_diff(old_content, new_content)
    prev = ""
    for line in diff:
        if line.startswith('-') and not line.startswith('---'):
            changes.append(f"🔴 Removed: {line[1:].strip()}")
        elif line.startswith('+') and not line.startswith('+++'):
            if prev and prev in line:
                changes[-1] = f"🔵 From: {prev}\n🔵 Updated to: {line[1:].strip()}"
            else:
                changes.append(f"🟢 Added: {line[1:].strip()}")
        prev = line[1:].strip()

    count = 0
    old_block_items = list(iter_block_items(old_document))
    new_block_items = list(iter_block_items(new_document))
    aligned_pairs = align_blocks(old_block_items, new_block_items)

    for idx, (old_block, new_block) in enumerate(aligned_pairs):
        old_styling = extract_styles(old_block)
        new_styling = extract_styles(new_block)   

        style_changes = []

        old_sections = []
        new_sections = []
        old_words_styling = []
        new_words_styling = []

        for (old_text, old_style), (new_text, new_style) in zip_longest(old_styling, new_styling, fillvalue=(None, None)):
            if old_text: 
                temp_sections = [x for x in old_text.split(" ") if x != ""]
                old_sections.extend(temp_sections)
                old_words_styling.extend([(x, {y: old_style[y] for y in old_style if old_style[y]}) for x in temp_sections])

            if new_text:
                temp_sections = [x for x in new_text.split(" ") if x != ""]
                new_sections.extend(temp_sections)
                new_words_styling.extend([(x, {y: new_style[y] for y in new_style if new_style[y]}) for x in temp_sections])

        matched, changed, added, deleted = identify_changes(old_words_styling, new_words_styling)
        
        if changed: 
            temp_change = {}
            temp_add = {}
            for change in changed:
                new_attrs = change[1][1]
                old_attrs = change[0][1]
                attr_name = change[0][0]

                for attr in new_attrs:
                    if attr in old_attrs:
                        new_attr = new_attrs[attr]
                        if old_attrs[attr] != new_attrs[attr]:
                            if (attr, new_attrs[attr]) in temp_change:
                                temp_change[(attr, new_attr)].append((attr_name, old_attrs[attr]))
                            else:
                                temp_change[(attr, new_attrs[attr])] = [(attr_name, old_attrs[attr])]
                    else:
                        if (attr, new_attrs[attr]) in temp_add:
                                temp_add[(attr, new_attrs[attr])].append((attr_name))
                        else:
                            temp_add[(attr, new_attrs[attr])] = [(attr_name)]

                for attr in old_attrs:
                    if attr not in new_attrs:
                        changes.append(f"🟡 Removed [{attr}]: '{change[0][0]}'")
            
            for attr, change in temp_change.items():
                changes.append(f"🟡 Changed [{attr[0]}]: '{" ".join([x[0] for x in change])}': {change[0][1]} to {attr[1]}")

            for attr, add in temp_add.items():
                if attr[1] is True:
                    changes.append(f"🟡 Added [{attr[0]}]: '{" ".join([x for x in add])}'")
                else:
                    changes.append(f"🟡 Added [{attr[0]}]: '{" ".join([x for x in add])}': {attr[1]}")

    for change in changes:
        print(change, "\n")

    time.sleep(10)
