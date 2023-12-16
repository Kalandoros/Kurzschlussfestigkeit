import math


def κ_faktor(r_x: float, r: float, x: float) -> float:
    """
    Funktion zur Berechnung κ-Faktors zur Berechnung des Stosskurzschlussstromes (dimensionslos) nach SN EN 60909-0
    r_x: Verhältnis R/X (dimensionslos)
    """
    κ = 1.02 + 0.98 * math.exp(r_x)
    return κ


def κ_faktor_alternativ(ip: float, ik__: float) -> float:
    """
    Funktion zur Berechnung κ-Faktors zur alternativen Berechnung des Stosskurzschlussstromes (dimensionslos) nach
    Umstellung der Formel des Stosskurzschlussstromes gemäss SN EN 60909-0 oder VDE Kurzschlussstromberechnung S. 269
    ip: Stosskurzschlussstrom (Augenblickswert) in A
    i_k__: dreipoliger oder zweipoliger Anfangs-Kurzschlusswechselstrom (Effektivwert) in A
    """
    κ = ip / (math.sqrt(2) * ik__)
    return κ


def stosskurzschlussstrom(ik__: float, κ: float = 2.0) -> float:
    """
    Funktion zur Berechnung des Stosskurzschlussstromes ip in A nach SN EN 60909-0
    i_k__: dreipoliger oder zweipoliger Anfangs-Kurzschlusswechselstrom (Effektivwert) in A
    κ: Faktor zur Berechnung des Stosskurzschlussstromes (dimensionslos)
    Erläuterung zu κ: In Niederspannungsnetzen darf das Produkt 1,15 κ auf 1,8 und in Hochspannungsnetzen auf 2,0
    begrenzt werden. (SN EN 60909-0 Kapitel 8.1.1)
    Daher wird κ = 2.0 als Standardwert verwendet, falls kein κ angegeben wird.
    """
    i_p = κ * math.sqrt(2) * ik__
    return i_p


def faktor_m(tk: float, f: float = 50.0, κ: float = 1.95) -> float:
    """
    Faktor für den Wärmeeffekt des Gleichstromanteils m (dimensionslos) nach SN EN 60909-0
    ik__: dreipoliger Anfangs-Kurzschlusswechselstrom (Effektivwert) in A
    f: Frequenz (50 Hz oder 60 Hz) in Hz
    tk: Dauer des Kurzschlussstromes in s
    κ: Faktor zur Berechnung des Stosskurzschlussstromes (dimensionslos)
    Erläuterung zu f: Daher wird f = 50.0 als Standardwert verwendet, falls kein f angegeben wird.
    Erläuterung zu κ: In Niederspannungsnetzen darf das Produkt 1,15 κ auf 1,8 und in Hochspannungsnetzen auf 2,0
    begrenzt werden. (SN EN 60909-0 Kapitel 8.1.1)
    Da κ = 2.0 zu unrealistisch hohen Gleichstromanteilen führt, wird κ = 1.95 als Standardwert verwendet,
    falls kein κ angegeben wird. (SN EN 60909-0 Kapitel 8.1.1 Bild 18)
    """
    m = (1 / (2 * f * tk * math.log(κ - 1))) * ((math.exp(4 * f * tk * math.log(κ - 1))) - 1)
    return m


def faktor_n(ik__: float, ik_: float, ik: float, tk: float) -> float:
    """
    Faktor für den Wärmeeffekt des Wechselstromanteils n (dimensionslos) nach SN EN 60909-0
    ik__: dreipoliger Anfangs-Kurzschlusswechselstrom (Effektivwert) in A

    ik: Dauerkurzschlussstrom (Effektivwert) in A
    tk: Dauer des Kurzschlussstromes in s
    κ:
    i_k: dreipoliger Anfangs-Kurzschlusswechselstrom (Effektivwert) in A
    Erläuterung zu ik__: Für die Berechnung des Joule-Integrals oder des thermisch gleichwertigen Kurzschlussstroms in
    Drehstromnetzen ist normalerweise der dreipolige Kurzschluss massgebend. (SN EN 60909-0 Kapitel 14)
    """
    pass
    # i_th = math.sqrt((math.)) ^ 2
    # return i_th


def thermisch_gleichwertiger_kurzschlussstrom(i_k3__: float, m: float, n: float, κ: float = 2.0) -> float:
    """
    Funktion zur Berechnung des thermisch gleichwertigen kurzschlussstromes nach SN EN 60909-0

    """
    pass
    # i_th = math.sqrt((math.)) ^ 2
    # return i_th


if __name__ == "__main__":
    print(stosskurzschlussstrom(5000, 1.25))
    print(stosskurzschlussstrom(31500))

    # Beispielrechnung gemäss VDE Kurzschlussstromberechnung S. 269 → Verifiziert
    print(κ_faktor_alternativ(ip=55.0, ik__=23.0))

    # Beispielrechnung gemäss SN EN 60909 - 0 Kapitel 8.1.1 Bild 18 → Verifiziert
    print("m =", faktor_m(tk=0.3, f=50.0, κ=1.95))
    # Beispielrechnung gemäss Siemens - Planungsleitfaden für Energieverteilungsanlagen S.59 → Verifiziert
    print("m =", faktor_m(tk=0.5, f=50.0, κ=1.8))
