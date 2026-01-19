import math
from dataclasses import asdict

def format_numbers_strings_scientific_and_normal(calc_result):
    """Formatiert Ergebnisse in zwei Spalten nebeneinander"""

    # Hilfsfunktion für intelligente Formatierung
    def format_scientific(value, threshold_low=0.001, threshold_high=1000):
        """
        Formatiert Werte intelligent:
        - Wissenschaftliche Notation für sehr kleine/große Werte
        - Normal für Werte zwischen threshold_low und threshold_high
        """
        if value == 0:
            return "0.00"

        abs_value = abs(value)

        # Verwende wissenschaftliche Notation nur für sehr kleine oder große Werte
        if abs_value < threshold_low or abs_value > threshold_high:
            exponent = int(math.floor(math.log10(abs_value)))
            mantissa = value / (10 ** exponent)
            # Verwende Unicode-Zeichen für Hochstellung
            exp_str = str(exponent).translate(str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻'))
            return f"{mantissa:.3f}×10{exp_str}"
        else:
            # Normale Formatierung für "vernünftige" Werte
            return f"{value:.3f}"

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
            # Formatiere die Werte intelligent
            val_20_str = format_scientific(val_20)
            val_80_str = format_scientific(val_80)
            lines.append(
                f"│ {param_name:<{col1_width}} │ {val_20_str:>{col2_width}} │ {val_80_str:>{col3_width}} │")

    lines.append(f"└─{'─' * col1_width}─┴─{'─' * col2_width}─┴─{'─' * col3_width}─┘")

    return "\n".join(lines)

def format_value_smart(value, threshold_low=0.001, threshold_high=1000):
    """
    Hilfsfunktion: Formatiert einen einzelnen Wert intelligent.
    Identisch zur Logik in formatter.py, aber als eigenständige Funktion.

    Args:
        value: Zu formatierender Wert
        threshold_low: Untere Schwelle für wissenschaftliche Notation
        threshold_high: Obere Schwelle für wissenschaftliche Notation

    Returns:
        Formatierter String
    """
    if value == 0:
        return "0.00"

    abs_value = abs(value)

    # Verwende wissenschaftliche Notation nur für sehr kleine oder große Werte
    if abs_value < threshold_low or abs_value > threshold_high:
        exponent = int(math.floor(math.log10(abs_value)))
        mantissa = value / (10 ** exponent)
        # Verwende Unicode-Zeichen für Hochstellung
        exp_str = str(exponent).translate(str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻'))
        return f"{mantissa:.3f}×10{exp_str}"
    else:
        # Normale Formatierung für "vernünftige" Werte
        return f"{value:.3f}"