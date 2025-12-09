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

#unit_properties = {"unit": "N", "display_unit": True}
unit_properties = dict(unit= "N", display_unit= True)

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
a_s: None|float = None
F_st_20: None|float = None
F_st_80: None|float = None
l: None|float = None
l_i: None|float = None

def on_clck_zürücksetzen(state):
    state.leiterseilbefestigung_selected = None
    state.standardkurzschlussströme_selected = 0.0 # muss float sein
    state.t_k = None
    state.leiterseiltyp_selected = None
    state.l = None
    state.l_i = None
    state.a = None
    state.teilleiter_selected = 0 # muss int sein
    state.a_s = None
    state.F_st_20 = None
    state.F_st_80 = None
    state.steifigkeitsnorm_selected = 0 # muss int sein

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
    # tgb.menu(label="Menu", lov=[("a", "Option A"), ("b", "Option B"), ("c", "Option C"), ("d", "Option D")], expanded = False)
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
            # 👇 Keep the original structure, just add a unique class
            tgb.number(label="Tk [s] Kurzschlussdauer", value="{t_k}", min=0.01, max=5.0, step=0.01,
                       class_name="input-with-unit tk-unit Mui-focused")

            # Leiterseilkonfiguration
            tgb.selector(label="Leiterseiltyp", value="{leiterseiltyp_selected}", lov="{leiterseiltyp_lov}",
                         dropdown=True, on_change=on_change_selectable)

            # 👇 Keep the original structure, use a different unique class for different unit
            tgb.number(label="l [m] Mittenabstand der Stützpunkte", value="{l}", min=0.0, max=100.0, step=0.1,
                       class_name="input-with-unit m-unit Mui-focused")
            tgb.number(label="l_i [m] Länge einer Abspann-Isolatorkette", value="{l_i}", min=0.0, max=10.0,
                       step=0.1, class_name="input-with-unit m-unit Mui-focused")
            tgb.number(label="a [m] Leitermittenabstand", value="{a}", min=0.0, max=20.0, step=0.1,
                       class_name="input-with-unit m-unit Mui-focused")
            tgb.selector(label="n (dimensionslos) Anzahl der Teilleiter eines Hauptleiters",
                         value="{teilleiter_selected}", lov="{teilleiter_lov}",
                         dropdown=True)
            # 👇 Keep the original structure, use a different unique class for different unit
            tgb.number(label="a_s [m] wirksamer Abstand zwischen Teilleitern", value="{a_s}", min=0.0, step=0.1,
                       class_name="input-with-unit m-unit Mui-focused")

            # Mechanischer Kraftwerte
            # 👇 Keep the original structure, use a different unique class for different unit
            tgb.number(label="Fst-20 [N] statische Seilzugkraft in einem Hauptleiter", value="{F_st_20}", min=0.0,
                       step=0.1, class_name="input-with-unit N-unit Mui-focused")
            tgb.number(label="Fst80 [N] statische Seilzugkraft in einem Hauptleiter", value="{F_st_80}", min=0.0,
                       step=0.1, class_name="input-with-unit N-unit Mui-focused")
            tgb.selector(label="N [1/N]Steifigkeitsnorm einer Anordnung mit Leiterseilen",
                         value="{steifigkeitsnorm_selected}", lov="{steifigkeitsnorm_lov}",
                         dropdown=True)
            tgb.html("br")
            with tgb.layout(columns="1 1", class_name="p1", columns__mobile="1 1"):
                tgb.button(label="Auswahl Leiterseiltyp aufheben", on_action=on_clck_btn)
                tgb.button(label="Zürücksetzen", on_action=on_clck_zürücksetzen)
    with tgb.layout(columns="1", class_name="p1", columns__mobile="1"):
        with tgb.expandable(title="Tabelle Leiterseiltypen", expanded=False):
            tgb.table("{leiterseiltyp}")

if __name__ == "__main__":
    Gui(page, css_file="main.css").run(use_reloader=True, title="Kurzschlussfestigkeit", watermark="© Angelo Rusvai", margin="2em", dark_mode=False, debug=True)
