import taipy.gui.builder as tgb

navbar_lov = [
    ("/Applikation", "Applikation"),
    ("/Dokumentation", "Dokumentation"),
]

def build_navbar() -> None:
    tgb.toggle(theme=True, class_name="h1 text-center pb2")
    tgb.navbar(lov=navbar_lov)

with tgb.Page() as kurzschlusskraefte_root_page:
    build_navbar()
    tgb.content()
