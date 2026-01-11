

## Seilzugkraft $F_{f,d}$ nach dem Kurzschluss durch das Fallen (Fall-Seilzugkraft) 
Nach dem Ausschalten des Kurzschlusses pendelt das Seil oder es fällt in seine Ruhelage zurück. Der 
Höchstwert Ff,d der am Ende des Falles auftretenden Seilzugkraft ist nur zu berücksichtigen bei $r > 0,6$, 
wenn $δmax ≥ 70°$, und mit einer Schlaufe in Spannfeldmitte, wenn $δ ≥ 60°$.

Unter berücksichtigung von [4] Beipiel Kapitel 9.3.2.5 wird die Fall-Seilzugkraft nur als unbedeutend angenommen,
wenn die Berechnung der Kurzschluss-Seilzugkraft $F_{t,d}$ nach [3] Kapitel 6.2.5 erfolgt ist.

Bei kurzen Spannfeldern vermindert die Biegesteifigkeit der Seile den Seilfall; deshalb wird die Fall-Seilzugkraft
zu groß berechnet, wenn die Spannfeldlänge den etwa 100-fachen Durchmesser des Einzelseils 
unterschreitet, d. h. $l < 100 d$. 

## Seilzugkraft $F_{pi,d}$ beim Kurzschluss durch zusammenziehen der Teilleiter (Bündel-Seilzugkraft) 

Hinweis: Dieses Programm löst die analytische Gleichung A.10 exakt inklusive des Dehnungsterms $(1 + \varepsilon_{st})$. 
Die grafischen Näherungen in den Bildern 12a-c vernachlässigen diesen Term zur Vereinfachung, weshalb dieses Programm 
bei hohen Seildehnungen konservativere (sicherere) Werte liefert. Würde man den Term $(1 + \varepsilon_{st})$ in die 
Diagramme einbauen, wäre für jedes $a_s/d$ nicht nur ein Diagramm nötig, sondern ein ganzes Buch voll, weil die 
Kurven sich je nach Dehnung massiv verschieben würden. Mathematisch führt die Kombination aus Gleichung (58) und (A.10) dazu, 
dass sich die Dehnung $\varepsilon_{st}$ im Lastterm neutralisiert. In den Diagrammen werden verschiedene Kurven gezeigt, 
um den Einfluss der Seildehnung sichtbarer zu machen. In der Formel nach (A.10) wird dieser Einfluss jedoch direkt über 
den Parameter $j$ mitberücksichtigt, weshalb die grafische Aufteilung im Programm nicht erforderlich ist.
Die Berechnung folgt strikt der analytischen Methode nach IEC 60865-1, Anhang A.10. Die beobachteten Abweichungen zu den 
Bildern 12a-c resultieren aus der numerischen Exaktheit der Gleichung, die im Gegensatz zur grafischen Darstellung keine 
Linearisierungen vornimmt. Dies führt zu einer konservativen und damit sicherheitsgerichteten Auslegung.

Info:
Es zwei Pfade:$\eta < 1.0$: Die Leiter nähern sich an, schlagen aber nicht zusammen. 
Hier nutzt du dein berechnetes $\eta$.$\eta = 1.0$: Die Leiter schlagen zusammen (Clashing). 
Hier musst du auf die Formel mit dem Faktor $i_s$ (Gleichung 60) ausweichen.

## Einzellasten
Bei der Berechnung der Seilzugkräfte durch Ausschwingen und Fallen des Spannfeldes werden
die Einzellasten gleichmässig auf die Seillänge verteilt, bei der Berechnung der Seilzugkraft durch
Bündelkontraktion bleiben sie unberücksichtigt. [2], [3]
Die Masse der Seilschlaufe in Spannfeldmitte und ihrer Befestigung wird jedoch nicht berücksichtigt. [3]

Bei der Ermittlung der statischen Seilzugkraft Fst und des statischen Durchhangs fst sollte der Beitrag 
konzentrierter Massen im Spannfeld, z. B. durch Klemmen, Schlaufen oder Gegenkontakte, berücksichtigt 
werden. Bei Schlaufen sollte dabei die Hälfte der Schlaufenmasse angesetzt werden. [3]

## Schlaufenebenen
Die Schlaufenebenen können parallel oder senkrecht zu den Hauptleitern sein. Der tatsächliche Ausschwing-
winkel infolge der Begrenzung der Ausschwingbewegung wird durch die Anordnung der Schlaufe zu den Hauptleitern selbst beeinflusst.
Zur Unterscheidung von Schlaufen mit paralleler und senkrechter Anordnung der Schlaufe zu den Hauptleitern wird 
aufgrund fehlender Angaben in [3] und [4], sowie der weiterführenden Literatur, folgendes definiert:
- Parallel: Schlaufe verläuft hauptsächlich horizontal (Winkel zwischen oberem und unterem Anschlusspunkt < 45° ).
- Senkrecht: Schlaufe verläuft hauptsächlich vertikal (Winkel zwischen oberem und unterem Anschlusspunkt > 45°).

Hinweis: Die Schlaufenebene wird nur bei Schlaufen in Spannfeldmitte berücksichtigt.

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
Abspannfedern zur Berechnung des statischen Durchhangs. [1] $$\frac{1}{S}= \frac{1}{S_{P1}}+\frac{1}{S_{P2}}+\frac{1}{S_{S1}}+\frac{1}{S_{S2}}$$

Während des Kurzschlußstromﬂusses erreichen die Federn ihre Endauslenkung und der resultierende Federkoefﬁzient springt auf einen wesentlich 
höheren Wert, der nur aus der Steiﬁgkeit der Gerüste folgt. [1] $$\frac{1}{S}= \frac{1}{S_{P1}}+\frac{1}{S_{P2}}$$

[1] Ergänzung des Berechnungsverfahrens nach IEC 60865-1VDE 0103 zur Ermittlung der Kurzschlußbeanspruchung von 
Leitungsseilen mit Schlaufen im Spannfeld, 2002 - FAU, Meyer

[2] PC-Programm für die Bemessung von Starkstromanlagen auf mechanische und thermische Kurzschlußfestigkeitnach, Bedienungsanleitung, 2006 - FAU

[3] SN EN 60865-1:2012

[3] SN EN 60865-2:2017

Formel zur Berechnung von $T_{pi}$, diese nicht in der Norm erwähnt ist.

$$T_{pi} = 1,15 \cdot \sqrt{\frac{m_s \cdot (a_s - d_s)}{F'_{pi}}}$$

Weitere Tipps:
Vorsicht bei math.radians()Du erwähntest math.sin(math.radians()). Das ist absolut korrekt für statische Winkel wie $180^\circ$ oder $90^\circ$.Aber Achtung: Die Terme in der Norm, die $\pi$ enthalten (z. B. $2\pi f T_{pi}$), sind bereits im Bogenmaß. Diese darfst du nicht noch einmal durch math.radians() jagen, sonst rechnet Python mit winzigen Werten weiter.

Richtig: $math.sin(math.pi / n)$ 

Falsch: $math.sin(math.radians(math.pi / n)$