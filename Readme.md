

## Seilzugkraft $F_{f,d}$ nach dem Kurzschluss durch das Fallen (Fall-Seilzugkraft) 
Nach dem Ausschalten des Kurzschlusses pendelt das Seil oder es fällt in seine Ruhelage zurück. Der 
Höchstwert Ff,d der am Ende des Falles auftretenden Seilzugkraft ist nur zu berücksichtigen bei $r > 0,6$, 
wenn $δmax ≥ 70°$, und mit einer Schlaufe in Spannfeldmitte, wenn $δ ≥ 60°$.

[ ] Was der Satz genau bedeutet, muss nochmal genau durchdacht werden!

Bei kurzen Spannfeldern vermindert die Biegesteifigkeit der Seile den Seilfall; deshalb wird die Fall-Seilzugkraft
zu groß berechnet, wenn die Spannfeldlänge den etwa 100-fachen Durchmesser des Einzelseils 
unterschreitet, d. h. $l < 100 d$. 

## Einzellasten
Bei der Berechnung der Seilzugkräfte durch Ausschwingen und Fallen des Spannfeldes werden
die Einzellasten gleichmässig auf die Seillänge verteilt, bei der Berechnung der Seilzugkraft durch
Bündelkontraktion bleiben sie unberücksichtigt. [2]

## Unterschlaufungen
Unterschlaufungen verbinden zwei Felder mit abgespannten Leitungsseilen. 
Versuche haben gezeigt, dass die Schlaufe als eingespannt in den Seilklemmen betrachtet werden kann, und
der tiefste Punkt der Schlaufe sich auf einer Kreisbahn um einen Punkt unterhalb der Verbindungslinie
der Seilklemmen bewegt. [1]

Die Einspannung verursacht eine Verformung der Ausschwingebene der Schlaufe, durch die ein Biegemoment 
im Seil der elektromagnetischen Kraft entgegenwirkt. Aus den Versuchsergebnissen wird in [9] empirisch ermittelt,
dass dieses Moment bei der Berechnung des Parameters $r$ in Gleichung $r = \frac{F'}{1.2n m'_sg_n}$ durch eine 
Vergrösserung des Eigengewichtskraftbelags um 20% berücksichtigt werden kann. [1]

## Federglieder
Federglieder sind im Programm nicht berücksichtigt, die Steifgkeit der Federn kann jedoch der Steiﬁgkeit der 
Abspannung zugeschlagen werden. Mit den Federn ergibt sich ein resultierender Federkoefﬁzient beider Gerüste und der 
Abspannfedern zur Berechnung des statischen Durchhangs. [1] $\frac{1}{S}= \frac{1}{S_{P1}}+\frac{1}{S_{P2}}+\frac{1}{S_{S1}}+\frac{1}{S_{S2}}$

Während des Kurzschlußstromﬂusses erreichen die Federn ihre Endauslenkung und der resultierende Federkoefﬁzient springt auf einen wesentlich 
höheren Wert, der nur aus der Steiﬁgkeit der Gerüste folgt. [1] $\frac{1}{S}= \frac{1}{S_{P1}}+\frac{1}{S_{P2}}$

[1] Ergänzung des Berechnungsverfahrens nach IEC 60865-1VDE 0103 zur Ermittlung der Kurzschlußbeanspruchung von 
Leitungsseilen mit Schlaufen im Spannfeld, 2002 - FAU, Meyer

[2] PC-Programm für die Bemessung von Starkstromanlagen auf mechanische und thermische Kurzschlußfestigkeitnach, Bedienungsanleitung, 2006 - FAU

Formel zur Berechnung von $T_{pi}$, diese nicht in der Norm erwähnt ist.

$$T_{pi} = 1,15 \cdot \sqrt{\frac{m_s \cdot (a_s - d_s)}{F'_{pi}}}$$

Weitere Tipps:
Vorsicht bei math.radians()Du erwähntest math.sin(math.radians()). Das ist absolut korrekt für statische Winkel wie $180^\circ$ oder $90^\circ$.Aber Achtung: Die Terme in der Norm, die $\pi$ enthalten (z. B. $2\pi f T_{pi}$), sind bereits im Bogenmaß. Diese darfst du nicht noch einmal durch math.radians() jagen, sonst rechnet Python mit winzigen Werten weiter.

Richtig: $math.sin(math.pi / n)$ 

Falsch: $math.sin(math.radians(math.pi / n)$