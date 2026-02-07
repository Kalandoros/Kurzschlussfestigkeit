import threading

from pandas import DataFrame
from sympy.core.numbers import NaN
from taipy.gui import notify, download
import taipy.gui.builder as tgb
import pandas as pd
from pathlib import Path
from datetime import datetime
import tempfile
import traceback
from src.utils import dataloader, helper
from src.engines.kurzschlusskraefte_leiterseile_engine import calculate_kurschlusskräfte_leiterseile_sweep_df
from .root import build_navbar
from src.engines.kurzschlusskraefte_leiterseile_engine import (
    KurschlusskräfteLeiterseileInput,
    KurschlusskräfteLeiterseileResult,
    calculate_kurschlusskräfte_leiterseile,
    CalculationCancelled,
)

# Configuration for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.precision', 3)
pd.options.display.float_format = '{:12.3e}'.format

leiterseilbefestigung_lov: list[str] = ["Abgespannt", "Aufgelegt", "Unterschlaufung", "Schlaufe am Spannfeldende"]
leiterseilbefestigung_selected: None|str = None

schlaufe_in_spannfeldmitte_lov: list[str] = ["Nein", "Ja"]
schlaufe_in_spannfeldmitte_selected: None|str = None

standardkurzschlussstroeme_lov: list[str] = ["10", "12.5", "16",  "20", "25", "31.5", "40", "50", "63", "80"]
standardkurzschlussstroeme_selected: None|str = None

frequenz_des_netzes_lov: list[str] = ["50", "16.66"]
frequenz_des_netzes_selected: None|str = None

hoehenunterschied_befestigungspunkte_lov: list[str] = ["Nein", "Ja"]
hoehenunterschied_befestigungspunkte_selected: None|str = None

schlaufenebene_parallel_senkrecht_lov: list[str] = ["Ebene senkrecht", "Ebene parallel"]
schlaufenebene_parallel_senkrecht_selected: None|str = None

temperatur_niedrig_lov: list[str] = ["-20", "-30", "-40", "-50"]
temperatur_niedrig_selected: None|str = None

temperatur_hoch_lov: list[str] = ["60", "70", "80", "90", "100"]
temperatur_hoch_selected: None|str = None

teilleiter_lov: list[str] = ["1", "2", "3", "4", "5", "6"]
teilleiter_selected: None|str = None

federkoeffizient_lov: list[str] = ["100000", "150000", "1300000", "400000", "500000", "2000000", "600000", "3000000"]
federkoeffizient_selected: None|str = None

"""
Auswahl der Leiterseiltypen: 
1. Gesamte Leiterseildaten als Dataframe, 
2. Selektierung der ersten Spalte mit "Bezeichnung" als List of values für das Dropdown, 
3. Parameter für das initiale Laden und die spätere Auswahl
"""
leiterseiltyp: pd.DataFrame = dataloader.load_csv_to_df()
leiterseiltyp_lov: list[str] = list(leiterseiltyp["Bezeichnung"])
leiterseiltyp_selected: None|str = None

name_der_verbindung: None|str = ""
kappa: None|float = None
t_k: None|float = None
f: None|float = None
m_c: None|float = None
l: None|float = None
l_i: None|float = None
l_h_f: None|float = None
a: None|float = None
a_s: None|float = None
F_st_20: None|float = None
F_st_80: None|float = None
l_s_1: None|float = None
l_s_2: None|float = None
l_s_3: None|float = None
l_s_4: None|float = None
l_s_5: None|float = None
l_s_6: None|float = None
l_s_7: None|float = None
l_s_8: None|float = None
l_s_9: None|float = None
l_s_10: None|float = None

content_vorlage: None|dict = None
vorlage_backup: None|dict = None

F_td_temp_niedrig: None|float|str = ""
F_fd_temp_niedrig: None|float|str = ""
F_pi_d_temp_niedrig: None|float|str = ""

F_td_temp_hoch: None|float|str = ""
F_fd_temp_hoch: None|float|str = ""
F_pi_d_temp_hoch: None|float|str = ""

F_td_massg: None|float|str = ""
F_fd_massg: None|float|str = ""
F_pi_d_massg: None|float|str = ""
temp_F_td_massg: None|float|str = ""
temp_F_fd_massg: None|float|str = ""
temp_F_pi_d_massg: None|float|str = ""

F_td_fd_pi_d_massg_1: None|float|str = ""
F_td_fd_pi_d_massg_2: None|float|str = ""

b_h_temp_niedrig: None|float|str = ""
b_h_temp_hoch: None|float|str = ""
b_h_max: None|float|str = ""
temp_b_h: None|float|str = ""

a_min_temp_niedrig: None|float|str = ""
a_min_temp_hoch: None|float|str = ""
a_min_min: None|float|str = ""

calc_result: None | KurschlusskräfteLeiterseileResult = None
calc_result_formatted: None|DataFrame = None
sweep_calc_df: None|DataFrame = None
sweep_vline_shapes: list = []

_calc_run_lock = threading.Lock()
_calc_run_id = 0
"""
Die folgenden zwei internen Funktionen sind dafür die Schleife zu der For-Loop zur Erstellung des Diagramms
zu unterbrechen falls wieder auf Berechnung gedrückt wurde. Damit soll sichergestellt werden, das nicht mehrere 
Schleifen parallel laufen und sich folgend gegenseitig überschreiben. 
Bei jedem klick zählt die Funktion _next_calc_run_id() eine neue ID aus und gibt diese zurück. 
Die Funktion _is_run_cancelled() überprüft ob die aktuelle ID noch gültig ist bzw. übereinstimmen. 
Wenn nicht wird die Berechnung der For-Loop zur Erstellung des Diagramms abgebrochen und die neue kann ihren job machen.
"""
def _next_calc_run_id():
    global _calc_run_id
    with _calc_run_lock:
        _calc_run_id += 1
        return _calc_run_id

def _is_run_cancelled(run_id):
    return run_id != _calc_run_id

# Funktion zu Berechnung des höchsten Punktes im Chart bei gegebenem x-Wert
def _build_vline_shapes(sweep_df, f_st_values) -> dict:
    if sweep_df is None or sweep_df.empty:
        return []
    if "F_st" not in sweep_df.columns:
        return []

    sweep_sorted = sweep_df.sort_values("F_st").reset_index(drop=True)
    f_st_series = sweep_sorted["F_st"]
    f_st_min = f_st_series.min()
    f_st_max = f_st_series.max()
    shapes = []

    for x_value in f_st_values:
        if x_value in (None, "", NaN):
            continue
        try:
            x_float = float(x_value)
        except (TypeError, ValueError):
            continue
        if x_float < f_st_min or x_float > f_st_max:
            continue

        if x_float == f_st_series.iloc[0]:
            row_low = row_high = sweep_sorted.iloc[0]
            x_low = x_high = f_st_series.iloc[0]
        elif x_float == f_st_series.iloc[-1]:
            row_low = row_high = sweep_sorted.iloc[-1]
            x_low = x_high = f_st_series.iloc[-1]
        else:
            idx_upper = f_st_series.searchsorted(x_float, side="left")
            if idx_upper <= 0 or idx_upper >= len(f_st_series):
                continue
            x_low = f_st_series.iloc[idx_upper - 1]
            x_high = f_st_series.iloc[idx_upper]
            row_low = sweep_sorted.iloc[idx_upper - 1]
            row_high = sweep_sorted.iloc[idx_upper]

        y_values = []
        for col in ["F_td", "F_fd", "F_pi_d"]:
            if x_low == x_high:
                y_val = row_low.get(col)
            else:
                y_low = row_low.get(col)
                y_high = row_high.get(col)
                if y_low in (None, "", NaN) or y_high in (None, "", NaN):
                    continue
                if pd.isna(y_low) or pd.isna(y_high):
                    continue
                y_val = y_low + (y_high - y_low) * ((x_float - x_low) / (x_high - x_low))
            if y_val in (None, "", NaN) or pd.isna(y_val):
                continue
            y_values.append(y_val)

        if not y_values:
            continue

        y_top = max(y_values)
        shapes.append({
            "type": "line",
            "xref": "x",
            "yref": "y",
            "x0": x_float,
            "x1": x_float,
            "y0": 0,
            "y1": y_top,
            "line": {"color": "#444444", "width": 1, "dash": "dot"},
        })
        shapes.append({
            "type": "line",
            "xref": "x",
            "yref": "y",
            "x0": 0,
            "x1": x_float,
            "y0": y_top,
            "y1": y_top,
            "line": {"color": "#444444", "width": 1, "dash": "dot"},
        })

    return shapes

def _build_sweep_chart_layout(shapes) -> dict:
    return {
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "font": {"family": "Arial", "size": 14, "color": "black"},
        "title": "Kurzschluss-Seilzugkräfte in Abhängigkeit von der statischen Seilzugkraft F<sub>st</sub>",
        "xaxis": {
            "title": "statische Seilzugkraft (kN)",
            "showline": True,
            "linecolor": "black",
            "ticks": "outside",
            "tickcolor": "black",
            "gridcolor": "#bbbbbb",
        },
        "yaxis": {
            "title": "Kraft (kN)",
            "rangemode": "tozero",
            "showline": True,
            "linecolor": "black",
            "ticks": "outside",
            "tickcolor": "black",
            "gridcolor": "#bbbbbb",
            "zeroline": True,
            "zerolinecolor": "black",
        },
        "shapes": shapes,
        "legend": {"title": {"text": "Legende:"}, "orientation": "h", "y": -0.15, "x": 0, "bgcolor": "transparent"},
        "margin": {"l": 60, "r": 20, "t": 60, "b": 60},
    }

sweep_chart_layout: dict = _build_sweep_chart_layout([])

def display_results(state) -> None:
    # Darstellung der erweiterten Ergebnisse im Callback:
    # state.calc_result_formatted = formatter.format_numbers_strings_scientific_and_normal(state.calc_result)
    state.calc_result_formatted = dataloader.create_df_from_calc_results(state.calc_result,
                                                                         state.temperatur_niedrig_selected,
                                                                         state.temperatur_hoch_selected)

    # Auf die Ergebnisse zugreifen, um sie in dem Text Widgets darzustellen:
    state.F_td_temp_niedrig = round(state.calc_result['F_st_20'].F_td, 2) if state.calc_result['F_st_20'].F_td not in (
        None, 0.0) else None
    state.F_td_temp_hoch = round(state.calc_result['F_st_80'].F_td, 2) if state.calc_result['F_st_80'].F_td not in (
        None, 0.0) else None
    state.F_fd_temp_niedrig = round(state.calc_result['F_st_20'].F_fd, 2) if state.calc_result['F_st_20'].F_fd not in (
        None, 0.0) else None
    state.F_fd_temp_hoch = round(state.calc_result['F_st_80'].F_fd, 2) if state.calc_result['F_st_80'].F_fd not in (
        None, 0.0) else None
    state.F_pi_d_temp_niedrig = round(state.calc_result['F_st_20'].F_pi_d, 2) if state.calc_result[
                                                                                     'F_st_20'].F_pi_d not in (None,
                                                                                                               0.0) else None
    state.F_pi_d_temp_hoch = round(state.calc_result['F_st_80'].F_pi_d, 2) if state.calc_result[
                                                                                  'F_st_80'].F_pi_d not in (None,
                                                                                                            0.0) else None
    state.b_h_temp_niedrig = round(state.calc_result['F_st_20'].b_h, 2) if state.calc_result['F_st_20'].b_h not in (
        None, 0.0) else None
    state.b_h_temp_hoch = round(state.calc_result['F_st_80'].b_h, 2) if state.calc_result['F_st_80'].b_h not in (None,
                                                                                                                 0.0) else None
    state.a_min_temp_niedrig = round(state.calc_result['F_st_20'].a_min, 2) if state.calc_result[
                                                                                   'F_st_20'].a_min not in (None,
                                                                                                            0.0) else None
    state.a_min_temp_hoch = round(state.calc_result['F_st_80'].a_min, 2) if state.calc_result['F_st_80'].a_min not in (
        None, 0.0) else None

    # Bestimme maximale (massgebende) Werte
    def get_max_value(val1, val2, val3=None):
        values = [v for v in [val1, val2, val3] if v not in (None, "", NaN)]
        return max(values) if values else ""

    # Bestimme minimale (massgebende) Werte
    def get_min_value(val1, val2):
        values = [v for v in [val1, val2] if v not in (None, "")]
        return min(values) if values else ""

    state.F_td_massg = get_max_value(state.F_td_temp_niedrig, state.F_td_temp_hoch)
    state.temp_F_td_massg = state.temperatur_hoch_selected if state.F_td_temp_hoch > state.F_td_temp_niedrig else state.temperatur_niedrig_selected
    state.F_fd_massg = get_max_value(state.F_fd_temp_niedrig, state.F_fd_temp_hoch)
    state.temp_F_fd_massg = state.temperatur_hoch_selected if state.F_fd_temp_hoch > state.F_fd_temp_niedrig else state.temperatur_niedrig_selected
    state.F_pi_d_massg = get_max_value(state.F_pi_d_temp_niedrig, state.F_pi_d_temp_hoch)
    if state.F_pi_d_temp_hoch not in (None, 0.0) and state.F_pi_d_temp_niedrig not in (None, 0.0):
        state.temp_F_pi_d_massg = state.temperatur_hoch_selected if state.F_pi_d_temp_hoch > state.F_pi_d_temp_niedrig else state.temperatur_niedrig_selected
    state.F_td_fd_pi_d_massg_1 = round(get_max_value(state.F_td_massg * 1.5, state.F_fd_massg, state.F_pi_d_massg), 2)
    state.F_td_fd_pi_d_massg_2 = get_max_value(state.F_td_massg, state.F_fd_massg, state.F_pi_d_massg)
    state.b_h_max = get_max_value(state.b_h_temp_niedrig, state.b_h_temp_hoch)
    state.temp_b_h = state.temperatur_hoch_selected if state.b_h_temp_niedrig < state.b_h_temp_hoch else state.temperatur_niedrig_selected
    state.a_min_min = get_min_value(state.a_min_temp_niedrig, state.a_min_temp_hoch)

def on_change_selectable_leiterseiltyp(state):
    #state.leiterseiltyp_lov = list(state.leiterseiltyp.keys())
    state.leiterseiltyp = leiterseiltyp[leiterseiltyp["Bezeichnung"] == state.leiterseiltyp_selected]
    notify(state, notification_type="info", message=f'Leiterseiltyp auf {state.leiterseiltyp["Bezeichnung"].values[0]} geändert')
    #print(state.leiterseiltyp["Dauerstrombelastbarkeit"].values[0])

def on_click_leiterseiltyp_zurücksetzen(state):
    state.leiterseiltyp = dataloader.load_csv_to_df()
    state.leiterseiltyp_selected = None
    #state.leiterseiltyp_lov = list(state.leiterseiltyp.keys())
    notify(state, notification_type="info", message="Auswahl aufgehoben")

def on_click_zurücksetzen(state):
    state.name_der_verbindung = ""
    state.leiterseilbefestigung_selected = None
    state.schlaufe_in_spannfeldmitte_selected = None
    state.hoehenunterschied_befestigungspunkte_selected = None
    state.standardkurzschlussstroeme_selected = "0.0" # muss float sein
    state.kappa = None
    state.t_k = None
    state.frequenz_des_netzes_selected = None
    state.leiterseiltyp_selected = None
    state.l = None
    state.l_i = None
    state.l_h_f = None
    state.a = None
    state.teilleiter_selected = "0" # muss int sein
    state.a_s = None
    state.F_st_20 = None
    state.F_st_80 = None
    state.federkoeffizient_selected = "0" # muss int sein
    state.schlaufenebene_parallel_senkrecht_selected = None
    state.temperatur_niedrig_selected = None
    state.temperatur_hoch_selected = None
    state.m_c = None
    state.l_s_1 = None
    state.l_s_2 = None
    state.l_s_3 = None
    state.l_s_4 = None
    state.l_s_5 = None
    state.l_s_6 = None
    state.l_s_7 = None
    state.l_s_8 = None
    state.l_s_9 = None
    state.l_s_10 = None
    on_click_leiterseiltyp_zurücksetzen(state)

    state.F_td_temp_niedrig = None
    state.F_fd_temp_niedrig = None
    state.F_pi_d_temp_niedrig = None

    state.F_td_temp_hoch = None
    state.F_fd_temp_hoch = None
    state.F_pi_d_temp_hoch = None

    state.F_td_massg = None
    state.F_fd_massg = None
    state.F_pi_d_massg = None
    state.temp_F_td_massg = None
    state.temp_F_fd_massg = None
    state.temp_F_pi_d_massg = None


    state.F_td_fd_pi_d_massg_1 = None
    state.F_td_fd_pi_d_massg_2 = None

    state.b_h_temp_niedrig = None
    state.b_h_temp_hoch = None
    state.b_h_max = None
    state.temp_b_h = None

    state.a_min_temp_niedrig = None
    state.a_min_temp_hoch = None
    state.a_min_min = None

    state.calc_result = None
    state.calc_result_formatted = None
    state.sweep_calc_df = None
    state.sweep_vline_shapes = []
    state.sweep_chart_layout = _build_sweep_chart_layout([])

def on_click_berechnen(state):
    run_id = _next_calc_run_id()

    required_fields = [
        # Allgemeine Angaben
        ('leiterseilbefestigung_selected', 'Art der Leiterseilbefestigung'),
        ('schlaufe_in_spannfeldmitte_selected', 'Schlaufe in Spannfeldmitte'),
        ('hoehenunterschied_befestigungspunkte_selected', 'Höhenunterschied der Befestigungspunkte'),
        #('schlaufenebene_parallel_senkrecht_selected', 'Schlaufebene'),
        ('temperatur_niedrig_selected', 'Niedrigste Temperatur'),
        ('temperatur_hoch_selected', 'Höchste Temperatur'),
        # Elektrische Werte
        ('standardkurzschlussstroeme_selected', 'Kurzschlussstrom'),
        ('kappa', 'Stossfaktor'),
        ('t_k', 'Kurzschlussdauer'),
        ('frequenz_des_netzes_selected', 'Frequenz des Netzes'),
        # Leiterseilkonfiguration
        ('leiterseiltyp_selected', 'Leiterseiltyp'),
        ('teilleiter_selected', 'Anzahl Teilleiter'),
        # Abstände
        ('l', 'Mittenabstand der Stützpunkte'),
        ('a', 'Leitermittenabstand'),
        # Mechanische Kraftwerte
        ('F_st_20', 'Statische Seilzugkraft bei -20°C'),
        ('F_st_80', 'Statische Seilzugkraft bei 80°C'),
        ('federkoeffizient_selected', 'Federkoeffizient'),
    ]

    # Prüfe alle minimum Pflichtfelder
    missing = []
    for field, label in required_fields:
        value = getattr(state, field, None)
        if (value is None or value == '' or
                (isinstance(value, (int, float, str)) and str(value) == '0.0') or
                (isinstance(value, (int, float, str)) and str(value) == '0') or
                (isinstance(value, (int, float, str)) and str(value) == '')):
            missing.append(label)

    if missing:
        notify(state, notification_type="error",
               message=f"Bitte folgende Pflichtfelder ausfüllen: {', '.join(missing)}", duration=15000)
        return
    if not state.leiterseiltyp_selected:
        notify(state, notification_type="error",
               message="Bitte Leiterseiltyp auswählen!", duration=15000)
        return

    # Auswahlbedingte Überprüfungen
    if state.teilleiter_selected in (None, 0.0, 0, '', '0.0', '0'):
        notify(state, notification_type="error",
               message=f"Bitte folgendes Pflichtfeld ausfüllen: 'n', 'Anzahl der Teilleiter eines Hauptleiters'", duration=15000)
    if int(state.teilleiter_selected) > 1 and state.a_s in (None, 0.0, 0, '', '0.0', '0'):
        notify(state, notification_type="error",
               message=f"Bitte folgendes Pflichtfeld ausfüllen: 'a_s', 'Wirksamer Abstand zwischen Teilleitern'", duration=15000)
        return
    if float(state.l) > 5 and state.l_s_1 in (None, 0.0, 0, '', '0.0', '0'):
        notify(state, notification_type="warning",
               message=f"Bitte folgende Eingabefelder überprüfen: 'l_s', 'Abstandshalter'", duration=15000)
    if state.leiterseilbefestigung_selected == "Abgespannt" and state.l_i in (None, 0.0, 0, '', '0.0', '0'):
        notify(state, notification_type="warning",
               message=f"Bitte folgendes Eingabefeld überprüfen: 'l_i', 'Länge einer Abspann-Isolatorkette'", duration=15000)
    if state.leiterseilbefestigung_selected == "Abgespannt" and state.m_c in (None, 0.0, 0, '', '0.0', '0'):
        notify(state, notification_type="warning",
               message=f"Bitte folgendes Eingabefeld überprüfen: 'm_c', 'Summe konzentrischer Massen im Spannfeld'", duration=15000)
    if state.leiterseilbefestigung_selected == "Aufgelegt" and state.l_h_f in (None, 0.0, 0, '', '0.0', '0'):
        notify(state, notification_type="warning",
               message=f"Bitte folgendes Eingabefeld überprüfen: 'l_h_f', 'Länge einer Klemme u. Formfaktor'", duration=15000)


    # Bereinigen der alten States, damit keine Variablenleichen entstehen, wenn zum Beispiel bei einer Rechnung
    # oder Fall nicht alle Parameter berechnet werden. In so einem Fall dürfen sich die "alten" Variablen nicht mit den
    # "neuen vermischen".
    state.F_td_temp_niedrig = None
    state.F_fd_temp_niedrig = None
    state.F_pi_d_temp_niedrig = None

    state.F_td_temp_hoch = None
    state.F_fd_temp_hoch = None
    state.F_pi_d_temp_hoch = None

    state.F_td_massg = None
    state.F_fd_massg = None
    state.F_pi_d_massg = None
    state.temp_F_td_massg = None
    state.temp_F_fd_massg = None
    state.temp_F_pi_d_massg = None

    state.F_td_fd_pi_d_massg_1 = None
    state.F_td_fd_pi_d_massg_2 = None

    state.b_h_temp_niedrig = None
    state.b_h_temp_hoch = None
    state.b_h_max = None
    state.temp_b_h = None

    state.a_min_temp_niedrig = None
    state.a_min_temp_hoch = None
    state.a_min_min = None

    state.calc_result = None
    state.calc_result_formatted = None

    try:
        # Erstellung des Input-Objekts für den Mediator
        inputs = KurschlusskräfteLeiterseileInput(
            leiterseilbefestigung=str(state.leiterseilbefestigung_selected),
            schlaufe_in_spannfeldmitte=str(state.schlaufe_in_spannfeldmitte_selected),
            hoehenunterschied_befestigungspunkte=str(state.hoehenunterschied_befestigungspunkte_selected),
            schlaufenebene_parallel_senkrecht=str(state.schlaufenebene_parallel_senkrecht_selected),
            temperatur_niedrig=int(state.temperatur_niedrig_selected),
            temperatur_hoch=int(state.temperatur_hoch_selected),
            standardkurzschlussstroeme=float(state.standardkurzschlussstroeme_selected),
            κ=float(state.kappa),
            t_k=float(state.t_k),
            f=float(state.frequenz_des_netzes_selected),
            leiterseiltyp=str(state.leiterseiltyp_selected) if state.leiterseiltyp_selected else None,
            d=float(state.leiterseiltyp["Aussendurchmesser"].values[0]),
            A_s=float(state.leiterseiltyp["Querschnitt eines Teilleiters"].values[0]),
            m_s=float(state.leiterseiltyp["Massenbelag eines Teilleiters"].values[0]),
            E=float(state.leiterseiltyp["Elastizitätsmodul"].values[0]),
            c_th=float(state.leiterseiltyp["Kurzzeitstromdichte"].values[0]),
            n=int(state.teilleiter_selected),
            m_c=float(state.m_c) if state.m_c not in (None, 0.0, 0, '', '0.0', '0') else None,
            l=float(state.l),
            l_i=float(state.l_i) if state.l_i not in (None, 0.0, 0, '', '0.0', '0')  else None,
            l_h_f= float(state.l_h_f) if state.l_h_f not in (None, 0.0, 0, '', '0.0', '0')  else None,
            a=float(state.a),
            a_s=float(state.a_s) if state.a_s not in (None, 0.0, 0, '', '0.0', '0') else None,
            F_st_20=float(state.F_st_20),
            F_st_80=float(state.F_st_80),
            federkoeffizient=int(state.federkoeffizient_selected),
            l_s_1=float(state.l_s_1) if state.l_s_1 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_2=float(state.l_s_2) if state.l_s_2 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_3=float(state.l_s_3) if state.l_s_3 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_4=float(state.l_s_4) if state.l_s_4 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_5=float(state.l_s_5) if state.l_s_5 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_6=float(state.l_s_6) if state.l_s_6 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_7=float(state.l_s_7) if state.l_s_7 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_8=float(state.l_s_8) if state.l_s_8 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_9=float(state.l_s_9) if state.l_s_9 not in (None, 0.0, 0, '', '0.0', '0') else None,
            l_s_10=float(state.l_s_10) if state.l_s_10 not in (None, 0.0, 0, '', '0.0', '0') else None
        )

        # Berechnung über den Mediator
        #print(inputs)
        calc_result = calculate_kurschlusskräfte_leiterseile(inputs)

        # Überprüft, ob das Abbruchkriterium bei mehrfachem Klicken von Berechnen für die For-Loop des Diagramms zutrifft
        if _is_run_cancelled(run_id):
            return

        # Übertragung der berechneten Werte an den state
        state.calc_result = calc_result

        # Darstellung und Auswertung der Ergebnisse
        display_results(state)

        notify(state, notification_type="success", message="Berechnung erfolgreich abgeschlossen", duration=5000)

        # Überprüft, ob das Abbruchkriterium bei mehrfachem Klicken von Berechnen für die For-Loop des Diagramms zutrifft
        if _is_run_cancelled(run_id):
            return

        try:
            state.sweep_calc_df = calculate_kurschlusskräfte_leiterseile_sweep_df(inputs, cancel_check=lambda: _is_run_cancelled(run_id))
            state.sweep_vline_shapes = _build_vline_shapes(state.sweep_calc_df, [state.F_st_20, state.F_st_80])
            state.sweep_chart_layout = _build_sweep_chart_layout(state.sweep_vline_shapes)
            # print("Sweep calc df preview:")
            # print(state.sweep_calc_df.head(10).to_string(index=False))
            notify(state, notification_type="success", message=f"Diagramm mit {len(state.sweep_calc_df)} Werten erstellt", duration=5000)
        except CalculationCancelled:
            return
        except Exception as sw:
            state.sweep_calc_df = None
            state.sweep_vline_shapes = []
            state.sweep_chart_layout = _build_sweep_chart_layout([])
            notify(state, notification_type="warning",
                   message=f"Diagramm konnte nicht erstellt werden: {str(sw)}", duration=10000)

    except ValueError as ve:
        error_msg = helper.get_exception_message(ve, show_chain=True)
        notify(state, notification_type="error", message=f"Fehler bei der Berechnung {error_msg}: {str(ve)}", duration=15000)

    except IndexError as ie:
        error_msg = helper.get_exception_message(ie, show_chain=True)
        notify(state, notification_type="error", message=f"Fehler bei der Berechnung {error_msg}: {str(ie)}", duration=15000)

    except NotImplementedError as nie:
        # Behandlung für noch nicht implementierte Fälle
        notify(state, notification_type="warning", message=f"⚠️ Diese Berechnungsmethode ist noch nicht implementiert:\n{str(nie)}", duration=15000)

    except Exception as e:
        print(f"Detaillierter Fehler:")
        traceback.print_exc()
        tb = traceback.extract_tb(e.__traceback__)
        error_msg = helper.get_exception_message(e, show_chain=True)
        notify(state, notification_type="error", message=f"Fehler bei der Berechnung {error_msg}: {str(e)}", duration=15000)

def on_click_load_vorlage(state):
    """
    Lädt Vorlage aus Excel und setzt GUI-Widgets.
    """

    # Reset all fields and results
    on_click_zurücksetzen(state)

    # Check if file_selector has content (it can be a string path or empty)
    file_path = state.content_vorlage

    # Check if a file path exists and is valid
    if not file_path or file_path == '' or file_path is None:
        notify(state, notification_type="warning", message="Bitte erst eine Datei auswählen")
        return

    # Additional check: verify the file path is a string (not during upload transition)
    if not isinstance(file_path, str):
        notify(state, notification_type="warning", message="Ungültiger Dateipfad. Bitte Datei erneut auswählen.")
        return

    try:
        # Lade die Excel-Datei über dataloader
        df = dataloader.load_excel_to_df(file_path)

        if df.empty:
            notify(state, notification_type="error", message="Datei konnte nicht geladen werden oder ist leer")
            return

        # Konvertiere DataFrame zu Dictionary mit den State-Variablen
        input_dict, loaded_fields, skipped_fields = dataloader.convert_excel_to_input_dict(df)

        if not input_dict:
            notify(state, notification_type="error", message="Keine gültigen Eingabedaten in der Datei gefunden")
            return

        # Speichere aktuellen Zustand für Undo
        state.vorlage_backup = {}
        for key in input_dict.keys():
            state.vorlage_backup[key] = getattr(state, key, None)

        # Setze alle State-Variablen aus dem Dictionary
        for key, value_from_dict in input_dict.items():
            setattr(state, key, value_from_dict)

        # Laden des Leiterseiltyps
        on_change_selectable_leiterseiltyp(state)

        # Erstelle Feedback-Nachricht
        message = f"✓ {len(loaded_fields)} Felder geladen"
        if skipped_fields:
            # Nur optionale Felder anzeigen, wenn sie übersprungen wurden
            optional_keywords = ['Phasenabstandshalter', 'Summe konzentrischer Massen',
                                 'Länge einer Abspann-Isolatorkette', 'wirksamer Abstand']
            optional_skipped = [f for f in skipped_fields if any(kw in f for kw in optional_keywords)]
            required_skipped = [f for f in skipped_fields if f not in optional_skipped]

            if required_skipped:
                message += f"\n⚠ {len(required_skipped)} Pflichtfelder fehlen"

        notify(state, notification_type="success", message=message, duration=5000)

        # WICHTIG: Setze content_vorlage zurück, um Memory Leak zu vermeiden
        state.content_vorlage = None

    except Exception as e:
        notify(state, notification_type="error", message=f"Fehler beim Laden der Datei: {str(e)}")
        # Setze auch bei Fehler zurück
        state.content_vorlage = None

def on_click_undo_vorlage(state):
    """
    Stellt den vorherigen Zustand vor dem Laden der Vorlage wieder her.
    """
    if state.vorlage_backup is None:
        notify(state, notification_type="warning", message="Keine vorherige Version zum Wiederherstellen vorhanden")
        return

    try:
        # Stelle alle gespeicherten Werte wieder her
        for key, value in state.vorlage_backup.items():
            setattr(state, key, value)

        on_click_leiterseiltyp_zurücksetzen(state)

        # Lösche das Backup nach dem Wiederherstellen
        state.vorlage_backup = None

        notify(state, notification_type="info", message="Vorherige Werte wiederhergestellt")

    except Exception as e:
        notify(state, notification_type="error", message=f"Fehler beim Wiederherstellen: {str(e)}")

def on_click_export_vorlage(state):
    """
    Exportiert die aktuellen GUI-Werte in eine Excel-Datei.
    Verwendet die hochgeladene Vorlage als Basis oder die Standard-Vorlage.
    """
    try:
        # Bestimme die Vorlage: Entweder die hochgeladene Datei oder die Standard-Vorlage
        template_path = None
        if state.content_vorlage and state.content_vorlage != '':
            template_path = Path(state.content_vorlage)
        else:
            # Verwende Standard-Vorlage
            template_path = Path(dataloader.get_project_root()) / "src" / "templates" / "Export Vorlage Kurzschlusskraft Leiterseile.xlsx"

        if not template_path.exists():
            notify(state, notification_type="error", message="Keine Vorlage gefunden. Bitte erst eine Datei auswählen.",
                   duration=15000)
            return

        # Sammle alle aktuellen State-Werte
        export_dict = {
            'leiterseilbefestigung_selected': state.leiterseilbefestigung_selected,
            'schlaufe_in_spannfeldmitte_selected': state.schlaufe_in_spannfeldmitte_selected,
            'hoehenunterschied_befestigungspunkte_selected': state.hoehenunterschied_befestigungspunkte_selected,
            'schlaufenebene_parallel_senkrecht_selected': state.schlaufenebene_parallel_senkrecht_selected,
            'temperatur_niedrig_selected': state.temperatur_niedrig_selected,
            'temperatur_hoch_selected': state.temperatur_hoch_selected,
            'standardkurzschlussstroeme_selected': state.standardkurzschlussstroeme_selected,
            'kappa': state.kappa,
            't_k': state.t_k,
            'frequenz_des_netzes_selected': state.frequenz_des_netzes_selected,
            'leiterseiltyp_selected': state.leiterseiltyp_selected,
            'teilleiter_selected': state.teilleiter_selected,
            'm_c': state.m_c,
            'l': state.l,
            'l_i': state.l_i,
            'a': state.a,
            'a_s': state.a_s,
            'F_st_20': state.F_st_20,
            'F_st_80': state.F_st_80,
            'federkoeffizient_selected': state.federkoeffizient_selected,
            'l_s_1': state.l_s_1,
            'l_s_2': state.l_s_2,
            'l_s_3': state.l_s_3,
            'l_s_4': state.l_s_4,
            'l_s_5': state.l_s_5,
            'l_s_6': state.l_s_6,
            'l_s_7': state.l_s_7,
            'l_s_8': state.l_s_8,
            'l_s_9': state.l_s_9,
            'l_s_10': state.l_s_10,
        }

        # Erstelle Dateinamen mit name_der_verbindung und Timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        connection_name = state.name_der_verbindung if state.name_der_verbindung else "Unbenannt"
        # Entferne ungültige Zeichen für Dateinamen
        connection_name = "".join(c for c in connection_name if c.isalnum() or c in (' ', '_', '-')).strip()
        if not connection_name:
            connection_name = "Unbenannt"
        filename = f"{connection_name}_{timestamp}.xlsx"

        # Erstelle temporäre Datei mit richtigem Namen im Temp-Verzeichnis
        # Wichtig: Datei muss mit dem gewünschten Namen existieren, damit Browser ihn übernimmt
        temp_dir = tempfile.gettempdir()
        output_path = Path(temp_dir) / filename

        # Exportiere zu Excel mit Vorlage
        success = dataloader.export_input_dict_to_excel(export_dict, template_path, output_path)

        if success:
            # Lese die erstellte Datei und trigger Download mit richtigem Namen
            with open(output_path, 'rb') as f:
                file_content = f.read()

            # Nutze download() Funktion für korrekten Dateinamen
            download(state, content=file_content, name=filename)
            notify(state, notification_type="success", message=f"Download gestartet: {filename}",
                   duration=5000)
        else:
            notify(state, notification_type="error", message="Fehler beim Erstellen der Excel-Datei.", duration=15000)

    except Exception as e:
        print(f"Detaillierter Fehler beim Export:")
        traceback.print_exc()
        notify(state, notification_type="error", message=f"Fehler beim Export: {str(e)}", duration=15000)

with tgb.Page() as kurzschlusskraefte_leiterseile_calc_page:
    build_navbar()
    tgb.html("br")
    tgb.text(value="Kurzschlussfestigkeit bei Leiterseilen", class_name="h1")
    with tgb.layout(columns="1 1", class_name="p1", columns__mobile="1"):
        with tgb.part(class_name="card"):
            tgb.text(value="Eingaben", class_name="h2")
            tgb.html("br")
            tgb.text(value="Allgemeine Angaben", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1", columns__mobile="1"):
                tgb.input(label="Name der Leiterseilverbindung", value="{name_der_verbindung}",
                      hover_text="Angabe des Projekts, Feldes und der Verbindung.",
                      class_name="input-with-unit --unit; mb1")
            with tgb.layout(columns="1 1 1", columns__mobile="1"):
                tgb.selector(label="Art der Leiterseilbefestigung", value="{leiterseilbefestigung_selected}",
                             lov="{leiterseilbefestigung_lov}", dropdown=True)
                tgb.selector(label="Schlaufe in Spannfeldmitte",
                             value="{schlaufe_in_spannfeldmitte_selected}", lov="{schlaufe_in_spannfeldmitte_lov}",
                             dropdown=True,
                             hover_text="Ja, wenn der obere Befestigungspunkt der Schlaufe bis "
                                        "zu 10 % der Länge des Hauptleiters von der Mitte entfernt ist.")
                tgb.selector(label="Höhenunterschied der Befestigungspunkte mehr als 25%",
                             value="{hoehenunterschied_befestigungspunkte_selected}",
                             lov="{hoehenunterschied_befestigungspunkte_lov}",
                             dropdown=True,
                             hover_text="Ja, wenn der Höhenunterschied der Befestigungspunkte "
                                        "mehr als 25 % der Spannfeldlänge beträgt.")
                tgb.selector(label="Schlaufebene bei Schlaufen in Spannfeldmitte",
                             value="{schlaufenebene_parallel_senkrecht_selected}",
                             lov="{schlaufenebene_parallel_senkrecht_lov}",
                             dropdown=True,
                             hover_text="Angabe nur notwendig, wenn Schlaufen in Spannfeldmitte verwendet werden.\n"
                                        "Parallel: Schlaufe verläuft hauptsächlich horizontal "
                                        "(Winkel zwischen oberem und unterem Anschlusspunkt < 45° ).\n"
                                        "Senkrecht: Schlaufe verläuft hauptsächlich vertikal "
                                        "(Winkel zwischen oberem und unterem Anschlusspunkt > 45°).\n"
                                        "Hinweis: Die Schlaufenebene wird nur bei Schlaufen in Spannfeldmitte berücksichtigt.")
                tgb.selector(label="ϑ_l Niedrigste Temperatur",
                             value="{temperatur_niedrig_selected}",
                             lov="{temperatur_niedrig_lov}",
                             dropdown=True, hover_text="Örtliche Tiefsttemperatur",
                             class_name="input-with-unit Grad-Celsius-unit")
                tgb.selector(label="ϑ_h Höchste Temperatur",
                             value="{temperatur_hoch_selected}",
                             lov="{temperatur_hoch_lov}",
                             dropdown=True, hover_text="Höchste Betriebstemperatur der Leiter",
                             class_name="input-with-unit Grad-Celsius-unit")
            tgb.html("br")
            tgb.text(value="Elektrische Werte", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1 1 1 1", columns__mobile="1", class_name=""):
                tgb.selector(label="I''k Anfangs-Kurzschlusswechselstrom beim dreipoligen Kurzschluss (Effektivwert)",
                             value="{standardkurzschlussstroeme_selected}", lov="{standardkurzschlussstroeme_lov}",
                             dropdown=True, class_name="input-with-unit A-unit")
                tgb.number(label="κ Sossfaktor", value="{kappa}", min=0.01, max=2.0, step=0.01, class_name="input-with-unit --unit")
                tgb.number(label="Tk Kurzschlussdauer", value="{t_k}", min=0.01, max=5.0, step=0.01,
                           hover_text="Wird kein Stossfaktor angegeben wird der Wert 1.8 angenommen.",
                           class_name="input-with-unit tk-unit Mui-focused")
                tgb.selector(label="f Frequenz des Netzes",
                             value="{frequenz_des_netzes_selected}", lov="{frequenz_des_netzes_lov}",
                             dropdown=True, class_name="input-with-unit Hz-unit")
            tgb.html("br")
            tgb.text(value="Leiterseilkonfiguration", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1 1 1", columns__mobile="1"):
                tgb.selector(label="Leiterseiltyp", value="{leiterseiltyp_selected}", lov="{leiterseiltyp_lov}",
                             dropdown=True, on_change=on_change_selectable_leiterseiltyp)
                tgb.selector(label="n Anzahl der Teilleiter eines Hauptleiters",
                             value="{teilleiter_selected}", lov="{teilleiter_lov}", dropdown=True)
                tgb.number(label="m_c Summe konzentrischer Massen im Spannfeld", value = "{m_c}", min = 0.0, max = 500.0,
                           step = 0.1, hover_text="z. B. durch Klemmen, Schlaufen, Abstandshalter oder Gegenkontakte.",
                           class_name = "input-with-unit kg-unit Mui-focused")
            tgb.html("br")
            tgb.text(value="Abstände", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1 1 1", columns__mobile="1"):
                tgb.number(label="l Mittenabstand der Stützpunkte", value="{l}", min=0.0, max=150.0, step=0.1,
                           class_name="input-with-unit m-unit Mui-focused")
                tgb.number(label="l_i Länge einer Abspann-Isolatorkette", value="{l_i}", min=0.0, max=20.0,
                           step=0.1, hover_text="Es ist der Abstand nur einer Abspann-Isolatorkette einzugeben.",
                           class_name="input-with-unit m-unit Mui-focused")
                tgb.number(label="l_h_f Länge einer Klemme u. Formfaktor", value="{l_h_f}", min=0.0, max=20.0,
                           step=0.1, hover_text="Nur bei aufgelegten Leiterseilen anzugeben. Es ist der "
                                                "Abstand nur einer Klemme und ein Formfaktor anzugeben.",
                           class_name="input-with-unit m-unit Mui-focused")
                tgb.number(label="a Leitermittenabstand", value="{a}", min=0.0, max=20.0, step=0.1,
                           hover_text="Bei sich verändernden Leitermittenabständen in der Spannfeld (z.B. zueinander "
                                      "zulaufende Leiterseilverbindungen, bei den der Abstand  an den Befestigungspunkten "
                                      "unterschiedlich sind, ist der Mittelwert, also der über die Länge gemittelte "
                                      "Abstand, zu verwenden.",
                           class_name="input-with-unit m-unit Mui-focused")
                tgb.number(label="a_s wirksamer Abstand zwischen Teilleitern", value="{a_s}", min=0.0, max=5.0, step=0.1,
                           hover_text="Nur bei mehreren Teilleitern anzugeben.", class_name="input-with-unit m-unit Mui-focused")
            tgb.html("br")
            tgb.text(value="Mechanische Kraftwerte", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1 1 1", columns__mobile="1"):
                tgb.number(label="Fst-20 statische Seilzugkraft in einem Hauptleiter", value="{F_st_20}", min=0.0,
                           step=0.1,
                           hover_text="Bei der Ermittlung der statischen Seilzugkraft Fst sollte der Beitrag \n"
                                      "konzentrierter Massen im Spannfeld, z. B. durch Klemmen, Schlaufen oder Gegenkontakte, berücksichtigt \n"
                                      "werden. Bei Schlaufen sollte dabei die Hälfte der Schlaufenmasse angesetzt werden.",
                           class_name="input-with-unit N-unit Mui-focused")
                tgb.number(label="Fst80 statische Seilzugkraft in einem Hauptleiter", value="{F_st_80}", min=0.0,
                           step=0.1,
                           hover_text="Bei der Ermittlung der statischen Seilzugkraft Fst sollte der Beitrag \n" 
                                      "konzentrierter Massen im Spannfeld, z. B. durch Klemmen, Schlaufen oder Gegenkontakte, berücksichtigt \n"
                                      "werden. Bei Schlaufen sollte dabei die Hälfte der Schlaufenmasse angesetzt werden.",
                           class_name="input-with-unit N-unit Mui-focused")
                tgb.selector(label="S resultierender Federkoeffizient beider Stützpunkte im Spannfeld",
                             value="{federkoeffizient_selected}", lov="{federkoeffizient_lov}",
                             dropdown=True, class_name="input-with-unit inv-N_m-unit")
            tgb.html("br")
            tgb.text(value="Erweiterte Eingaben", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1", columns__mobile="1"):
                with tgb.expandable(title="Abstände Abstandshalter", expanded=False, class_name="h6",
                                    hover_text="Abstände beginnend von links vom Ende der Isolatorkette oder dem Anschlusspunkt bei aufgelegten Leiterseilen. \n"
                                               "Abstände zwischen Abstandshaltern, Gegenkontakte von Trennern zählen ebenfalls als Abstandshalter. \n"
                                               "Die gesamte Seillänge eines Hauptleiters und die Summe der angegebenen Abstände müssen übereinstimmen bzw. gleich sein."):
                    with tgb.layout(columns="1 1 1 1 1", columns__mobile="1"):
                        tgb.number(label="Abstandshalter 1", value="{l_s_1}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 2", value="{l_s_2}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 3", value="{l_s_3}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 4", value="{l_s_4}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 5", value="{l_s_5}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 6", value="{l_s_6}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 7", value="{l_s_7}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 8", value="{l_s_8}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 9", value="{l_s_9}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstandshalter 10", value="{l_s_10}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        # Todo: Hier müssen unbedingt die zusätzlichen Gewichte noch abgefragt werden (Gegenkontakts, Abstandhalters).
            tgb.html("br")
            with tgb.layout(columns="1 1 1", columns__mobile="1", class_name="p0"):
                tgb.button(label="Berechnen", on_action=on_click_berechnen, class_name="fullwidth")
                tgb.button(label="Alles zurücksetzen", on_action=on_click_zurücksetzen, class_name="fullwidth")
                tgb.button(label="Leiterseiltyp aufheben", on_action=on_click_leiterseiltyp_zurücksetzen, class_name="fullwidth")
            tgb.html("br")
            with tgb.layout(columns="1 1 1 1", columns__mobile="1", class_name="p0"):
                tgb.file_selector(content="{content_vorlage}", label="Vorlage auswählen", extensions=".xlsx",
                                  drop_message="Drop Message", class_name="fullwidth")
                tgb.button(label="Vorlage laden", on_action=on_click_load_vorlage, class_name="fullwidth")
                tgb.button(label="Laden Rückgängig", on_action=on_click_undo_vorlage, class_name="fullwidth")
                tgb.button(label="Excel Export herunterladen", on_action=on_click_export_vorlage, class_name="fullwidth")
            tgb.html("br")
        with tgb.part(class_name="card"):
            tgb.text(value="Ergebnisse", class_name="h2")
            tgb.html("br")
            with tgb.layout(columns="1 1 1", columns__mobile="1", class_name="p0"):
                with tgb.part():
                    tgb.text(value="Massgebende Seilzugkräfte bei {temperatur_niedrig_selected}/{temperatur_hoch_selected} °C", class_name="h6")
                    tgb.html("hr")
                    tgb.text(value="Ft,d bei {temp_F_td_massg} °C: {F_td_massg} kN", class_name="mb-4")
                    tgb.text(value="Ff,d bei {temp_F_fd_massg} °C: {F_fd_massg} kN", class_name="mb-4")
                    tgb.text(value="Fpi,d bei {temp_F_pi_d_massg} °C: {F_pi_d_massg} kN", class_name="mb-4")
                    tgb.html("br")
                with tgb.part():
                    tgb.text(value="Maximale Seilzugkräfte bei {temperatur_niedrig_selected} °C", class_name="h6")
                    tgb.html("hr")
                    tgb.text(value="Ft,d bei {temperatur_niedrig_selected} °C: {F_td_temp_niedrig} kN", class_name="mb-4")
                    tgb.text(value="Ff,d bei {temperatur_niedrig_selected} °C: {F_fd_temp_niedrig} kN", class_name="mb-4")
                    tgb.text(value="Fpi,d bei {temperatur_niedrig_selected} °C: {F_pi_d_temp_niedrig} kN", class_name="mb-4")
                    tgb.html("br")
                with tgb.part():
                    tgb.text(value="Maximale Seilzugkräfte bei {temperatur_hoch_selected} °C", class_name="h6")
                    tgb.html("hr")
                    tgb.text(value="Ft,d bei {temperatur_hoch_selected} °C: {F_td_temp_hoch} kN", class_name="mb-4")
                    tgb.text(value="Ff,d bei {temperatur_hoch_selected} °C: {F_fd_temp_hoch} kN", class_name="mb-4")
                    tgb.text(value="Fpi,d bei {temperatur_hoch_selected} °C: {F_pi_d_temp_hoch} kN", class_name="mb-4")
                    tgb.html("br")
            with tgb.layout(columns="1 1", columns__mobile="1", class_name="p0"):
                with tgb.part():
                    tgb.text(value="Seilauslenkung und Abstand", class_name="h6")
                    tgb.html("hr")
                    tgb.text(value="Maximale horizontale Seilauslenkung bei {temp_b_h} °C: {b_h_max} m",
                             class_name="mb-4")
                    tgb.text(value="Minimaler Leiterabstand bei {temp_b_h} °C: {a_min_min} m", class_name="mb-4")
                    tgb.html("br")
                    tgb.text(value="Auslegungen der Verbindungsmittel und Unterkonstruktionen", class_name="h6")
                    tgb.html("hr")
                    tgb.text(value="Die Befestigungsmittel von Leiterseilen (z.B. Klemmen) sind für den höchsten der "
                                   "Werte 1,5 Ft,d, 1,0 Ff,d oder 1,0 Fpi,d, hier {F_td_fd_pi_d_massg_1} kN, "
                                   "zu bemessen.", class_name="mb-4")
                    tgb.text(value="Für die Bemessung der Abspanngerüste, Unterkonstruktionen (Gerätegerüste), "
                                   "Isolatorketten, Verbindungsmittel, Fundamente und Stützisolatoren ist der höchste "
                                   "der Werte Ft,d, Ff,d, Fpi,d, hier {F_td_fd_pi_d_massg_2} kN, als "
                                   "statische Last anzusetzen.", class_name="mb-4")
                    tgb.text(value="Der Bemessungswert der Festigkeit, der Unterkonstruktionen, der Stahlgerüste und Stützisolatoren "
                                   "muss mindestens {F_td_fd_pi_d_massg_2} kN betragen. Bei durch Biegekräfte "
                                   "beanspruchten Stützisolatoren wird der Bemessungswert der Festigkeit als eine am "
                                   "Isolatorkopf angreifende Kraft angegeben.", class_name="mb-4")
                    tgb.html("br")
                with tgb.part():
                    tgb.text(value="Erweiterte Ergebnisse", class_name="h6")
                    tgb.html("hr")
                    with tgb.expandable(title="Zusätzliche Berechnungsergebnisse", expanded=False):
                        tgb.table(data="{calc_result_formatted}", rebuild=True, number_format="%.3e",
                                  size="small", width="100%", page_size=6, page_size_options=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
            tgb.text(value="Abbildungen", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1", columns__mobile="1"):
                with tgb.expandable(title="Diagramm", expanded=False):
                    tgb.chart(data="{sweep_calc_df}", x="F_st",
                              y=["F_td", "F_fd", "F_pi_d"], name=["F<sub>td</sub>", "F<sub>fd</sub>", "F<sub>pi d</sub>"],
                              color=["red", "blue", "green"], mode="lines", rebuild=True, height="800px",
                              layout="{sweep_chart_layout}")
                    #tgb.table(examples="{calc_result_formatted}", rebuild=True, show_all=True, number_format="%.3e", size="small", width="35%")
                #with tgb.expandable(title="Zusätzliche Berechnungsergebnisse", expanded=False, class_name="h6"):
                    #tgb.text(value="{calc_result_formatted}", mode="pre")
    with tgb.layout(columns="1", class_name="p1", columns__mobile="1"):
        with tgb.expandable(title="Tabelle Leiterseiltypen", expanded=False):
            tgb.table("{leiterseiltyp}")

