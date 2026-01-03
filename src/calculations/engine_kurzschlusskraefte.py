from dataclasses import dataclass
from typing import Optional
import math
import scipy.constants
from . import berechnungen_kurzschlusskraefte as bkk

@dataclass
class ShortCircuitInput:
    # Elektrische Werte
    I_k_double_prime: float  # Anfangs-Kurzschlusswechselstrom in kA
    t_k: float               # Kurzschlussdauer in s
    
    # Konfiguration
    n: int                   # Anzahl Teilleiter
    befestigung: str         # "Abgespannt" oder "Aufgelegt"
    
    # Geometrie
    l: float                 # Mittenabstand der Stützpunkte in m
    l_i: float               # Länge der Isolatorkette in m
    a: float                 # Leitermittenabstand in m
    a_s: float               # Abstand Teilleiter in m
    
    # Seileigenschaften (aus Datenbank/Dataloader)
    m_s: float               # Massenbelag eines Teilleiters in kg/m
    A_s: float               # Querschnitt eines Teilleiters in m^2
    E: float                 # Elastizitätsmodul in N/m^2
    
    # Mechanik
    F_st: float              # Statische Seilzugkraft in N (abhängig von Temperatur)
    S: float                 # Federkoeffizient der Stützpunkte in N/m (UI: Steifigkeitsnorm)

@dataclass
class ShortCircuitResult:
    l_c: Optional[float] = None
    F_a: Optional[float] = None
    r: Optional[float] = None
    delta_1: Optional[float] = None
    f_es: Optional[float] = None
    T: Optional[float] = None
    T_res: Optional[float] = None
    E_eff: Optional[float] = None
    N: Optional[float] = None
    zeta: Optional[float] = None
    F_td: Optional[float] = None
    f_ed: Optional[float] = None

class ShortCircuitMediator:
    def __init__(self, inputs: ShortCircuitInput):
        self.inputs = inputs
        self.results = ShortCircuitResult()
        self.mu0 = scipy.constants.mu_0
        self.g = scipy.constants.g

    def run_calculation(self) -> ShortCircuitResult:
        # Schritt 1: Effektive Seillänge
        if self.inputs.befestigung == "Abgespannt":
            self.results.l_c = bkk.l_c(self.inputs.l, self.inputs.l_i)
        else:
            self.results.l_c = self.inputs.l
            
        # Schritt 2: Charakteristischer Kraftbelag (kA -> A)
        I_k_A = self.inputs.I_k_double_prime * 1000
        self.results.F_a = bkk.F_a(self.mu0, I_k_A, self.inputs.l, self.results.l_c, self.inputs.a)
        
        # Schritt 3: Verhältnis r
        self.results.r = bkk.r(self.results.F_a, self.inputs.n, self.inputs.m_s, self.g)
        
        # Schritt 4: Richtung delta_1
        self.results.delta_1 = bkk.delta_1(self.results.r)
        
        # Schritt 5: Statischer Durchhang
        self.results.f_es = bkk.f_es(self.inputs.n, self.inputs.m_s, self.g, self.inputs.l, self.inputs.F_st)
        
        # Schritt 6: Periodendauer
        self.results.T = bkk.T(self.results.f_es, self.g)
        
        # Schritt 7: Resultierende Periodendauer
        self.results.T_res = bkk.T_res(self.results.T, self.results.r, self.results.delta_1)
        
        # Schritt 8: Effektiver E-Modul
        sigma_fin = 50e6 # Konstante aus bkk
        self.results.E_eff = bkk.E_eff(self.inputs.E, self.inputs.F_st, self.inputs.n, self.inputs.A_s, sigma_fin)
        
        # Schritt 9: Steifigkeitsnorm
        self.results.N = bkk.N(self.inputs.S, self.inputs.l, self.inputs.n, self.results.E_eff, self.inputs.A_s)
        
        # Schritt 10: Beanspruchungsfaktor
        self.results.zeta = bkk.zeta(self.inputs.n, self.g, self.inputs.m_s, self.inputs.l, self.inputs.F_st, self.results.N)
        
        # Hinweis: Hier fehlen noch Schritte für phi, psi und F_td im Detail, 
        # aber das Prinzip des Mediators ist nun sichtbar.
        # F_td Berechnung erfordert oft das Lösen von Gleichungen (psi).
        
        return self.results

def calculate_short_circuit(inputs: ShortCircuitInput) -> ShortCircuitResult:
    mediator = ShortCircuitMediator(inputs)
    return mediator.run_calculation()
