from src.utils import dataloader
import taipy.gui.builder as tgb
from taipy.gui import navigate

def on_menu_action(state, id, payload):
    # payload['args'][0] typically contains the selected item ID for tgb.menu
    page_id = payload.get("args", [None])[0]
    if page_id:
        navigate(state, to=page_id)

menu_lov = [("Willkommen", "Willkommen"),
            ("Kurzschlusskraefte", "Kurzschlusskraefte")]

app_version = dataloader.get_app_version()

show_disclaimer = True

def accept_disclaimer(state):
    state.show_disclaimer = False

with tgb.Page() as root_page:
    with tgb.part(class_name="version-watermark"):
        tgb.text(f"Version {app_version}")
    tgb.toggle(theme=True, class_name="h1 text-center pb2")
    tgb.menu(label="Menu", lov=menu_lov, on_action=on_menu_action)
    with tgb.dialog(open="{show_disclaimer}", title="Haftungsausschluss / Disclaimer", on_action=accept_disclaimer):
        tgb.text(value="#### Wichtiger Hinweis", mode="md")
        tgb.text(value="Trotz sorgfältiger Programmierung und Tests dienen die Ergebnisse nur zur Information und Orientierung.", mode="md")
        tgb.text(value="**Keine Haftung:** Soweit gesetzlich zulässig (Art. 100 OR), wird jede Haftung für direkte "
                 "oder indirekte Schäden aus der Verwendung dieses Tools ausgeschlossen.", mode="md")
        tgb.text(value="**Prüfpflicht:** Die Ergebnisse müssen durch qualifiziertes Fachpersonal vor der "
                 "technischen Umsetzung verifiziert werden.", mode="md")
        tgb.html("br")
        tgb.button(label="Verstanden & akzeptiert", on_action=accept_disclaimer, class_name="fullwidth")
    tgb.content()



