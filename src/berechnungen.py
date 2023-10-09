import math


def κ_faktor(r_x: float, r: float, x: float) -> float:
    """
    Funktion zur Berechnung κ-Faktors zur Berechnung des Stosskurzschlussstromes (dimensionslos)
    r_x: Verhältnis R/X (dimensionslos)
    """
    κ = 1.02 + 0.98 * math.exp(r_x)
    return κ


def stosskurzschlussstrom(i_k3: float, κ: float) -> float:
    """
    Funktion zur Berechnung des Stosskurzschlussstromes ip in A
    i_k3: dreipoliger Anfangs-Kurzschlusswechselstrom (Effektivwert) in A
    κ: Faktor zur Berechnung des Stosskurzschlussstromes
    """
    i_p = κ * math.sqrt(2) * i_k3
    return i_p


def thermisch_gleichwertiger_kurzschlussstrom(i_k3: float, m: float, n: float) -> float:
    """
    Funktion zur Berechnung des thermisch gleichwertigen kurzschlussstromes

    """
    pass
    # i_th = math.sqrt((math.)) ^ 2
    # return i_th


if __name__ == "__main__":
    print(stosskurzschlussstrom(5000, 1.25))
