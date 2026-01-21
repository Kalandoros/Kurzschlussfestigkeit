import traceback

def get_error_location(tb):
    """
    Extrahiert Funktionsname und Zeilennummer aus Traceback.

    Args:
       tb: Traceback-Objekt der Exception

    Returns:
       str: Fehlerposition im Format " in Funktion 'name' (Zeile XX)" oder ""
    """
    error_location = ""
    for frame in tb:
        if "berechnungen_kurzschlusskraefte.py" in frame.filename:
            error_location = f" in Funktion '{frame.name}' (Zeile {frame.lineno})"
            break
        elif "engine_kurzschlusskraefte.py" in frame.filename:
            error_location = f" in '{frame.name}' (Zeile {frame.lineno})"
            break
    return error_location


def get_detailed_error_location(tb, max_frames=10):
    """
    Erstellt vollständige Call-Chain aus Traceback.

    Args:
        tb: Traceback-Objekt
        max_frames: Maximale Anzahl anzuzeigender Frames

    Returns:
        str: Call-Chain im Format "datei::funktion() → datei::funktion()
    """
    error_locations = []
    relevant_files = ["berechnungen_kurzschlusskraefte.py", "engine_kurzschlusskraefte.py",
                      "berechnungen_kurzschlussgroessen.py", "betriebsmittel.py"]

    # Sammle alle relevanten Frames
    for frame in tb:
        # Prüfe ob Frame aus einem unserer Calculation-Module kommt
        if any(file in frame.filename for file in relevant_files):
            file_name = frame.filename.split("\\")[-1]  # Nur Dateiname, nicht kompletter Pfad
            error_locations.append(f"{file_name}::{frame.name}() Zeile {frame.lineno}")

    # Begrenze auf max_frames
    if error_locations:
        if len(error_locations) > max_frames:
            error_locations = error_locations[-max_frames:]  # Nur die letzten N Frames

        # Formatiere als Chain
        chain = " → ".join(error_locations)
        return f"\n📍 {chain}"

    return ""


def format_exception_message(exception, show_chain=True):
    """
    Erstellt vollständige Call-Chain aus Traceback.

    Args:
        tb: Traceback-Objekt
        max_frames: Maximale Anzahl anzuzeigender Frames

    Returns:
        str: Call-Chain im Format "datei::funktion() → datei::funktion()
    """
    tb = traceback.extract_tb(exception.__traceback__)

    if show_chain:
        location = get_detailed_error_location(tb)
    else:
        location = get_error_location(tb)

    error_type = type(exception).__name__
    error_msg = str(exception)

    return f"❌ {error_type}{location}\n💬 {error_msg}"