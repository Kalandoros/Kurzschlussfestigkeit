from pathlib import Path

import markdown
import taipy.gui.builder as tgb

from src.utils import dataloader

from .root import build_navbar

DOC_PATH = Path(__file__).with_name("documentation.md")

def escape_taipy_braces(text: str) -> str:
    return text.replace("{", "&#123;").replace("}", "&#125;")

# 2. Read the content safely
try:
    with open(DOC_PATH, "r", encoding="utf-8") as f:
        md_content = escape_taipy_braces(f.read())
except FileNotFoundError:
    md_content = escape_taipy_braces("### Error: README.md not found in the nested folder.")

with tgb.Page() as kurzschlusskraefte_doc_page:
    build_navbar()
    tgb.html("br")
    tgb.text(value="Kurzschlussfestigkeit bei Leiterseilen", class_name="h1")
    #tgb.html("hr")
    with tgb.layout(columns="2 1", class_name="p1", columns__mobile="2 1"):
        with tgb.part(class_name="card doc-card"):
            #tgb.html(None, _load_documentation())
            tgb.text(md_content, mode="md")

