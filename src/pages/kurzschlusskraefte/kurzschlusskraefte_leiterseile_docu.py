from pathlib import Path
import taipy.gui.builder as tgb
from .root import build_navbar
from ...utils import third_party_integration as third_party

DOC_PATH = Path(__file__).with_name("documentation.md")
raw_text = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.exists() else "## Error\nDatei nicht gefunden"

content = third_party.MaTex(raw_text)

with tgb.Page() as kurzschlusskraefte_leiterseile_docu_page:
    build_navbar()
    tgb.html("br")
    tgb.text(value="Kurzschlussfestigkeit bei Leiterseilen", class_name="h1")
    with tgb.layout(columns="1", class_name="p1"):
        with tgb.part(class_name="card doc-card"):
            tgb.part(class_name="card taipy-text third-party-iframe-taipy-style", content="{content}", height="990px")
