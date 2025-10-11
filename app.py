from taipy.gui import Gui, notify
import taipy.gui.builder as tgb
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.precision', 3)

from src import dataloader

leiterseilbefestigung_lov: list[str] = ["Abgespannt", "Aufgelegt"]
leiterseilbefestigung_selected: None|str = None

standardkurzschlussströme_lov: list[int|float] = [10, 12.5, 16, 20, 25, 31.5, 40, 50, 63, 80]
standardkurzschlussströme_selected: None|int|float = None

teilleiter_lov: list[int] = [1, 2, 3, 4, 5, 6]
teilleiter_selected: None|int = None

steifigkeitsnorm_lov: list[int] = [100000, 150000, 1300000, 400000, 2000000, 600000, 3000000]
steifigkeitsnorm_selected: None|int = None

"""
Auswahl der Leiterseiltypen: 
1. Gesamte Leiterseildaten als Dataframe, 
2. Selektierung der ersten Spalte mit "Bezeichnung" als List of values für das Dropdown, 
3. Parameter für das initiale Laden und die spätere Auswahl
"""
leiterseiltyp: pd.DataFrame = dataloader.load_csv_to_df()
leiterseiltyp_lov: list[str] = list(leiterseiltyp["Bezeichnung"])
leiterseiltyp_selected: None|str = None

t_k: None|float = None
a: None|float = None
F_st_20: None|float = None
F_st_80: None|float = None
l: None|float = None
l_i: None|float = None

def on_change_selectable(state):
    #state.leiterseiltyp_lov = list(state.leiterseiltyp.keys())
    state.leiterseiltyp = leiterseiltyp[leiterseiltyp["Bezeichnung"] == state.leiterseiltyp_selected]
    notify(state, notification_type="info", message=f'Leiterseiltyp auf {state.leiterseiltyp["Bezeichnung"].values[0]} geändert')
    #print(state.leiterseiltyp["Dauerstrombelastbarkeit"].values[0])
def on_clck_btn(state):
    state.leiterseiltyp = dataloader.load_csv_to_df()
    state.leiterseiltyp_selected = None
    #state.leiterseiltyp_lov = list(state.leiterseiltyp.keys())
    notify(state, notification_type="info", message="Auswahl aufgehoben")

with tgb.Page() as page:
    tgb.toggle(theme=True, class_name="h1 text-center pb2")
    tgb.text(value="Kurzschlussfestigkeit bei Leiterseilen", class_name="h1")
    with tgb.layout(columns="1 1", class_name="p1", columns__mobile="1 1"):
        with tgb.part(class_name="card"):
            # Rahmenwerte
            tgb.selector(label="Art der Leiterseilbefestigung", value="{leiterseilbefestigung_selected}",
                         lov="{leiterseilbefestigung_lov}", dropdown=True)
            tgb.selector(label="I''k [A] Anfangs-Kurzschlusswechselstrom beim dreipoligen Kurzschluss (Effektivwert)",
                         value="{standardkurzschlussströme_selected}", lov="{standardkurzschlussströme_lov}",
                         dropdown=True)
            tgb.number(label="Tk [s] Kurzschlussdauer", value="{t_k}", min=0.01, max=5.0, step=0.01)
            # Leiterseilkonfiguration
            tgb.selector(label="Leiterseiltyp", value="{leiterseiltyp_selected}", lov="{leiterseiltyp_lov}",
                         dropdown=True, on_change=on_change_selectable)
            tgb.number(label="l [m] Mittenabstand der Stützpunkte", value="{l}", min=0.0, max=100.0, step=0.1)
            tgb.number(label="li [m] Länge einer Abspann-Isolatorkette", value="{l_i}", min=0.0, max=10.0, step=0.1)
            tgb.number(label="a [m] Leitermittenabstand", value="{a}", min=0.0, max=20.0, step=0.1)
            tgb.selector(label="n (dimensionslos) Anzahl der Teilleiter eines Hauptleiters",
                         value="{teilleiter_selected}", lov="{teilleiter_lov}",
                         dropdown=True)
            tgb.number(label="a_s [m] wirksamer Abstand zwischen Teilleitern", value="{F_st_20}", min=0.0,
                       step=0.1)
            # Mechanischer Kraftwerte
            tgb.number(label="Fst-20 [N] statische Seilzugkraft in einem Hauptleiter", value="{F_st_20}", min=0.0,
                       step=0.1)
            tgb.number(label="Fst80 [N] statische Seilzugkraft in einem Hauptleiter", value="{F_st_80}", min=0.0,
                       step=0.1)
            tgb.selector(label="N [1/N]Steifigkeitsnorm einer Anordnung mit Leiterseilen",
                         value="{steifigkeitsnorm_selected}", lov="{steifigkeitsnorm_lov}",
                         dropdown=True)
            tgb.html("br")
            tgb.button(label="Auswahl aufheben", on_action=on_clck_btn)
    with tgb.layout(columns="1", class_name="p1", columns__mobile="1"):
        with tgb.expandable(title="Tabelle Leiterseiltypen", expanded=False):
            tgb.table("{leiterseiltyp}")

if __name__ == "__main__":
    Gui(page).run(use_reloader=True, title="Kurzschlussfestigkeit", watermark="© Angelo Rusvai", margin="2em", dark_mode=False, debug=True)
