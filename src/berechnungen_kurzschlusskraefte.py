import math
import scipy

# Konstanten
μ0 = scipy.constants.mu_0 # 4 * math.pi * 1e-7 ist auch möglich
g = scipy.constants.g # 4 * math.pi * 1e-7 ist auch möglich

# Zwischengrössen
def l_c(l: float, l_i: float) -> float:
    """
    Funktion zur Berechnung der Seillänge lc eines Hauptleiters im Spannfeld in m.
    Seilanordnungen in N/m nach SN EN 60865-1:2012 Kapitel 6.2.2.
    l_c: Seillänge eines Hauptleiters im Spannfeld m
    l_i: Länge einer Abspann-Isolatorkette m
    l_v: Seil(bogen)länge der Schlaufe m
    a: Leitermittenabstand in m
    Erläuterung zu lc:
    Bei Feldern mit aufgelegten Seilen, die Stützisolatoren auf Biegung beanspruchen, gilt lc = l. Bei Feldern mit
    abgespannten Seilen gilt lc = l − 2li, dabei ist li die Länge einer Abspann-Isolatorkette.
    (SN EN 60865-1:2012 Kapitel 6.2.2 Seite 26)
    """
    l_c: float = l - (2 * l_i)
    return l_c

def r(F_: float, n: float, m_s: float, g: float) -> float:
    """
    Funktion zur Berechnung Verhältnisses r der elektromagnetischen Kraft auf ein Leiterseil bei Kurzschluss zur
    Eigengewichtskraft (dimensionslos).
    F_: Seillänge eines Hauptleiters im Spannfeld m
    n: Anzahl der Teilleiter eines Hauptleiters (dimensionslos)
    m_s: Massenbelag eines Teilleiters kg/m
    g: Normfallbeschleunigung m/s^2
    """
    r: float = F_ / (n * m_s * g)
    return r

def δ_1(r: float) -> float:
    """
    Funktion zur Berechnung der Richtung δ1 der resultierenden Kraft in°.
    r: Verhältnisses r der elektromagnetischen Kraft auf ein Leiterseil bei Kurzschluss zur
    Eigengewichtskraft (dimensionslos)
    """
    r: float = math.atan(r)
    return r

# Hauptgrössen
def F(μ0: float, i1: float, i2: float, l: float, a: float) -> float:
    """
    Funktion zur Berechnung der Kraft F zwischen zwei parallelen, langen Leitern während eines Kurzschlusses in N
    nach SN EN 60865-1:2012 Kapitel 4.
    μ0: magnetische Feldkonstante, Permeabilität des leeren Raumes Vs/(Am)
    i1, i2: Augenblickswerte der Leiterströme in A
    l: Mittenabstand der Stützpunkte in m
    a: Leitermittenabstand in m
    Erläuterung zu F:
    Es werden die Kräfte zwischen parallelen Leitern angegeben. Die elektromagnetischen Kraftanteile, die durch
    abgewinkelte und/oder sich kreuzende Leiter auftreten, können im Allgemeinen vernachlässigt werden.
    (SN EN 60865-1:2012 Kapitel 4 Seite 11)
    """
    F: float = (μ0 / 2 * math.pi) * i1 * i2 * l * a
    return F

def F_(μ0: float, ik__: float, a: float, l: float, lc: float, lv: float) -> float:
    """
    Funktion zur Berechnung der Kraft F' Kraft charakteristischer elektromagnetischer Kraftbelag auf den Hauptleiter in
    Seilanordnungen in N/m nach SN EN 60865-1:2012 Kapitel 6.2.2.
    Bei Stromfluss über die gesamte Seillänge des Hauptleiters im Spannfeld mit und ohne Schlaufe mittel
    μ0: magnetische Feldkonstante, Permeabilität des leeren Raumes Vs/(Am)
    Ik′′: Anfangs-Kurzschlusswechselstrom (Effektivwert) beim dreipoligen Kurzschluss in A
    a: Leitermittenabstand in m
    l: Mittenabstand der Stützpunkte in m
    l_c: Seillänge eines Hauptleiters im Spannfeld m
    l_v: Seil(bogen)länge der Schlaufe m
    a: Leitermittenabstand in m
    Erläuterung zu lc:
    Bei Feldern mit aufgelegten Seilen, die Stützisolatoren auf Biegung beanspruchen, gilt lc = l. Bei Feldern mit
    abgespannten Seilen gilt lc = l − 2li, dabei ist li die Länge einer Abspann-Isolatorkette.
    (SN EN 60865-1:2012 Kapitel 6.2.2 Seite 26)
    """
    F: float = (μ0 / 2 * math.pi) * 0.75 * i1 * i2 * l * a
    return F




def testrechnungen() -> None:
    # Beispielrechnung gemäss Programm IEC 60865 FAU Projekt Riet→ Verifiziert
    print("l_c = ", l_c(l=31.0, l_i=5.25))
    # Nicht verifiziert!
    # Beispielrechnung gemäss Programm IEC 60865 FAU Projekt Riet→ Verifiziert
    print("r = ", r(F_=39.677, n=2, m_s=1.659, g=g))
    # Nicht verifiziert!
    # Beispielrechnung gemäss Programm IEC 60865 FAU Projekt Riet→ Verifiziert
    print("δ_1 = ", δ_1(r(F_=39.677, n=2, m_s=1.68, g=g)))


if __name__ == "__main__":
    testrechnungen()
