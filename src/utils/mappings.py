from pathlib import Path

# Reverses Mapping für den Excel Export
REVERSE_FIELD_MAPPINGS = {
    "Export Vorlage Kurzschlusskraft Leiterseile.xlsx": {
        'leiterseilbefestigung_selected': 'Art der Leiterseilbefestigung',
        'schlaufe_in_spannfeldmitte_selected': 'Schlaufe in Spannfeldmitte',
        'hoehenunterschied_befestigungspunkte_selected': 'Höhenunterschied der Befestigungspunkte mehr als 25%',
        'schlaufenebene_parallel_senkrecht_selected': 'Schlaufebene bei Schlaufen in Spannfeldmitte',
        'temperatur_niedrig_selected': 'ϑ_l Niedrigste Temperatur',
        'temperatur_hoch_selected': 'ϑ_h Höchste Temperatur',
        'standardkurzschlussstroeme_selected': 'I\'\'k Anfangs-Kurzschlusswechselstrom beim dreipoligen Kurzschluss (Effektivwert)',
        'kappa': 'κ Sossfaktor',
        't_k': 'Tk Kurzschlussdauer',
        'frequenz_des_netzes_selected': 'f Frequenz des Netzes',
        'leiterseiltyp_selected': 'Leiterseiltyp',
        'teilleiter_selected': 'n Anzahl der Teilleiter eines Hauptleiters',
        'm_c': 'm_c Summe konzentrischer Massen im Spannfeld',
        'l': 'l Mittenabstand der Stützpunkte',
        'l_i': 'l_i Länge einer Abspann-Isolatorkette',
        'l_h_f': 'l_h_f Länge einer Klemme u. Formfaktor',
        'a': 'a Leitermittenabstand',
        'a_s': 'a_s wirksamer Abstand zwischen Teilleitern',
        'F_st_20': 'Fst-20 statische Seilzugkraft in einem Hauptleiter',
        'F_st_80': 'Fst80 statische Seilzugkraft in einem Hauptleiter',
        'federkoeffizient_selected': 'S resultierender Federkoeffizient beider Stützpunkte im Spannfeld',
        'l_s_1': 'Abstand Phasenabstandshalter 1',
        'l_s_2': 'Abstand Phasenabstandshalter 2',
        'l_s_3': 'Abstand Phasenabstandshalter 3',
        'l_s_4': 'Abstand Phasenabstandshalter 4',
        'l_s_5': 'Abstand Phasenabstandshalter 5',
        'l_s_6': 'Abstand Phasenabstandshalter 6',
        'l_s_7': 'Abstand Phasenabstandshalter 7',
        'l_s_8': 'Abstand Phasenabstandshalter 8',
        'l_s_9': 'Abstand Phasenabstandshalter 9',
        'l_s_10': 'Abstand Phasenabstandshalter 10',
    },
    "Other Template.xlsx": {...},
}

def get_reverse_mapping(template_path: str | Path) -> dict[str, str]:
    # Wählt den key aus dem Dateinamen des Template-Pfades
    key = Path(template_path).name
    try:
        # Gibt das Reverse Mapping auf Basis des Keys zurück
        return REVERSE_FIELD_MAPPINGS[key]
    except KeyError as e:
        raise ValueError(f"No mapping for template: {key}") from e