from dataclasses import asdict

from pandas.io.clipboard import init_windows_clipboard
from taipy.gui import notify, download
import taipy.gui.builder as tgb
import pandas as pd
from pathlib import Path
from datetime import datetime
import tempfile
import traceback
from src.utils import dataloader
from src.calculations.engine_kurzschlusskraefte import Kurschlusskräfte_Input, ShortCircuitResult, calculate_short_circuit

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

federkoeffizient_lov: list[str] = ["100000", "150000", "1300000", "400000", "500000", "2000000", "600000", "3000000"]
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

name_der_verbindung: None|str = ""
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

content_vorlage: str = ""
vorlage_backup: None|dict = None

F_td_temp_niedrig: None|float|str = ""
F_fd_temp_niedrig: None|float|str = ""
F_pid_temp_niedrig: None|float|str = ""

F_td_temp_hoch: None|float|str = ""
F_fd_temp_hoch: None|float|str = ""
F_pid_temp_hoch: None|float|str = ""

F_td_massg: None|float|str = ""
F_fd_massg: None|float|str = ""
F_pid_massg: None|float|str = ""



calc_result: None|ShortCircuitResult = None
calc_result_formatted: None|str = None


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
    state.name_der_verbindung = ""
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
    on_click_leiterseiltyp_zurücksetzen(state)

def on_click_berechnen(state):
    if not state.leiterseiltyp_selected:
        notify(state, notification_type="error", message="Bitte Leiterseiltyp auswählen!")
        return

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
        if (value is None or value == '' or
                (isinstance(value, (int, float, str)) and str(value) == '0.0') or
                (isinstance(value, (int, float, str)) and str(value) == '0') or
                (isinstance(value, (int, float, str)) and str(value) == '')):
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
            d=float(state.leiterseiltyp["Aussendurchmesser"].values[0]),
            A_s=float(state.leiterseiltyp["Querschnitt eines Teilleiters"].values[0]),
            m_s=float(state.leiterseiltyp["Massenbelag eines Teilleiters"].values[0]),
            E=float(state.leiterseiltyp["Elastizitätsmodul"].values[0]),
            c_th=float(state.leiterseiltyp["Kurzzeitstromdichte"].values[0]),
            n=int(state.teilleiter_selected),
            m_c=float(state.m_c) if state.m_c not in (None, 0.0) else None,
            l=float(state.l),
            l_i=float(state.l_i) if state.l_i not in (None, 0.0)  else None,
            a=float(state.a),
            a_s=float(state.a_s) if state.a_s not in (None, 0.0) else None,
            F_st_20=float(state.F_st_20),
            F_st_80=float(state.F_st_80),
            federkoeffizient=int(state.federkoeffizient_selected),
            l_s_1=float(state.l_s_1) if state.l_s_1 not in (None, 0.0) else None,
            l_s_2=float(state.l_s_2) if state.l_s_2 not in (None, 0.0) else None,
            l_s_3=float(state.l_s_3) if state.l_s_3 not in (None, 0.0) else None,
            l_s_4=float(state.l_s_4) if state.l_s_4 not in (None, 0.0) else None,
            l_s_5=float(state.l_s_5) if state.l_s_5 not in (None, 0.0) else None,
            l_s_6=float(state.l_s_6) if state.l_s_6 not in (None, 0.0) else None,
            l_s_7=float(state.l_s_7) if state.l_s_7 not in (None, 0.0) else None,
            l_s_8=float(state.l_s_8) if state.l_s_8 not in (None, 0.0) else None,
            l_s_9=float(state.l_s_9) if state.l_s_9 not in (None, 0.0) else None,
            l_s_10=float(state.l_s_10) if state.l_s_10 not in (None, 0.0) else None
        )

        # Berechnung über den Mediator
        #print(inputs)
        state.calc_result = calculate_short_circuit(inputs)

        # Dartellung der Ergebnisse:
        # Im Callback:
        def format_results(calc_result):
            """Formatiert Ergebnisse in zwei Spalten nebeneinander"""

            # Hole beide Ergebnisse
            result_20 = calc_result.get('F_st_20')
            result_80 = calc_result.get('F_st_80')

            if not result_20 or not result_80:
                return "Keine Berechnungsergebnisse verfügbar"

            # Konvertiere zu Dictionaries
            dict_20 = asdict(result_20)
            dict_80 = asdict(result_80)

            # Spaltenbreiten
            col1_width = 25  # Parameter Name
            col2_width = 20  # -20°C Werte
            col3_width = 20  # 80°C Werte

            # Erstelle Header
            lines = []
            lines.append(f"┌─{'─' * col1_width}─┬─{'─' * col2_width}─┬─{'─' * col3_width}─┐")
            lines.append(f"│ {'Parameter':<{col1_width}} │ {'-20°C':^{col2_width}} │ {'80°C':^{col3_width}} │")
            lines.append(f"├─{'─' * col1_width}─┼─{'─' * col2_width}─┼─{'─' * col3_width}─┤")

            # Iteriere durch alle Felder
            for param_name in dict_20.keys():
                val_20 = dict_20[param_name]
                val_80 = dict_80[param_name]

                # Nur nicht-None Werte anzeigen
                if val_20 is not None and val_80 is not None:
                    # Formatiere die Werte rechtsbündig
                    val_20_str = f"{val_20:.4f}"
                    val_80_str = f"{val_80:.4f}"
                    lines.append(
                        f"│ {param_name:<{col1_width}} │ {val_20_str:>{col2_width}} │ {val_80_str:>{col3_width}} │")

            lines.append(f"└─{'─' * col1_width}─┴─{'─' * col2_width}─┴─{'─' * col3_width}─┘")

            return "\n".join(lines)

        state.calc_result_formatted = format_results(state.calc_result)

        # Auf die Ergebnisse zugreifen, um sie darzustellen:
        state.F_td_temp_niedrig = state.calc_result['F_st_20'].F_td  # in kN
        state.F_td_temp_hoch = state.calc_result['F_st_80'].F_td
        state.F_fd_temp_niedrig = state.calc_result['F_st_20'].F_fd
        state.F_fd_temp_hoch = state.calc_result['F_st_80'].F_fd
        # TODO: Wenn F_fd und F_pid implementiert sind, auch diese hinzufügen:
        # state.F_pid_temp_niedrig = state.calc_result['F_st_20'].F_pid
        # state.F_pid_temp_hoch = state.calc_result['F_st_80'].F_pid

        # Bestimme maximale (maßgebende) Werte
        def get_max_value(val1, val2):
            values = [v for v in [val1, val2] if v not in (None, "")]
            return max(values) if values else ""

        state.F_td_massg = get_max_value(state.F_td_temp_niedrig, state.F_td_temp_hoch)
        state.F_fd_massg = get_max_value(state.F_fd_temp_niedrig, state.F_fd_temp_hoch)
        #state.F_pid_massg = get_max_value(state.F_pid_temp_niedrig, state.F_pid_temp_hoch)

        notify(state, notification_type="success", message="Berechnung abgeschlossen")

    except ValueError as ve:
        notify(state, notification_type="error", message=f"{str(ve)}", duration=10000)

    except NotImplementedError as nie:
        # Behandlung für noch nicht implementierte Fälle
        notify(state, notification_type="warning",
               message=f"⚠️ Diese Berechnungsmethode ist noch nicht implementiert:\n{str(nie)}",
               duration=10000)

    except Exception as e:
        print(f"Detaillierter Fehler:")
        traceback.print_exc()
        notify(state, notification_type="error", message=f"Fehler bei der Berechnung: {str(e)}")

def on_click_load_vorlage(state):
    """
    Callback-Funktion, die aufgerufen wird, wenn der "Vorlage laden" Button geklickt wird.
    Lädt die Eingabedaten aus der hochgeladenen Datei und setzt die GUI Widgets entsprechend.
    """
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
            optional_keywords = ['Phasenabstandshalter', 'Summe konzentrischer Massen', 'Länge einer Abspann-Isolatorkette', 'wirksamer Abstand']
            optional_skipped = [f for f in skipped_fields if any(kw in f for kw in optional_keywords)]
            required_skipped = [f for f in skipped_fields if f not in optional_skipped]

            if required_skipped:
                message += f"\n⚠ {len(required_skipped)} Pflichtfelder fehlen"

        notify(state, notification_type="success", message=message, duration=5000)

    except Exception as e:
        notify(state, notification_type="error", message=f"Fehler beim Laden der Datei: {str(e)}")

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
            template_path = Path(dataloader.get_project_root()) / "data" / "Export Vorlage.xlsx"

        if not template_path.exists():
            notify(state, notification_type="error", message="Keine Vorlage gefunden. Bitte erst eine Datei auswählen.")
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
            notify(state, notification_type="success", message=f"Download gestartet: {filename}")
        else:
            notify(state, notification_type="error", message="Fehler beim Erstellen der Excel-Datei. Prüfe die Konsole für Details.")

    except Exception as e:
        print(f"Detaillierter Fehler beim Export:")
        traceback.print_exc()
        notify(state, notification_type="error", message=f"Fehler beim Export: {str(e)}")

with tgb.Page() as kurzschlusskraefte_page:
    tgb.text(value="Kurzschlussfestigkeit bei Leiterseilen", class_name="h1")
    tgb.html("br")
    with tgb.layout(columns="1 1", class_name="p1", columns__mobile="1 1"):
        with tgb.part(class_name="card"):
            tgb.text(value="Eingaben", class_name="h2")
            tgb.html("br")
            tgb.text(value="Allgemeine Angaben", class_name="h6")
            tgb.html("hr")
            with tgb.layout(columns="1", columns__mobile="1"):
                tgb.input(label="Name der Leiterseilverbindung", value="{name_der_verbindung}",
                      hover_text="Angabe des Projekts, Feldes und der Verbindung.",
                      class_name="input-with-unit --unit; mb1")
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
                tgb.number(label="m_c Summe konzentrischer Massen im Spannfeld", value = "{m_c}", min = 0.0, max = 500.0,
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
                        tgb.number(label="Abstand Phasenabstandshalter 1", value="{l_s_1}", min=0.0, step=0.1,
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
            with tgb.layout(columns="1 1 1", columns__mobile="1 1 1", class_name="p0"):
                tgb.button(label="Berechnen", on_action=on_click_berechnen, class_name="fullwidth")
                tgb.button(label="Alles zurücksetzen", on_action=on_click_zurücksetzen, class_name="fullwidth")
                tgb.button(label="Leiterseiltyp aufheben", on_action=on_click_leiterseiltyp_zurücksetzen, class_name="fullwidth")
            tgb.html("br")
            with tgb.layout(columns="1 1 1 1", columns__mobile="1 1 1 1", class_name="p0"):
                tgb.file_selector(content="{content_vorlage}", label="Vorlage auswählen", extensions=".csv,.xlsx",
                                  drop_message="Drop Message", class_name="fullwidth")
                tgb.button(label="Vorlage laden", on_action=on_click_load_vorlage, class_name="fullwidth")
                tgb.button(label="Laden Rückgängig", on_action=on_click_undo_vorlage, class_name="fullwidth")
                tgb.button(label="Excel Export herunterladen", on_action=on_click_export_vorlage, class_name="fullwidth")
            tgb.html("br")
        with tgb.part(class_name="card"):
            tgb.text(value="Ergebnisse", class_name="h2")

            tgb.html("br")
            tgb.text(value="Maximale Seilzugkräfte bei {temperatur_niedrig_selected} °C", class_name="h6")
            tgb.html("hr")
            tgb.text(value="Ft,d bei {temperatur_niedrig_selected} °C: {F_td_temp_niedrig:.2f} kN", class_name="mb-4")
            tgb.text(value="Ff,d bei {temperatur_niedrig_selected} °C: {F_fd_temp_niedrig:.2f} kN", class_name="mb-4")
            tgb.text(value="Fpi,d bei {temperatur_niedrig_selected} °C: {F_pid_temp_niedrig:.2f} kN",class_name="mb-4")
            tgb.html("br")
            tgb.text(value="Maximale Seilzugkräfte bei {temperatur_hoch_selected} °C", class_name="h6")
            tgb.html("hr")
            tgb.text(value="Ft,d bei {temperatur_hoch_selected} °C: {F_td_temp_hoch:.2f} kN", class_name="mb-4")
            tgb.text(value="Ff,d bei {temperatur_hoch_selected} °C: {F_fd_temp_hoch:.2f} kN", class_name="mb-4")
            tgb.text(value="Fpi,d bei {temperatur_hoch_selected} °C: {F_pid_temp_hoch:.2f} kN", class_name="mb-4")
            tgb.html("br")
            tgb.text(value="Massgebende Seilzugkräfte bei {temperatur_niedrig_selected}/{temperatur_hoch_selected} °C", class_name="h6")
            tgb.html("hr")
            tgb.text(value="Ft,d bei {temperatur_hoch_selected} °C: {F_td_massg:.2f} kN", class_name="mb-4")
            tgb.text(value="Ff,d bei {temperatur_hoch_selected} °C: {F_fd_massg:.2f} kN", class_name="mb-4")
            tgb.text(value="Fpi,d bei {temperatur_hoch_selected} °C: {F_pid_massg:.2f} kN", class_name="mb-4")
            tgb.html("br")
            tgb.text(value="Auslegungen der Verbindungsmittel und Unterkonstruktionen", class_name="h6")
            tgb.html("hr")
            tgb.text(value="Die Befestigungsmittel von Leiterseilen sind für den höchsten der Werte 1,5 Ft,d, 1,0 Ff,d oder "
                      "1,0 Fpi,d, hier {F_pid_massg:.2f},zu bemessen.", hover_text="" , class_name="mb-4")
            tgb.text(value="Für die Bemessung der Abspanngerüste, Ketten-Isolatoren, Verbindungsmittel ist der höchste der "
                           "Werte Ft,d, Ff,d, Fpi,d, hier {F_pid_massg:.2f},als statische Last anzusetzen.", class_name="mb-4")
            tgb.text(
                value="Bei Anordnungen mit Leiterseilen darf der höchste der Werte Ft,d, Ff,d, Fpi,d, hier {F_pid_massg:.2f}, "
                      "nicht größer sein als der Bemessungswert der Festigkeit, der von den Herstellern der "
                      "Unterkonstruktionen und Stützisolatoren angegeben wird. Bei durch Biegekräfte beanspruchten "
                      "Stützisolatoren wird der Bemessungswert der Festigkeit als eine am Isolatorkopf angreifende "
                      "Kraft angegeben.", class_name="mb-4")
            tgb.html("br")
            tgb.text(value="Seilauslenkung und Abstand", class_name="h6")
            tgb.html("hr")
            tgb.text(value="bh max. horizontalen Seilauslenkung bei {temperatur_hoch_selected}: {F_pid_massg:.2f} m",
                     class_name="mb-4")
            tgb.text(value="amin min. Leiterabstand bei {temperatur_hoch_selected}: {F_pid_massg:.2f} m", class_name="mb-4")
            tgb.html("br")
            tgb.text(value="Erweiterte Ergebnisse", class_name="h6")
            tgb.html("hr")

            with tgb.layout(columns="1", columns__mobile="1"):
                with tgb.expandable(title="Zusätzliche Berechnungsergebnisse", expanded=False, class_name="h6"):
                    tgb.text(value="{calc_result_formatted}", mode="pre")

    with tgb.layout(columns="1", class_name="p1", columns__mobile="1"):
        with tgb.expandable(title="Tabelle Leiterseiltypen", expanded=False):
            tgb.table("{leiterseiltyp}")
