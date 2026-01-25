import taipy.gui.builder as tgb
from taipy.gui import navigate

def on_menu_action(state, id, payload):
    # payload['args'][0] typically contains the selected item ID for tgb.menu
    page_id = payload.get("args", [None])[0]
    if page_id:
        navigate(state, to=page_id)

menu_lov = [("Willkommen", "Willkommen"),
            ("Kurzschlusskraefte", "Kurzschlusskraefte")]
with tgb.Page() as root_page:
    tgb.toggle(theme=True, class_name="h1 text-center pb2")
    tgb.menu(label="Menu", lov=menu_lov, on_action=on_menu_action)
    tgb.content()


