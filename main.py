from docx import Document
from docx.shared import Cm
from utils import iter_block_items,extract_styles, manage_space
from section import Section
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import difflib
from itertools import zip_longest


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

for old_block, new_block in zip_longest(iter_block_items(old_document), iter_block_items(new_document)):
    print("\n")
    old_styling = extract_styles(old_block)
    new_styling = extract_styles(new_block)   
    old_section = ""
    new_section = "" 
    style_changes = []

    old_sections = []
    new_sections = []
    words_styling = []

    for (old_text, old_style), (new_text, new_style) in zip_longest(old_styling, new_styling, fillvalue=(None, None)):
        if old_text: 
            old_section = manage_space(old_section, old_text)
        if new_text:
            new_section = manage_space(new_section, new_text)
        print("old text: ", old_text)
        print("new text: ", new_text)

        if old_style != new_style:
            if (new_text and new_text in old_section) or (old_text and old_text in new_section):
                style_changes.append(((old_text, old_style), (new_text, new_style)))
        # right here the idea should be that you split the sentence into word by word then you manually check the styling for each and then combine them back together, nso that you have control over styling of each word. from the new version, spot the differences to calculate what are the differences
    if old_section == new_section:
        for old_version, new_version in style_changes:
            print(old_version)
            print(new_version)
            for attr in old_version[1]:
                old_temp = old_version[1][attr]
                new_temp = new_version[1][attr]
                if old_temp != new_temp:
                    if old_temp and new_temp:
                        changes.append(f"🟡 Changed {attr}: '{old_version[0].strip()}' [{old_version[1][attr]}] to '{new_version[0].strip()}' [{new_version[1][attr]}]")
                    elif old_temp:
                        changes.append(f"🟡 Removed {attr}: '{old_version[0].strip()}' [{old_version[1][attr]}]")
                    else:
                        changes.append(f"🟡 Added {attr}: '{new_version[0].strip()}' [{new_version[1][attr]}]")

    # print(f"old section: {old_section}")
    # print(f"new section: {new_section}")
    
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

