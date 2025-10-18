import math
import scipy
import sympy
import numpy
from numpy.ma.core import arccos
from rich.jupyter import display


# Konstanten
μ0 = scipy.constants.mu_0 # 4 * math.pi * 1e-7 ist auch möglich
g = scipy.constants.g # 9.81 ist auch möglich
σ_fin = 50 * 10**6 # σ_fin niedrigste Spannung, ab da der Elastizitätsmodul konstant wird in N/m^2

# Grössen ab Kapitel 6.2.2
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

def δ_end(δ_1: float, T_k1: float, T_kres: float) -> float:
    """
    Funktion zur Berechnung des Faktors δ_end zur Berechnung von bei Ausschwingwinkel am Ende des in
    Kurzschlussstrom-Flusses in ° nach SN EN 60865-1:2012 Kapitel 6.2.2
    T_k1: Dauer des ersten Kurzschlussstrom-Flusses ins s
    T_res:  resultierende Periodendauer der Spannfeld-Pendelung während des Kurzschlussstrom-Flusses ins s
    δ_end: Ausschwingwinkel am Ende des Kurzschlussstrom-Flusses in °
    """
    δ_end_1: float = δ_1 * (1 - math.cos(360*(T_k1 / T_kres)))
    δ_end_2: float = δ_1 * 2

    if 0 <= T_k1 / T_kres <= 0.5:
        δ_end: float = δ_end_1
        return δ_end
    elif T_k1 / T_kres > 0.5:
        δ_end: float = δ_end_2
        return δ_end

# TODO Hier ist noch was zu cracken wie man die IF-Schleife aufläust
def δ_max(r: float, δ_end: float, T_kres: float) -> float:
    """
    # Backminder: def δ_max(r: float, δ_end: float, T_kres: float) -> float:
    Funktion zur Berechnung des Faktors von x zur Berechnung Größe zur Berechnung des maximalen Ausschwingwinkels
    in (dimensionslos) nach SN EN 60865-1:2012 Kapitel 6.2.2
    r: Verhältnisses r der elektromagnetischen Kraft auf ein Leiterseil bei Kurzschluss zur Eigengewichtskraft (dimensionslos)
    δ_end: Berechnung von bei Ausschwingwinkel am Ende des in Kurzschlussstrom-Flusses in °
    χ: Größe zur Berechnung des maximalen Ausschwingwinkels (dimensionslos)
    Hinweis: Formeln zur Programmierung wird auf die Gleichungen (31) und (19) bis (30) verwiesen.
    """
    if 0 <= δ_end <= 90:
        χ_1: float = 1 - (r * math.sin(δ_end))
        x: float = χ_1
        if 0.766 < x <= 1:
            δ_max_1: float = 1.25 * arccos(x)
            δ_max: float = δ_max_1
            return δ_max
        elif -0.985 <= x <= 0.766:
            δ_max_2: float = 10 + arccos(x)
            δ_max: float = δ_max_2
            return δ_max
        elif x <= 1:
            δ_max_3: float = 180
            δ_max: float = δ_max_3
            return δ_max
    elif δ_end > 90:
        χ_2: float = 1 - r
        x: float = χ_2
        if 0.766 < x <= 1:
            δ_max_1: float = 1.25 * arccos(x)
            δ_max: float = δ_max_1
            return δ_max
        elif -0.985 <= x <= 0.766:
            δ_max_2: float = 10 + arccos(x)
            δ_max: float = δ_max_2
            return δ_max
        elif x <= 1:
            δ_max_3: float = 180
            δ_max: float = δ_max_3
            return δ_max
    return δ_max


# Grössen ab Kapitel 6.2.3
def φ(T_k1: float, T_kres: float, r: float, δ_end: float) -> float:
    """
    Funktion zur Berechnung des Faktors φ zur Berechnung Faktoren für die Berechnung der Zugkraft in Leiterseilen
    (dimensionslos) nach SN EN 60865-1:2012 Kapitel 6.2.3
    T_k1: Dauer des ersten Kurzschlussstrom-Flusses is s
    T_res: Resultierende Periodendauer der Spannfeld-Pendelung während des Kurzschlussstrom-Flusses ins s
    r: Verhältnisses r der elektromagnetischen Kraft auf ein Leiterseil bei Kurzschluss zur Eigengewichtskraft (dimensionslos)
    δ_end: Richtung der resultierenden Kraft in °
    """
    φ_1: float = 3 * (math.sqrt((1 + r**2)-1))
    φ_2: float = 3 * ((r * math.sin(δ_end)) - (math.cos(δ_end) - 1))

    if T_k1  >= T_kres / 4:
        φ: float = φ_1
        return δ_end
    elif T_k1  < T_kres / 4:
        φ: float = φ_2
    return φ

def ψ(φ: float, ζ: float) -> float:
    """
    Funktion zur Berechnung des Faktors ψ zur Berechnung Faktoren für die Berechnung der Zugkraft in Leiterseilen
    (dimensionslos) nach SN EN 60865-1:2012 Kapitel 6.2.3
    ψ: Faktoren für die Berechnung der Zugkraft in Leiterseilen (dimensionslos)
    φ: Faktoren für die Berechnung der Zugkraft in Leiterseilen (dimensionslos)
    ζ: Beanspruchungsfaktor des Hauptleiters in Seilanordnungen (dimensionslos)
    Hinweis: Es werden nur reale Zahlen und Zahlen zwischen 0 und 1 eingegeben.
    """
    ψ = sympy.symbols(names='ψ', real=True)
    polynom = (ψ**3 * φ**2) + ((φ * ( 2 + ζ)) * (ψ**2)) + (ψ * (1 + (2 * ζ))) - (ζ*(2 + φ))
    gl_Psi = sympy.solve(polynom, ψ)

    list_sol: [list] = []
    for i in gl_Psi:
        if  0 <= i <= 1:
            list_sol = list_sol.append(i)
        else:
            break
    return gl_Psi


# Grössen ab Kapitel 6.2.4
def ε_ela(N: float, F_td: float, F_st) -> float:
    """
    Funktion zur Berechnung der Wert ε_ela elastische Seildehnung (dimensionslos) nach SN EN 60865-1:2012 Kapitel 6.2.4.
    N: Steifigkeitsnorm einer Anordnung mit Leiterseilen in 1/N
    F_td: Kurzschluss-Seilzugkraft in einem Hauptleiter (Bemessungswert) in Seilanordnungen in N
    F_st: statische Seilzugkraft in einem Hauptleiter in N
    """
    ε_ela: float = N * (F_td - F_st)
    return ε_ela

# Grössen ab Kapitel 6.2.4
def ε_th(c_th: float, I_k__: float, n: float, A_s: float, T_k1: float, T_res: float) -> float:
    """
    Funktion zur Berechnung der Wert ε_th thermische Seildehnung (dimensionslos) nach SN EN 60865-1:2012 Kapitel 6.2.4.
    c_th: Materialkonstante in m4/(A2s)
    I_k__: Anfangs-Kurzschlusswechselstrom beim dreipoligen Kurzschluss (Effektivwert) in A
    n: Anzahl der Teilleiter eines Hauptleiters (dimensionslos)
    A_s: Querschnitt eines Teilleiters in m^2
    T_res:  resultierende Periodendauer der Spannfeld-Pendelung während des Kurzschlussstrom-Flusses ins s
    T_k1: Dauer des ersten Kurzschlussstrom-Flusses ins s
    """
    if T_k1 >= T_res / 4:
        ε_th: float =  c_th * (I_k__ / (n * A_s))**2 * (T_res / 4)
        return ε_th
    elif T_k1 < T_res / 4:
        ε_th: float = c_th * (I_k__ / (n * A_s)) ** 2 * (T_k1)
        return ε_th

# Grössen ab Kapitel 6.2.4
def C_D(l: float, f_es: float, ε_ela: float, ε_th: float) -> float:
    """
    Funktion zur Berechnung der Wert C_D Faktor für die Durchhangvergrößerung durch Seildehnung (dimensionslos) nach
    SN EN 60865-1:2012 Kapitel 6.2.4.
    l: Mittenabstand der Stützpunkte in m
    f_es: statischer Ersatz-Seildurchhang in Spannfeldmitte in m
    ε_ela: elastische Seildehnung (dimensionslos)
    ε_th: thermische Seildehnung (dimensionslos)
    """
    C_D: float = math.sqrt(1 + ((3 / 8) * (l / f_es)**2 * (ε_ela + ε_th)))
    return C_D

# Grössen ab Kapitel 6.2.4
def C_F(r: float) -> float:
    """
    Funktion zur Berechnung der Wert C_F Faktor für die Durchhangvergrößerung durch Änderung der Seilkurvenform
    (dimensionslos) nach SN EN 60865-1:2012 Kapitel 6.2.4.
    r: Verhältnisses r der elektromagnetischen Kraft auf ein Leiterseil bei Kurzschluss zur
    Eigengewichtskraft (dimensionslos)
    """
    if r <= 0.8:
        C_F: float = 1.05
        return C_F
    elif 0.8 < r < 1.8:
        C_F: float = 0.97 + 0.01 * r
        return C_F
    elif r >= 1.8:
        C_F: float = 1.15
        return C_F

# Grössen ab Kapitel 6.2.4
def f_ed(C_D: float, C_F: float, f_es: float) -> float:
    """
    Funktion zur Berechnung des Werts f_ed dynamischer Seildurchhang in Spannfeldmitte in m nach
    SN EN 60865-1:2012 Kapitel 6.2.4.
    f_es: statischer Ersatz-Seildurchhang in Spannfeldmitte in m
    C_D: Faktor für die Durchhangvergrößerung durch Seildehnung (dimensionslos)
    C_F: Faktor für die Durchhangvergrößerung durch Änderung der Seilkurvenform (dimensionslos)
    """
    f_ed: float = C_D * C_F * f_es
    return f_ed


# Grössen ab Kapitel 6.2.5 (Schlaufen)
def δ_ebene_parallel(f_es: float, f_ed: float, l_v: float, h: float, w: float) -> float:
    """
    Funktion zur Berechnung des Faktors δ_ebene_parallel zur Berechnung von bei Ausschwingwinkel am Ende des in
    Kurzschlussstrom-Flusses in ° bei Anordnung Ebene parallel nach SN EN 60865-1:2012 Kapitel 6.2.2
    f_es: statischer Ersatz-Seildurchhang in Spannfeldmitte in m
    f_ed: dynamischer Seildurchhang in Spannfeldmitte in m
    l_v: Seil(bogen)länge der Schlaufe in m
    h: Schlaufenhöhe in m
    w: Schlaufenbreite in m
    Hinweis: Wenn bei paralleler Ebene oder l h f w f bei senkrechter Ebene, dann ist nach 6.2.2 zu rechnen.
    """

    if l_v >= math.sqrt((h + f_es + f_ed)**2 + w**2):
        δ_ebene_parallel: float = arccos(((h +f_es)**2 + f_ed**2 - (l_v**2 - w**2)) / (2 * f_ed * (h +f_es)))
        return δ_ebene_parallel

# Grössen ab Kapitel 6.2.5 (Schlaufen)
def δ_ebene_senkrecht(f_es: float, f_ed: float, l_v: float, h: float, w: float) -> float:
    """
    Funktion zur Berechnung des Faktors δ_ebene_parallel zur Berechnung von bei Ausschwingwinkel am Ende des in
    Kurzschlussstrom-Flusses in ° bei Anordnung Ebene parallel nach SN EN 60865-1:2012 Kapitel 6.2.2
    f_es: statischer Ersatz-Seildurchhang in Spannfeldmitte in m
    f_ed: dynamischer Seildurchhang in Spannfeldmitte in m
    l_v: Seil(bogen)länge der Schlaufe in m
    h: Schlaufenhöhe in m
    w: Schlaufenbreite in m
    Hinweis: Wenn bei paralleler Ebene oder l h f w f bei senkrechter Ebene, dann ist nach 6.2.2 zu rechnen.
    """

    if l_v >= math.sqrt((h + f_es )**2 + w**2) + f_ed:
        δ_ebene_senkrecht: float = arccos(((h +f_es)**2 + f_ed**2 - (l_v**2 - w**2)) / (2 * f_ed * math.sqrt((h +f_es)**2 + w**2))) + arccos((h + f_es) / (math.sqrt((h +f_es)**2 + w**2)))
        return δ_ebene_senkrecht












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

# Grössen ab Kapitel 6.2.2
def F_a(μ0: float, I_k: float, l: float, l_c: float, a: float) -> float:
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
    Erläuterung zu lc:
    Bei Feldern mit aufgelegten Seilen, die Stützisolatoren auf Biegung beanspruchen, gilt lc = l. Bei Feldern mit
    abgespannten Seilen gilt lc = l − 2li, dabei ist li die Länge einer Abspann-Isolatorkette.
    (SN EN 60865-1:2012 Kapitel 6.2.2 Seite 26)
    """
    F_a: float = (μ0 / 2 * math.pi) * 0.75 * (I_k**2 / a) * (l_c / l)
    return F_a

# Grössen ab Kapitel 6.2.2
def F_b(μ0: float, I_k: float, l: float, l_c: float, l_v: float, a: float) -> float:
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
    Erläuterung zu lc:
    Bei Feldern mit aufgelegten Seilen, die Stützisolatoren auf Biegung beanspruchen, gilt lc = l. Bei Feldern mit
    abgespannten Seilen gilt lc = l − 2li, dabei ist li die Länge einer Abspann-Isolatorkette.
    (SN EN 60865-1:2012 Kapitel 6.2.2 Seite 26)
    """
    F_b: float = (μ0 / 2 * math.pi) * 0.75 * (I_k**2 / a) * (((l_c/2) + (l_v/2)) / l)
    return F_b

# Grössen ab Kapitel 6.2.3
def F_td(F_st: float, φ: float, ψ: float) -> float:
    """
    Funktion zur Berechnung der Kraft F_td Kurzschluss-Seilzugkraft in einem Hauptleiter (Bemessungswert) in
    Seilanordnungen in N nach SN EN 60865-1:2012 Kapitel 6.2.3.
    # Bei Stromfluss über die gesamte Seillänge des Hauptleiters im Spannfeld mit und ohne Schlaufe mittel
    F_st: statische Seilzugkraft in einem Hauptleiter in N
    φ: Faktoren für die Berechnung der Zugkraft in Leiterseilen (dimensionslos)
    ψ: Faktoren für die Berechnung der Zugkraft in Leiterseilen (dimensionslos)
    """
    F_td: float = F_st * (1 + (φ*ψ))
    return F_td


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
    print(ψ(φ= 3.29, ζ= 0.19))
    print(ψ(φ= 3.29, ζ= 0.3))

    print(ψ(φ= 13.86, ζ= 0.0))
    print(ψ(φ= 13.86, ζ= 0.1))

    print(ψ(φ= 5.78, ζ= 1.7))
    print(ψ(φ= 5.78, ζ= 3.9))

    print(ψ(φ= 1.57, ζ= 1.1))
    print(ψ(φ= 1.57, ζ= 2.7))