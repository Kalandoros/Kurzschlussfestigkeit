from taipy.gui import Gui
import taipy.gui.builder as tgb

from src.pages import (kurzschlusskraefte_leiterseile_docu_page, kurzschlusskraefte_leiterseile_calc_page, on_menu_action, root_page)
from src.utils import third_party_integration as third_party

# Importiere das komplette Modul, damit Taipy die Variablen findet
from src.pages.kurzschlusskraefte import content_vorlage

with tgb.Page() as home_page:
    tgb.text(value="# Willkommen bei UWClac", mode="md")
    tgb.image(content="src/assets/Icon.jpg", width="10%")

pages = {
    "/": root_page,
    "Willkommen": home_page,
    "Kurzschlusskraefte": kurzschlusskraefte_leiterseile_calc_page,
    "Applikation": kurzschlusskraefte_leiterseile_calc_page,
    "Dokumentation": kurzschlusskraefte_leiterseile_docu_page,
}

if __name__ == "__main__":
    gui = Gui(pages=pages, css_file="src/css/main.css")
    gui.register_content_provider(third_party.MaTex, third_party.render_matex)
    gui.run(initial_page="Willkommen", #use_reloader=True,
            title="Kurzschlussfestigkeit", favicon="src/assets/Icon.jpg", watermark="© Angelo Rusvai",margin="2em",
            dark_mode=False, debug=True, port="auto")
