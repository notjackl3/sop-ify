from docx import Document
from docx.shared import Cm
from utils import iter_block_items,extract_styles, manage_space, identify_changes
from section import Section
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import difflib
from itertools import zip_longest
import time
from difflib import SequenceMatcher


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


# name, attribute
ATTRIBUTES_TO_CHECK = [
    ("bold", "bold"),
    ("italic", "italic"),
    ("underline", "underline"),
    ("font color", "font.color.rgb"),
    ("font size", "font.size")
]



while True:
    print("🟦 Refreshing: ")
    document = Document()
    old_document = Document("documents/How to Organise Weekly Knowledge Sharing Sessions.docx")
    new_document = Document("documents/How to Organise Weekly Knowledge Sharing Sessions copy.docx")

    old_content = [para.text for para in old_document.paragraphs if para.text != ""]
    new_content = [para.text for para in new_document.paragraphs if para.text != ""]

    diff = difflib.unified_diff(old_content, new_content)
    changes = []
    for line in diff:
        if line.startswith('-') and not line.startswith('---'):
            changes.append(f"🔴 Removed: {line[1:].strip()}")
        elif line.startswith('+') and not line.startswith('+++'):
            changes.append(f"🟢 Added: {line[1:].strip()}")

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
                for attr in change[1][1]:
                    if attr in change[0][1]:
                        new_attr = change[1][1][attr]
                        if change[0][1][attr] != change[1][1][attr]:
                            if (attr, change[1][1][attr]) in temp_change:
                                temp_change[(attr, new_attr)].append((change[0][0], change[0][1][attr]))
                            else:
                                temp_change[(attr, change[1][1][attr])] = [(change[0][0], change[0][1][attr])]
                    else:
                        if (attr, change[1][1][attr]) in temp_add:
                                temp_add[(attr, change[1][1][attr])].append((change[0][0]))
                        else:
                            temp_add[(attr, change[1][1][attr])] = [(change[0][0])]
            
            for attr, change in temp_change.items():
                changes.append(f"🟡 Changed [{attr[0]}] '{" ".join([x[0] for x in change])}': {change[0][1]} to {attr[1]}")

            for attr, add in temp_add.items():
                changes.append(f"🟡 Added [{attr[0]}] '{" ".join([x for x in add])}': {attr[1]}")

    for change in changes:
        print(change, "\n")


    time.sleep(10)
