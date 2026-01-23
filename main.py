import taipy.gui.builder as tgb
from taipy.gui import Gui
from src.pages import kurzschlusskraefte_page, root_page, on_menu_action

# Importiere das komplette Modul, damit Taipy die Variablen findet
from src.pages.kurzschlusskraefte import content_vorlage

with tgb.Page() as home_page:
    tgb.text(value="# Willkommen", mode="md")
    tgb.image(content="src/assets/Icon.jpg", width="10%")

pages = {
    "/": root_page,
    "Willkommen": home_page,
    "Kurzschlusskraefte": kurzschlusskraefte_page
}

if __name__ == "__main__":
    Gui(pages=pages, css_file="src/css/main.css").run(
        initial_page="Willkommen",
        #use_reloader=True,
        title="Kurzschlussfestigkeit", 
        favicon="src/assets/Icon.jpg",
        watermark="© Angelo Rusvai", 
        margin="2em", 
        dark_mode=False, 
        debug=True,
        #port="auto"
    )
