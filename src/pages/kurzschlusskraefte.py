from pandas.io.clipboard import init_windows_clipboard
from taipy.gui import notify
import taipy.gui.builder as tgb
import pandas as pd
from src.utils import dataloader
from src.calculations.engine_kurzschlusskraefte import ShortCircuitInput, ShortCircuitResult, calculate_short_circuit, Kurschlusskräfte_Input

# Configuration for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.precision', 3)

leiterseilbefestigung_lov: list[str] = ["Abgespannt", "Aufgelegt", "Unterschlaufung", "Schlaufe am Spannfeldende"]
leiterseilbefestigung_selected: None|str = None

schlaufe_in_spannfeldmitte_lov: list[str] = ["Ja", "Nein"]
schlaufe_in_spannfeldmitte_selected: None|int = None

standardkurzschlussstroeme_lov: list[str] = ["10", "12.5", "16", "20", "25", "31.5", "40", "50", "63", "80"]
standardkurzschlussstroeme_selected: None | int | float = None

hoehenunterschied_befestigungspunkte_lov: list[str] = ["Ja", "Nein"]
hoehenunterschied_befestigungspunkte_selected: None|int = None

schlaufenebene_parallel_senkrecht_lov: list[str] = ["Ebene senkrecht", "Ebene parallel"]
schlaufenebene_parallel_senkrecht_selected: None|int = None

temperatur_niedrig_lov: list[str] = ["-20", "-30", "-40", "-50"]
temperatur_niedrig_selected: None | int | float = None

temperatur_hoch_lov: list[str] = ["60", "70", "80", "90", "100"]
temperatur_hoch_selected: None | int | float = None

teilleiter_lov: list[str] = ["1", "2", "3", "4", "5", "6"]
teilleiter_selected: None|int = None

federkoeffizient_lov: list[str] = ["100000", "150000", "1300000", "400000", "2000000", "600000", "3000000"]
federkoeffizient_selected: None|int = None

"""
Auswahl der Leiterseiltypen: 
1. Gesamte Leiterseildaten als Dataframe, 
2. Selektierung der ersten Spalte mit "Bezeichnung" als List of values für das Dropdown, 
3. Parameter für das initiale Laden und die spätere Auswahl
"""
leiterseiltyp: pd.DataFrame = dataloader.load_csv_to_df()
leiterseiltyp_lov: list[str] = list(leiterseiltyp["Bezeichnung"])
leiterseiltyp_selected: None|str = None

kappa: None|float = None
t_k: None|float = None
m_c: None|float = None
l: None|float = None
l_i: None|float = None
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


def on_change_selectable_leiterseiltyp(state):
    #state.leiterseiltyp_lov = list(state.leiterseiltyp.keys())
    state.leiterseiltyp = leiterseiltyp[leiterseiltyp["Bezeichnung"] == state.leiterseiltyp_selected]
    notify(state, notification_type="info", message=f'Leiterseiltyp auf {state.leiterseiltyp["Bezeichnung"].values[0]} geändert')
    print(state.leiterseiltyp["Dauerstrombelastbarkeit"].values[0])

def on_click_leiterseiltyp_zurücksetzen(state):
    state.leiterseiltyp = dataloader.load_csv_to_df()
    state.leiterseiltyp_selected = None
    #state.leiterseiltyp_lov = list(state.leiterseiltyp.keys())
    notify(state, notification_type="info", message="Auswahl aufgehoben")

def on_click_zurücksetzen(state):
    state.leiterseilbefestigung_selected = None
    state.schlaufe_in_spannfeldmitte_selected = None
    state.hoehenunterschied_befestigungspunkte_selected = None
    state.standardkurzschlussstroeme_selected = "0.0" # muss float sein
    state.kappa = None
    state.t_k = None
    state.leiterseiltyp_selected = None
    state.l = None
    state.l_i = None
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

# Für die spätere Bearbeitung
def on_calculate(state):
    if not state.leiterseiltyp_selected:
        notify(state, notification_type="error", message="Bitte Leiterseiltyp auswählen!")
        return
    if not state.standardkurzschlussstroeme_selected:
        notify(state, notification_type="error", message="Bitte Kurzschlussstrom auswählen!")
        return

    # Extraktion der Seildaten
    row = state.leiterseiltyp[state.leiterseiltyp["Bezeichnung"] == state.leiterseiltyp_selected]
    if row.empty:
        return

    try:
        # Erstellung des Input-Objekts für den Mediator
        inputs = ShortCircuitInput(
            I_k_double_prime=float(state.standardkurzschlussstroeme_selected),
            t_k=state.t_k,
            n=int(state.teilleiter_selected) if state.teilleiter_selected else 1,
            befestigung=state.leiterseilbefestigung_selected or "Aufgelegt",
            l=state.l,
            l_i=state.l_i,
            a=state.a,
            a_s=state.a_s,
            m_s=float(row["Massenbelag eines Teilleiters"].values[0].replace(',', '.')) if isinstance(
                row["Massenbelag eines Teilleiters"].values[0], str) else row["Massenbelag eines Teilleiters"].values[
                0],
            A_s=(float(row["Querschnitt eines Teilleiters"].values[0].replace(',', '.')) if isinstance(
                row["Querschnitt eines Teilleiters"].values[0], str) else row["Querschnitt eines Teilleiters"].values[
                0]) * 1e-6,
            E=(float(row["Elastizitätsmodul"].values[0].replace(',', '.')) if isinstance(
                row["Elastizitätsmodul"].values[0], str) else row["Elastizitätsmodul"].values[0]),
            F_st=state.F_st_20,  # Beispielhaft für -20°C
            S=float(state.steifigkeitsnorm_selected) if state.steifigkeitsnorm_selected else 100000.0
        )

        # Berechnung über den Mediator
        state.calc_result = calculate_short_circuit(inputs)
        notify(state, notification_type="success", message="Berechnung abgeschlossen")

    except Exception as e:
        notify(state, notification_type="error", message=f"Fehler bei der Berechnung: {str(e)}")

def on_click_test(state):
    required_fields = [
        # Allgemeine Angaben
        ('leiterseilbefestigung_selected', 'Art der Leiterseilbefestigung'),
        ('schlaufe_in_spannfeldmitte_selected', 'Schlaufe in Spannfeldmitte'),
        ('hoehenunterschied_befestigungspunkte_selected', 'Höhenunterschied der Befestigungspunkte'),
        ('schlaufenebene_parallel_senkrecht_selected', 'Schlaufebene'),
        ('temperatur_niedrig_selected', 'Niedrigste Temperatur'),
        ('temperatur_hoch_selected', 'Höchste Temperatur'),
        # Elektrische Werte
        ('standardkurzschlussstroeme_selected', 'Kurzschlussstrom'),
        ('kappa', 'Stossfaktor'),
        ('t_k', 'Kurzschlussdauer'),
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

    # Prüfe alle Pflichtfelder
    missing = []
    for field, label in required_fields:
        value = getattr(state, field, None)
        if value is None or value == '' or (isinstance(value, (int, float, str)) and str(value) == '0'):
            missing.append(label)

    if missing:
        notify(state, notification_type="error",
               message=f"Bitte folgende Pflichtfelder ausfüllen: {', '.join(missing)}", duration=100000)
        return

    try:
        # Erstellung des Input-Objekts für den Mediator
        inputs = Kurschlusskräfte_Input(
            leiterseilbefestigung=str(state.leiterseilbefestigung_selected),
            schlaufe_in_spannfeldmitte=str(state.schlaufe_in_spannfeldmitte_selected),
            hoehenunterschied_befestigungspunkte=str(state.hoehenunterschied_befestigungspunkte_selected),
            schlaufenebene_parallel_senkrecht=str(state.schlaufenebene_parallel_senkrecht_selected),
            temperatur_niedrig=int(state.temperatur_niedrig_selected),
            temperatur_hoch=int(state.temperatur_hoch_selected),
            standardkurzschlussstroeme=float(state.standardkurzschlussstroeme_selected),
            κ=float(state.kappa),
            t_k=float(state.t_k),
            leiterseiltyp=str(state.leiterseiltyp_selected) if state.leiterseiltyp_selected else None,
            n=int(state.teilleiter_selected),
            m_c=float(state.m_c) if state.m_c is not None else None,
            l=float(state.l),
            l_i=float(state.l_i) if state.l_i is not None else None,
            a=float(state.a),
            a_s=float(state.a_s) if state.a_s is not None else None,
            F_st_20=float(state.F_st_20),
            F_st_80=float(state.F_st_80),
            federkoeffizient=int(state.federkoeffizient_selected) if state.federkoeffizient_selected else None,
            l_s_1=float(state.l_s_1) if state.l_s_1 is not None else None,
            l_s_2=float(state.l_s_2) if state.l_s_2 is not None else None,
            l_s_3=float(state.l_s_3) if state.l_s_3 is not None else None,
            l_s_4=float(state.l_s_4) if state.l_s_4 is not None else None,
            l_s_5=float(state.l_s_5) if state.l_s_5 is not None else None,
            l_s_6=float(state.l_s_6) if state.l_s_6 is not None else None,
            l_s_7=float(state.l_s_7) if state.l_s_7 is not None else None,
            l_s_8=float(state.l_s_8) if state.l_s_8 is not None else None,
            l_s_9=float(state.l_s_9) if state.l_s_9 is not None else None,
            l_s_10=float(state.l_s_10) if state.l_s_10 is not None else None
        )

        # Berechnung über den Mediator
        print(inputs)
        notify(state, notification_type="success", message="Berechnung abgeschlossen")


    except ValueError as ve:
        notify(state, notification_type="error", message=f"Ungültiger Zahlenwert: {str(ve)}")
    except Exception as e:
        notify(state, notification_type="error", message=f"Fehler: {str(e)}")

with tgb.Page() as kurzschlusskraefte_page:
    # tgb.menu(label="Menu", lov=[("a", "Option A"), ("b", "Option B"), ("c", "Option C"), ("d", "Option D")], expanded = False)
    tgb.text(value="Kurzschlussfestigkeit bei Leiterseilen", class_name="h1")
    with tgb.layout(columns="1 1", class_name="p1", columns__mobile="1 1"):
        with tgb.part(class_name="card"):
            tgb.text(value="Eingaben", class_name="h2")
            tgb.html("br")
            tgb.text(value="Allgemeine Angaben", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1 1 1", columns__mobile="1 1 1"):
                tgb.selector(label="Art der Leiterseilbefestigung", value="{leiterseilbefestigung_selected}",
                             lov="{leiterseilbefestigung_lov}", dropdown=True)
                tgb.selector(label="Schlaufe in Spannfeldmitte",
                             value="{schlaufe_in_spannfeldmitte_selected}", lov="{schlaufe_in_spannfeldmitte_lov}",
                             dropdown=True, hover_text="Ja, wenn der obere Befestigungspunkt der Schlaufe bis "
                                                       "zu 10 % der Länge des Hauptleiters von der Mitte entfernt ist.")
                tgb.selector(label="Höhenunterschied der Befestigungspunkte mehr als 25%",
                             value="{hoehenunterschied_befestigungspunkte_selected}",
                             lov="{hoehenunterschied_befestigungspunkte_lov}",
                             dropdown=True, hover_text="Ja, wenn der Höhenunterschied der Befestigungspunkte"
                                                       " mehr als 25 % der Spannfeldlänge beträgt.")
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
            with tgb.layout(columns="1 1 1", columns__mobile="1 1 1", class_name=""):
                tgb.selector(label="I''k Anfangs-Kurzschlusswechselstrom beim dreipoligen Kurzschluss (Effektivwert)",
                             value="{standardkurzschlussstroeme_selected}", lov="{standardkurzschlussstroeme_lov}",
                             dropdown=True, class_name="input-with-unit A-unit")
                tgb.number(label="κ Sossfaktor", value="{kappa}", min=0.01, max=2.0, step=0.01, class_name="input-with-unit --unit")
                tgb.number(label="Tk Kurzschlussdauer", value="{t_k}", min=0.01, max=5.0, step=0.01,
                           hover_text="Wird kein Stossfaktor angegeben wird der Wert 1.8 angenommen.",
                           class_name="input-with-unit tk-unit Mui-focused")
            tgb.html("br")
            tgb.text(value="Leiterseilkonfiguration", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1 1 1", columns__mobile="1 1 1"):
                tgb.selector(label="Leiterseiltyp", value="{leiterseiltyp_selected}", lov="{leiterseiltyp_lov}",
                             dropdown=True, on_change=on_change_selectable_leiterseiltyp)
                tgb.selector(label="n Anzahl der Teilleiter eines Hauptleiters",
                             value="{teilleiter_selected}", lov="{teilleiter_lov}", dropdown=True)
                tgb.number(label="m_c Summe konzentrischer Massen im Spannfeld", value = "{m_c}", min = 0.0, max = 10.0,
                           step = 0.1, hover_text="z. B. durch Klemmen, Schlaufen oder Gegenkontakte.",
                           class_name = "input-with-unit kg-unit Mui-focused")
            tgb.html("br")
            tgb.text(value="Abstände", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1 1 1 1", columns__mobile="1 1 1 1"):
                tgb.number(label="l Mittenabstand der Stützpunkte", value="{l}", min=0.0, max=100.0, step=0.1,
                           class_name="input-with-unit m-unit Mui-focused")
                tgb.number(label="l_i Länge einer Abspann-Isolatorkette", value="{l_i}", min=0.0, max=10.0,
                           step=0.1, class_name="input-with-unit m-unit Mui-focused")
                tgb.number(label="a Leitermittenabstand", value="{a}", min=0.0, max=20.0, step=0.1,
                           class_name="input-with-unit m-unit Mui-focused")
                tgb.number(label="a_s wirksamer Abstand zwischen Teilleitern", value="{a_s}", min=0.0, step=0.1,
                           class_name="input-with-unit m-unit Mui-focused")
            tgb.html("br")
            tgb.text(value="Mechanische Kraftwerte", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1 1 1", columns__mobile="1 1 1"):
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
                with tgb.expandable(title="Abstände Phasenabstandshalter", expanded=False, class_name="h6",
                                    hover_text="Abstände beginnend von links vom Ende der Isolatorkette oder dem Anschlusspunkt bei aufgelegten Leiterseilen. \n"
                                               "Abstände zwischen Phasenabstandshaltern, Gegenkontakte von Trennern zählen ebenfalls als Phasenabstandshalter."):
                    with tgb.layout(columns="1 1 1 1 1", columns__mobile="1 1 1 1 1"):
                        tgb.number(label="Abstand Phasenabstandshalter 1", value = "{l_s_1}", min = 0.0, step = 0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 2", value="{l_s_2}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 3", value="{l_s_3}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 4", value="{l_s_4}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 5", value="{l_s_5}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 6", value="{l_s_6}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 7", value="{l_s_7}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 8", value="{l_s_8}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 9", value="{l_s_9}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        tgb.number(label="Abstand Phasenabstandshalter 10", value="{l_s_10}", min=0.0, step=0.1,
                                   class_name="input-with-unit m-unit Mui-focused")
                        # Todo: Hier müssen unbedingt die zusätzlichen Gewichte noch abgefragt werden (Gegenkontakts, Abstandhalters).
            tgb.html("br")
            with tgb.layout(columns="1 1 1", class_name="p1", columns__mobile="1 1 1"):
                tgb.button(label="Berechnen", on_action=on_click_test)
                tgb.button(label="Auswahl Leiterseiltyp aufheben", on_action=on_click_leiterseiltyp_zurücksetzen)
                tgb.button(label="Zurücksetzen", on_action=on_click_zurücksetzen)
        with tgb.part(class_name="card"):
            tgb.text(value="Ergebnisse", class_name="h2")

            tgb.html("br")
            tgb.text(value="Maximale Seilzugkräfte bei -20 °C", class_name="h6")
            tgb.html("hr")

            tgb.html("br")
            tgb.text(value="Maximale Seilzugkräfte bei 80 °C", class_name="h6")
            tgb.html("hr")

            tgb.html("br")
            tgb.text(value="Massgebende Seilzugkräfte bei -20/80 °C", class_name="h6")
            tgb.html("hr")

            tgb.html("br")
            tgb.text(value="Auslegungen der Verbindungsmittel und Unterkonstruktionen", class_name="h6")
            tgb.html("hr")

            tgb.html("br")
            tgb.text(value="Seilauslenkung und Abstand", class_name="h6")
            tgb.html("hr")

            tgb.html("br")
            tgb.text(value="Erweiterte Ergebnisse", class_name="h6")
            tgb.html("hr")

            with tgb.layout(columns="1", columns__mobile="1"):
                with tgb.expandable(title="Zusätzliche Berechnungsergebnisse", expanded=False, class_name="h6"):
                    with tgb.layout(columns="1 1 1", columns__mobile="1 1 1"):
                        pass


    with tgb.layout(columns="1", class_name="p1", columns__mobile="1"):
        with tgb.expandable(title="Tabelle Leiterseiltypen", expanded=False):
            tgb.table("{leiterseiltyp}")
