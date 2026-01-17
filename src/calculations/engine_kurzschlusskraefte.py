from dataclasses import dataclass
from typing import Optional, Callable
import math
import scipy.constants
from . import berechnungen_kurzschlusskraefte as bkskls


@dataclass
class Kurschlusskräfte_Input:
    # Allgemeine Angaben
    leiterseilbefestigung: str
    schlaufe_in_spannfeldmitte: str
    hoehenunterschied_befestigungspunkte: str
    schlaufenebene_parallel_senkrecht: str
    temperatur_niedrig: int
    temperatur_hoch: int

    # Elektrische Werte
    standardkurzschlussstroeme: float
    κ: float
    t_k: float

    # Leiterseilkonfiguration
    leiterseiltyp: str
    d: float
    A_s: float
    m_s: float
    E: float
    c_th: float
    n: int
    m_c: Optional[float]

    # Abstände
    l: float
    l_i: Optional[float]
    a: float
    a_s: Optional[float]

    # Mechanische Kraftwerte
    F_st_20: float
    F_st_80: float
    federkoeffizient: int

    # Erweiterte Eingaben - Abstände Phasenabstandshalter
    l_s_1: Optional[float]
    l_s_2: Optional[float]
    l_s_3: Optional[float]
    l_s_4: Optional[float]
    l_s_5: Optional[float]
    l_s_6: Optional[float]
    l_s_7: Optional[float]
    l_s_8: Optional[float]
    l_s_9: Optional[float]
    l_s_10: Optional[float]

    def __post_init__(self):
        self.standardkurzschlussstroeme = self.standardkurzschlussstroeme * 10 ** 3
        self.d = self.d * 10 ** -3
        self.A_s = self.A_s * 10 ** -6
        self.E = self.E * 10 ** 6
        self.F_st_20 = self.F_st_20 * 10 ** 3
        self.F_st_80 = self.F_st_80 * 10 ** 3

@dataclass
class ShortCircuitResult:

    l_c: Optional[float] = None
    F_a: Optional[float] = None
    r: Optional[float] = None
    δ_1: Optional[float] = None
    f_es: Optional[float] = None
    T: Optional[float] = None
    T_res: Optional[float] = None
    E_eff: Optional[float] = None
    N: Optional[float] = None
    ζ: Optional[float] = None
    δ_end: Optional[float] = None
    δ_max: Optional[float] = None
    φ: Optional[float] = None
    ψ: Optional[float] = None
    F_td: Optional[float] = None
    ε_ela: Optional[float] = None
    ε_th: Optional[float] = None
    C_D: Optional[float] = None
    C_F: Optional[float] = None
    f_ed: Optional[float] = None
    F_fd: Optional[float] = None
    b_h: Optional[float] = None
    a_min: Optional[float] = None


    def convert_units(self):
        """Konvertiert berechnete Werte in die gewünschten Einheiten """
        if self.F_td is not None:
            self.F_td = self.F_td / 1000
        if self.F_fd is not None:
            self.F_fd = self.F_fd / 1000

class ShortCircuitMediator:
    def __init__(self, inputs: Kurschlusskräfte_Input):
        self.inputs = inputs
        self.results = ShortCircuitResult()
        self.mu0 = scipy.constants.mu_0
        self.g = scipy.constants.g
        self.σ_fin = 50 * 10**6
        
        # Lookup-Dictionary für Berechnungsmethoden
        self._calculation_matrix: dict[tuple, Callable] = {
            # (Leiterseilbefestigung, Schlaufe in Spannfeldmitte, Höhenunterschied, Schlaufenebene)
            ("Abgespannt", "Nein", "Nein", None): self.run_calculation_1_1,
            ("Abgespannt", "Nein", "Nein", ""): self.run_calculation_1_1,  # Fallback für leeren String
            ("Abgespannt", "Nein", "Ja", None): self.run_calculation_1_2,
            ("Abgespannt", "Nein", "Ja", ""): self.run_calculation_1_2,
            ("Abgespannt", "Ja", "Nein", "Ebene parallel"): self.run_calculation_2_1,
            ("Abgespannt", "Ja", "Nein", "Ebene senkrecht"): self.run_calculation_2_2,
            ("Abgespannt", "Ja", "Ja", "Ebene parallel"): self.run_calculation_2_3,
            ("Abgespannt", "Ja", "Ja", "Ebene senkrecht"): self.run_calculation_2_4,
            ("Aufgelegt", "Nein", "Nein", None): self.run_calculation_3_1,
            ("Aufgelegt", "Nein", "Nein", ""): self.run_calculation_3_1,
            # Weitere Kombinationen hier ergänzen ...
        }
    
    def select_and_run_calculation(self) -> dict[str, ShortCircuitResult]:
        """
        Wählt die passende Berechnungsmethode basierend auf den Eingabeparametern
        und führt die Berechnung aus.
        
        Returns:
            Dictionary mit Ergebnissen für F_st_20 und F_st_80
            
        Raises:
            ValueError: Wenn keine passende Berechnungsmethode gefunden wurde
        """
        # Normalisiere Schlaufenebene-Parameter (None wenn nicht relevant)
        schlaufenebene = self.inputs.schlaufenebene_parallel_senkrecht
        if self.inputs.schlaufe_in_spannfeldmitte == "Nein":
            schlaufenebene = None
        
        # Erstelle Lookup-Key
        key = (
            self.inputs.leiterseilbefestigung,
            self.inputs.schlaufe_in_spannfeldmitte,
            self.inputs.hoehenunterschied_befestigungspunkte,
            schlaufenebene
        )
        
        # Suche passende Berechnungsmethode
        calculation_method = self._calculation_matrix.get(key)
        
        if calculation_method is None:
            raise ValueError(
                f"❌ Keine Berechnungsmethode für diese Konfiguration gefunden:\n"
                f"  • Leiterseilbefestigung: {self.inputs.leiterseilbefestigung}\n"
                f"  • Schlaufe in Spannfeldmitte: {self.inputs.schlaufe_in_spannfeldmitte}\n"
                f"  • Höhenunterschied >25%: {self.inputs.hoehenunterschied_befestigungspunkte}\n"
                f"  • Schlaufenebene: {self.inputs.schlaufenebene_parallel_senkrecht or 'nicht relevant'}"
            )
        
        # Führe die ausgewählte Berechnung durch
        return calculation_method()

    def run_calculation_1_1(self) -> dict[str, ShortCircuitResult]:
        """
        Fall 1.1: Abgespannte Leiterseile ohne Schlaufe, ohne Höhenunterschied
        
        Anwendungsbereich:
        - Leiterseilbefestigung: Abgespannt
        - Schlaufe in Spannfeldmitte: Nein
        - Höhenunterschied >25%: Nein
        
        Norm: SN EN 60865-1:2012 Kapitel 6.2.3
        """
        results = {}
        
        for key, F_st in [('F_st_20', self.inputs.F_st_20), ('F_st_80', self.inputs.F_st_80)]:
            result = ShortCircuitResult()
            
            # Schritt 1: Effektive Seillänge
            result.l_c = bkskls.l_c(self.inputs.l, self.inputs.l_i)

            # Schritt 2: Charakteristischer elektromagnetischer Kraftbelag
            result.F_a = bkskls.F_a(self.mu0, self.inputs.standardkurzschlussstroeme, 
                                    self.inputs.l, result.l_c, self.inputs.a)
        
            # Schritt 3: Verhältnis r
            result.r = bkskls.r(result.F_a, self.inputs.n, self.inputs.m_s, self.g)
        
            # Schritt 4: Richtung δ_1
            result.δ_1 = bkskls.δ_1(result.r)
        
            # Schritt 5: Statischer Durchhang
            result.f_es = bkskls.f_es(self.inputs.n, self.inputs.m_s, self.g, self.inputs.l, F_st)
        
            # Schritt 6: Periodendauer
            result.T = bkskls.T(result.f_es, self.g)
        
            # Schritt 7: Resultierende Periodendauer
            result.T_res = bkskls.T_res(result.T, result.r, result.δ_1)
        
            # Schritt 8: Effektiver E-Modul
            result.E_eff = bkskls.E_eff(self.inputs.E, F_st, self.inputs.n, self.inputs.A_s, self.σ_fin)
        
            # Schritt 9: Steifigkeitsnorm
            result.N = bkskls.N(self.inputs.federkoeffizient, self.inputs.l, 
                               self.inputs.n, result.E_eff, self.inputs.A_s)
        
            # Schritt 10: Beanspruchungsfaktor
            result.ζ = bkskls.ζ(self.inputs.n, self.g, self.inputs.m_s, self.inputs.l, F_st, result.N)

            # Schritt 11: Ausschwingwinkel
            result.δ_end = bkskls.δ_end(result.δ_1, self.inputs.t_k, result.T_res)

            # Schritt 12: Maximaler Ausschwingwinkel
            result.δ_max = bkskls.δ_max(result.r, result.δ_end)

            # Schritt 13: Lastparameter φ
            result.φ = bkskls.φ_ohne_schlaufe(self.inputs.t_k, result.T_res, result.r, result.δ_end)

            # Schritt 14: Lastparameter ψ
            result.ψ = bkskls.ψ_ohne_schlaufe(result.φ, result.ζ)

            # Schritt 15: Kurzschluss-Seilzugkraft F_td
            result.F_td = bkskls.F_td_ohne_schlaufe_spannfeldmitte(F_st, result.φ, result.ψ)

            # Schritt 16: Elastische Seildehnung ε_ela
            result.ε_ela = bkskls.ε_ela(result.N, result.F_td, F_st)

            # Schritt 17: thermische Seildehnung ε_th
            result.ε_th = bkskls.ε_th(self.inputs.c_th, self.inputs.standardkurzschlussstroeme, self.inputs.n,
                                      self.inputs.A_s, self.inputs.t_k, result.T_res)

            # Schritt 18: Faktor Durchhangvergrößerung C_D
            result.C_D = bkskls.C_D(self.inputs.l, result.f_es, result.ε_ela, result.ε_th)

            # Schritt 19: Faktor Durchhangvergrößerung C_F
            result.C_F = bkskls.C_F(result.r)

            # Schritt 20: Dynamischer Seildurchhangs f_ed
            result.f_ed = bkskls.f_ed(result.C_D, result.C_F, result.f_es)

            # Schritt 21: Fall-Seilzugkraft F_fd
            result.F_fd = bkskls.F_fd(F_st, result.ζ, result.δ_max)

            # Schritt 22: Max. Horizontale Seilauslenkung b_h
            result.b_h = bkskls.b_h_ohne_schlaufe_spannfeldmitte_abgespannt(result.f_ed, result.δ_max, result.δ_1)

            # Schritt 23: Min. minimaler Leiterabstand a_min
            result.a_min = bkskls.a_min(self.inputs.a, result.b_h)


            # Einheitenkonvertierung
            result.convert_units()

            results[key] = result
        
        return results

    def run_calculation_1_2(self) -> dict[str, ShortCircuitResult]:
        """
        Fall 1.2: Abgespannte Leiterseile ohne Schlaufe, mit Höhenunterschied >25%
        
        Anwendungsbereich:
        - Leiterseilbefestigung: Abgespannt
        - Schlaufe in Spannfeldmitte: Nein
        - Höhenunterschied >25%: Ja
        
        Norm: SN EN 60865-1:2012 Kapitel 6.3
        """
        # TODO: Implementierung für Fall 1.2
        raise NotImplementedError("Fall 1.2 noch nicht implementiert")

    def run_calculation_2_1(self) -> dict[str, ShortCircuitResult]:
        """
        Fall 2.1: Abgespannte Leiterseile mit Schlaufe (Ebene parallel)
        
        Anwendungsbereich:
        - Leiterseilbefestigung: Abgespannt
        - Schlaufe in Spannfeldmitte: Ja
        - Schlaufenebene: Ebene parallel
        
        Norm: SN EN 60865-1:2012 Kapitel 6.2.5
        """
        # TODO: Implementierung für Fall 2.1
        raise NotImplementedError("Fall 2.1 noch nicht implementiert")

    def run_calculation_2_2(self) -> dict[str, ShortCircuitResult]:
        """
        Fall 2.2: Abgespannte Leiterseile mit Schlaufe (Ebene senkrecht)
        
        Anwendungsbereich:
        - Leiterseilbefestigung: Abgespannt
        - Schlaufe in Spannfeldmitte: Ja
        - Schlaufenebene: Ebene senkrecht
        
        Norm: SN EN 60865-1:2012 Kapitel 6.2.5
        """
        # TODO: Implementierung für Fall 2.2
        raise NotImplementedError("Fall 2.2 noch nicht implementiert")

    def run_calculation_2_3(self) -> dict[str, ShortCircuitResult]:
        """
        Fall 2.3: Abgespannte Leiterseile mit Schlaufe und Höhenunterschied (Ebene parallel)
        """
        # TODO: Implementierung für Fall 2.3
        raise NotImplementedError("Fall 2.3 noch nicht implementiert")

    def run_calculation_2_4(self) -> dict[str, ShortCircuitResult]:
        """
        Fall 2.4: Abgespannte Leiterseile mit Schlaufe und Höhenunterschied (Ebene senkrecht)
        """
        # TODO: Implementierung für Fall 2.4
        raise NotImplementedError("Fall 2.4 noch nicht implementiert")

    def run_calculation_3_1(self) -> dict[str, ShortCircuitResult]:
        """
        Fall 3.1: Aufgelegte Leiterseile ohne Schlaufe
        
        Anwendungsbereich:
        - Leiterseilbefestigung: Aufgelegt
        - Schlaufe in Spannfeldmitte: Nein
        
        Norm: SN EN 60865-1:2012 Kapitel 6.2.3
        """
        # TODO: Implementierung für Fall 3.1
        # Ähnlich wie 1.1, aber l_c = l (keine Isolatorkette)
        raise NotImplementedError("Fall 3.1 noch nicht implementiert")


def calculate_short_circuit(inputs: Kurschlusskräfte_Input) -> dict[str, ShortCircuitResult]:
    """
    Hauptfunktion zur Berechnung der Kurzschlusskräfte.
    
    Wählt automatisch die passende Berechnungsmethode basierend auf den Eingabeparametern.
    """
    mediator = ShortCircuitMediator(inputs)
    return mediator.select_and_run_calculation()
