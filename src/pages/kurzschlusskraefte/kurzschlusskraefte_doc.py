from pathlib import Path
import taipy.gui.builder as tgb
from .root import build_navbar
from taipy.gui import Markdown

DOC_PATH = Path(__file__).with_name("documentation.md")

with open(DOC_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()
    #md_content = f.read().replace("{", " { ").replace("}", " } ")

with tgb.Page() as kurzschlusskraefte_doc_page:
    build_navbar()
    tgb.html("br")
    tgb.text(value="Kurzschlussfestigkeit bei Leiterseilen", class_name="h1")
    #tgb.html("hr")
    with tgb.layout(columns="2 1", class_name="p1", columns__mobile="2 1"):
        with tgb.part(class_name="card doc-card"):
            tgb.text(value="{md_content}", mode="md")

