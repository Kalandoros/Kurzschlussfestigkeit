import taipy.gui.builder as tgb
from taipy.gui import Gui
from src.pages import kurzschlusskraefte_page, root_page, on_menu_action


with tgb.Page() as home_page:
    tgb.text(value="# Willkommen", mode="md")
    tgb.image(content="src/assets/Icon.jpg", width="10%")

pages = {
    "/": root_page,
    "Willkommen": home_page,
    "Kurzschlusskraefte": kurzschlusskraefte_page
}

if __name__ == "__main__":
    Gui(pages=pages, css_file="main.css").run(
        initial_page="Willkommen",
        use_reloader=True, 
        title="Kurzschlussfestigkeit", 
        favicon="src/assets/Icon.jpg",
        watermark="© Angelo Rusvai", 
        margin="2em", 
        dark_mode=False, 
        debug=True

    )
