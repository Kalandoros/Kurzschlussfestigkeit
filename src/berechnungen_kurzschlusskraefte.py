import math
import scipy

# Konstanten
μ0 = scipy.constants.mu_0 # 4 * math.pi * 1e-7 ist auch möglich
g = scipy.constants.g # 9.81 ist auch möglich
σ_fin = 50 * 10**6 # σ_fin niedrigste Spannung, ab der der Elastizitätsmodul konstant wird in N/m^2

# Zwischengrössen
def l_c(l: float, l_i: float) -> float:
    """
    Funktion zur Berechnung der Seillänge lc eines Hauptleiters im Spannfeld in m nach SN EN 60865-1:2012 Kapitel 6.2.2
    l_c: Seillänge eines Hauptleiters im Spannfeld in m
    l: Mittenabstand der Stützpunkte in m
    l_i: Länge einer Abspann-Isolatorkette in m
    a: Leitermittenabstand in m
    Erläuterung zu lc:
    Bei Feldern mit aufgelegten Seilen, die Stützisolatoren auf Biegung beanspruchen, gilt lc = l. Bei Feldern mit
    abgespannten Seilen gilt l_c = l − 2 * l_i, dabei ist li die Länge einer Abspann-Isolatorkette.
    (SN EN 60865-1:2012 Kapitel 6.2.2 Seite 26)
    """
    l_c: float = l - (2 * l_i)
    return l_c

def r(F_: float, n: float, m_s: float, g: float) -> float:
    """
    Funktion zur Berechnung Verhältnisses r der elektromagnetischen Kraft auf ein Leiterseil bei Kurzschluss zur
    Eigengewichtskraft (dimensionslos) nach SN EN 60865-1:2012 Kapitel 6.2.2
    r: Verhältnis von elektromagnetischer Kraft auf ein Leiterseil bei Kurzschluss zur Eigengewichtskraft (dimensionslos)
    F_: charakteristischer elektromagnetischer Kraftbelag auf den Hauptleiter in Seilanordnungen in N/m
    n: Anzahl der Teilleiter eines Hauptleiters (dimensionslos)
    m_s: Massenbelag eines Teilleiters in kg/m
    g: Normfallbeschleunigung in m/s^2
    """
    r: float = F_ / (n * m_s * g)
    return r

def δ_1(r: float) -> float:
    """
    Funktion zur Berechnung der Richtung δ1 der resultierenden Kraft in ° nach SN EN 60865-1:2012 Kapitel 6.2.2
    δ_1: Richtung der resultierenden Kraft in °
    r: Verhältnisses r der elektromagnetischen Kraft auf ein Leiterseil bei Kurzschluss zur
    Eigengewichtskraft (dimensionslos)
    """
    r: float = math.atan(r)
    return r

def f_es(n: float, m_s: float, g: float, l: float, F_st: float) -> float:
    """
    Funktion zur Berechnung des statischen Ersatz-Seildurchhangs in Spannfeldmitte f_es in m
    nach SN EN 60865-1:2012 Kapitel 6.2.2
    f_es: statischer Ersatz-Seildurchhang in Spannfeldmitte in m
    n: Anzahl der Teilleiter eines Hauptleiters (dimensionslos)
    m_s: Massenbelag eines Teilleiters in kg/m
    g: Normfallbeschleunigung in m/s^2
    F_st: statische Seilzugkraft in einem Hauptleiter in N
    """
    f_es: float = (n * m_s * g * l**2) / (8 * F_st)
    return f_es

def T(f_es: float, g: float) -> float:
    """
    Funktion zur Berechnung der Periodendauer der Spannfeld-Pendelung T in s nach SN EN 60865-1:2012 Kapitel 6.2.2
    T: Periodendauer der Spannfeld-Pendelung in s
    f_es: statischer Ersatz-Seildurchhang in Spannfeldmitte in m
    g: Normfallbeschleunigung in m/s^2
    """
    T: float = 2 * math.pi * math.sqrt(0.8 * (f_es/g))
    return T

def T_res(T: float, r: float, δ_1: float) -> float:
    """
    Funktion zur Berechnung der resultierenden Periodendauer der Spannfeld-Pendelung T_res während des
    Kurzschlussstrom-Flusses in s nach SN EN 60865-1:2012 Kapitel 6.2.2
    T_res: resultierende Periodendauer der Spannfeld-Pendelung während des Kurzschlussstrom-Flusses in s
    T: Periodendauer der Spannfeld-Pendelung in s
    r: Verhältnisses r der elektromagnetischen Kraft auf ein Leiterseil bei Kurzschluss zur
    Eigengewichtskraft (dimensionslos)
    """
    T_res: float = T / ((math.sqrt(math.sqrt(1 + r**2)))*(1 - ((math.pi**2 / 64) * ((δ_1 / 90)**2))))
    return T_res

def E_eff(E: float, F_st: float, n: float, A_s: float, σ_fin: float) -> float:
    """
    Funktion zur Berechnung des tatsächlichen Elastizitätsmoduls E_eff in N/m^2 nach SN EN 60865-1:2012 Kapitel 6.2.2
    E_eff: tatsächlicher Elastizitätsmodul in N/m^2
    E: Elastizitätsmodul in N/m^2
    F_st: statische Seilzugkraft in einem Hauptleiter in N
    n: Anzahl der Teilleiter eines Hauptleiters (dimensionslos)
    A_s: Querschnitt eines Teilleiters in m^2
    σ_fin: niedrigste Spannung, ab der der Elastizitätsmodul konstant wird in N/m^2
    """
    E_eff: float = E *(0.3 + (0.7 * math.sin((F_st / (n * A_s * σ_fin) * 90))))

    if E_eff / (n * A_s) <= σ_fin:
        E_eff: float = E_eff
    elif E_eff / (n * A_s) > σ_fin:
        E_eff: float = E
    return E_eff

def N(S: float, l: float, n: float, E_eff: float, A_s: float) -> float:
    """
    Funktion zur Berechnung der Steifigkeitsnorm N einer Anordnung mit Leiterseilen in 1/N
    nach SN EN 60865-1:2012 Kapitel 6.2.2
    N: Steifigkeitsnorm einer Anordnung mit Leiterseilen in 1/N
    S: resultierender Federkoeffizient der beiden Stützpunkte eines Spannfelds in N/m
    l: Mittenabstand der Stützpunkte in m
    n: Anzahl der Teilleiter eines Hauptleiters (dimensionslos)
    E_eff: tatsächlicher Elastizitätsmodul in N/m^2
    A_s: Querschnitt eines Teilleiters in m^2
    """
    N: float = (1 / (S * l)) * (1 / (n * E_eff * A_s))
    return N

def ζ(n: float, g: float, m_s: float, l: float, F_st: float, N: float) -> float:
    """
    Funktion zur Berechnung des Faktors zur Berechnung von F_pi_d bei zusammenschlagenden Bündelleitern ξ
    (dimensionslos) nach SN EN 60865-1:2012 Kapitel 6.2.2
    ξ: Faktors zur Berechnung von F_pi_d bei zusammenschlagenden Bündelleitern (dimensionslos)
    n: Anzahl der Teilleiter eines Hauptleiters (dimensionslos)
    g: Normfallbeschleunigung in m/s^2
    m_s: Massenbelag eines Teilleiters in kg/m
    l: Mittenabstand der Stützpunkte in m
    F_st: statische Seilzugkraft in einem Hauptleiter in N
    N: Steifigkeitsnorm einer Anordnung mit Leiterseilen in 1/N
    """
    ζ: float = (n * g * m_s * l**2) / (24 * math.pow(F_st,3) * N)
    return ζ


# Hauptgrössen
def F(μ0: float, i_1: float, i_2: float, l: float, a: float) -> float:
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
    F: float = (μ0 / 2 * math.pi) * i_1 * i_2 * l * a
    return F

# TODO: noch offen
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
    print("σ_fin = ", σ_fin)

if __name__ == "__main__":
    testrechnungen()
