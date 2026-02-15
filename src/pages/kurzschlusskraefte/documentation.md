## Funktionen der Applikation
**Integrierte Funktionen:**

* Berechnung der Seilzugkräfte im Kurzschlussfall für horizontal abgespannte Leiterseile
* Berechnung der Seilzugkräfte im Kurzschlussfall für horizontal aufgelagte Leiterseile

**Nicht integrierte Funktionen (vorerst):**

* Berechnung der Seilzugkräfte im Kurzschlussfall für Unterschlaufungen
* Berechnung der Seilzugkräfte im Kurzschlussfall für horizontal abgespannte Leiterseile mit Schlaufen in Spannfeldmitte
* Berechnung der Seilzugkräfte im Kurzschlussfall für vertikal verlaufende Leiterseile
* Berechnung der Seilzugkräfte im Kurzschlussfall für Schlaufen am Spannfeldende

![Übersicht_Berechnungsfälle.png](/src/assets/kurzschlusskraefte_leiterseile/%C3%9Cbersicht_Berechnungsf%C3%A4lle.png)

## Geltungsbereich der Ergebnisse
Die Applikation ist nach [3] und [4] aufgebaut und entspricht deren Prinzipien.
Wie in [3] beschrieben, gelten die Berechnungen bei horizontal angeordneten Hauptleitern für Spannfeldlängen
bis ca. 120 m und bis zu einem Durchhang von 8% in Bezug auf die Spannfeldlänge.<br>
Weissen die Befestigungspunkte einen Höhenunterschied von > 25% bezogen auf die Spannfeldlänge auf, ist die Berechnung
als Schlaufe, im Sinne von vertikal verlaufenden Leiterseilen, durchzuführen.

## Seilzugkraft $F_{t,d}$ während des Kurzschlusses durch das Ausschwingen (Kurzschluss-Seilzugkraft)
Während eines mehrphasigen Kurzschlusses fliessen die Ströme in den betroffenen Leitern in entgegengesetzter Richtung, 
was eine gegenseitige Abstossung der Hauptleiter bewirkt. Diese elektromagnetische Kurzschlusskraft versetzt das Leiterseil in eine 
Schwingbewegung, wobei diese Bewegung als mechanisches Pendel beschrieben werden kann.
Die Kurzschluss-Seilzugkraft $F_{t,d}$ ist dabei die Überlagerung der elektromagnetischen Kurzschlusskraft, der 
Gewichtskraft des Seiles und der Zentrifugalkraft des sich bewegenden Leiterseils.

![Kurzschluss-Seilkraft.png](/src/assets/kurzschlusskraefte_leiterseile/Kurzschluss-Seilkraft.png)

Gemäss [2] wird die Kurzschluss-Seilzugkraft massgeblich durch das Kraftverhältnis $r$ (Verhältnis der 
elektromagnetischen Kraft auf ein Leiterseil zur Eigengewichtskraft) bestimmt. Der Höchstwert der 
Kurzschluss-Seilzugkraft tritt am äußeren Umkehrpunkt der ersten Schwingbewegung (Ausschwingmaximum) auf, 
sofern der Kurzschluss bis zu diesem Zeitpunkt anhält. 

## Seilzugkraft $F_{f,d}$ nach dem Kurzschluss durch das Fallen (Fall-Seilzugkraft) 
Nach dem Ausschalten des Kurzschlusses pendelt das Seil oder es fällt in seine Ruhelage zurück. Der 
Höchstwert $F_{f,d}$ der am Ende des Falles auftretenden Seilzugkraft ist nur bei $r > 0,6$ und $δ_{max} ≥ 70°$,
und bei einer Schlaufe in Spannfeldmitte, wenn $δ ≥ 60°$, zu berücksichtigen. Hintergrund dieser Bedingungen ist, 
das nach [1] das Seilfallen in den Versuchen erst beobachtet werden konnte, wenn der Leiter genügend Energie hat, 
was sich in den Ausschlagwinkeln $δ$ und $δ_{max}$ ausdrückt.Das bedeutet zusammengefasst:

* Fall-Seilzugkraft $F_{f,d}$ ohne Schlaufe in Spannfeldmitte zu berücksichtigen, wenn: $r > 0,6$ und $δ_{max} ≥ 70°$ 
ansonsten, wenn nicht beide Bedingungen zutreffen, ist die Fall-Seilzugkraft $F_{f,d}$ als unbedeutend anzunehmen
* Fall-Seilzugkraft $F_{f,d}$ mit Schlaufe in Spannfeldmitte zu berücksichtigen, wenn: $r > 0,6$ und $δ_{max} ≥ 70°$ und $δ ≥ 60°$
ansonsten, wenn nicht alle drei Bedingungen zutreffen, ist die Fall-Seilzugkraft $F_{f,d}$ als unbedeutend anzunehmen.

In [4] Beispiel Kapitel 9.3.2.5 können diese Bedingungen nachvollzogen werden. Sind die Bedingungen erfüllt, also muss
die Fall-Seilzugkraft $F_{f,d}$ berücksichtigt werden, wird davon ausgegangen, das die Auslenkung derart ausgeprägt ist,
das sich die Leiterseile überschlagen. 



Bei kurzen Spannfeldern vermindert die Biegesteifigkeit der Seile den Leiterseilfall. Deshalb wird die Fall-Seilzugkraft
zu gross berechnet, wenn die Spannfeldlänge den etwa 100-fachen Durchmesser des Einzelseils unterschreitet,
d.h. $l < 100 d$ ist. 

## Seilzugkraft $F_{pi,d}$ beim Kurzschluss durch Zusammenziehen der Teilleiter (Bündel-Seilzugkraft) 
In Bündelleitern fliesst der Kurzschlussstrom gleichphasig in den Teilleitern, was ein Zusammenziehen und Annähern
der Teilleiter zur Folge hat. Durch die horizontale Annäherung der Teilleiter und erhöht sich die Seilzugkraft an den 
Hauptleiterbefestigungen und lässt diese steigen. Durch das Zusammenschlagen der Teilleiter wird eine weitere Kontraktion 
der Teilleiter mit Auswirkungen auf die Seilzugkräfte an den Hauptleiterbefestigungen verhindert, sodass in diesem Fall eine 
Vergrösserung des Kurzschlussstromes keine bedeutende Vergrösserung der Bündel-Seilzugkraft zur Folge hat. Werden Abstandshalter zur 
Fixierung der Teilleiter eingebaut, ist das Zusammenschlagen erst bei höheren Kurzschlussströmen möglich, was zu einer 
entsprechend hohen Bündel-Seilzugkraft führt.

Bei regelmässigen Bündelleiteranordnungen bis einschliesslich vier Teilleitern wird die Bündel-Seilzugkraft 
mit $F_{pi,d}= 1,1 \,F_{t,d}$ berechnet, wenn einer der beiden folgenden Bedingungen erfüllt ist und damit nachgewiesen ist, 
das die Teilleiter wirksam zusammenschlagen.

* $a_s /d ≤ 2,0$ und $l_s /d ≥ 50 \,a_s$
* $a_s /d ≤ 2,5$ und $l_s /d ≥ 70 \,a_s$

Schlagen die Teilleiter während des Kurzschlusses nicht wirksam zusammen, gibt es zwei mögliche Berechnungspfade:

* $j ≥ 1.0$: Die Leiter schlagen zusammen bzw. berühren sich. Es wird die Formel mit dem Faktor $\xi$ (Gleichung A.9 Bild 11) verwendet.
* $j < 1.0$: Die Leiter nähern sich an, schlagen aber nicht zusammen. Hier wird das berechnete $\eta$ (Gleichung A.10 Bild 12) verwendet.

Je nach zutreffender Bedingung wird die Bündel-Seilzugkraft weiter nach [3] Kapitel 6.4.2 oder 6.4.3 berechnet. 
Folgend sind die drei möglichen Fälle Teilleiterseilkontraktionen aufgezeigt, welche den verschiedenen Berechnungswegen 
zugrunde liegen:
![Zusammenschlagen_Teilleiter.png](/src/assets/kurzschlusskraefte_leiterseile/Zusammenschlagen_Teilleiter.png)

In Abweichung von der Norm [3] wird unterschieden, ob Abstandhalter vorhanden sind oder nicht. 
Sind Abstandhalter vorhanden, wird nach [4] mit den gemittelten Abständen $l_s$ der Abstandshalter gerechnet. 
Falls keine Abstandhalter vorhanden sind, wird $l_c$, also die Seillänge eines Hauptleiters im Spannfeld
verwendet. Dieser Ansatz wurde mit dem Programm IEC865D verifiziert.

In den Diagrammen von [3] Bilder 12a-c werden verschiedene Kurven gezeigt, um den Einfluss der Seildehnung sichtbarer zu machen. 
Die Berechnung folgt strikt der analytischen Methode nach [3] Anhang A.10. Die beobachteten Abweichungen der
Berechnungen zu den Bildern 12a-c aus [3] resultieren aus der numerischen Exaktheit der Gleichung, die im Gegensatz 
zur grafischen Darstellung keine Linearisierungen zwischen den Verhältnissen von $a_s/d$ in den angegebenen Bereichen vornimmt. 
Die resultierenden Werte für $\eta$ wurden mit dem Programm IEC865D verifiziert.

## Einzellasten
Bei der Berechnung der Seilzugkräfte bei Kurzschluss durch Ausschwingen $F_{t,d}$ und Fallen $F_{f,d}$ des Spannfeldes
sowie bei der Seilauslenkung $b_{h}$ werden die Einzellasten gleichmässig auf die Seillänge verteilt. Sie werden dem 
Massenbelag des Leiterseiles als zusätzlicher Massenbelag hinzugefügt. Bei der Berechnung der Seilzugkraft durch 
Bündelkontraktion wird die zusätzliche Masse der Seilschlaufe in der Spannfeldmitte und ihrer 
Befestigung nicht berücksichtigt. [3] S.26, [1] S.11 Hintergrund ist, das Versuche gezeigt haben, das die 
Seilzugkräfte bei Berücksichtigung der Masse der Seilschlaufe in Spannfeldmitte dazu neigten, sich auf der unsicheren Seite
zu befinden. [1] S.9

Bei der Ermittlung der statischen Seilzugkraft $F_{st}$ und des statischen Durchhangs $f_{st}$ sollte der Beitrag 
konzentrierter Massen im Spannfeld, wie z.B. durch Abstandshalter, Klemmen, Schlaufen oder Gegenkontakte, berücksichtigt 
werden. Bei Schlaufen sollte dabei die Hälfte der Schlaufenmasse angesetzt werden. [3] S.26

## Schlaufen in Spannfeldmitte
Schlaufen in der Nähe der Hauptleiterbefestigungen (Hochgerüsten) haben geringen Einfluss auf die Seilzugkräfte beim Kurzschluss 
und die Bewegung des Hauptleiters. [1] S.3 In solchen Fällen ist die Berechnung ohne Schlaufe in Spannfeldmitte (in der Applikation 
"Schlaufe in Spannfeldmitte" mit Auswahl "Nein") durchzuführen. [1], [3] Als Richtlinie soll gelten, das Schlaufen als in der 
Nähe der Hauptleiterbefestigungen betrachtet werden, wenn sich diese im Bereich von 10% in Bezug auf die Spannfeldlänge 
an den äusseren Enden der Spannfeldlänge befinden.

Schlaufen in Spannfeldmitte werden berücksichtigt, wenn der obere Befestigungspunkt der Schlaufe bis zu 10% bezogen 
auf die Spannfeldlänge von der Mitte entfernt ist. D.h. für Schlaufen im Bereich der zentralen 20% der Spannfeldlänge 
wird eine Berechnung unter Berücksichtigung von Schlaufen in Spannfeldmitte (in der Applikation "Schlaufe in Spannfeldmitte" mit 
Auswahl "Ja") durchgeführt. 

Welche Berechnungsart (mit oder ohne Schlaufe in Spannfeldmitte) für die verbleibenden 60% der Spannfeldlänge 
angewendet wird, ist der Norm, den Beispielen zur Norm und der Literatur nicht zu entnehmen. Es wird in solchen Fällen
empfohlen, die Berechnung ohne Schlaufe in Spannfeldmitte durchzuführen. Üblicherweise ist der Einfluss der Schlaufen 
auf die Seilzugkräfte beim Kurzschluss gering [1] S.8f und ist hauptsächlich auf die höhere statische Seilzugkraft $F_{st}$ 
aufgrund der Berücksichtigung der Einzellast der Schlaufe (mit der halben Schlaufenmasse) zurückzuführen. [1] S.10
Lediglich die maximale horizontale Seilauslenkung $b_h$ der Hauptleiter wird ohne Berücksichtigung der Schlaufe in Spannfeldmitte
in der Tendenz zu gross berechnet, was zu kleineren minimalen Leiterabständen $a_min$ führt und damit im Sinne der Norm 
auf der sicheren Seite liegt. Dieser beschriebene Effekt wird jedoch durch die Berücksichtigung der Schlaufen in Spannfellmitte
im Bereich von mittleren 20% in Bezug auf die Spannfeldlänge "kompensiert", wo der Einfluss auf $b_h$ am grössten wäre.
So lässt sich die Herleitung einer ausreichenden Genauigkeit im Kontext der vereinfachten Berechnung der Seilzugkräfte nach
Norm SN EN 60865-1 nachvollziehen. Da der Einfluss der Schlaufe auf die Seilzugkräfte beim Kurzschluss und die daraus 
resultierenden Bewegungen des Hauptleiters mit zunehmender Entfernung von der Spannfeldmitte geringer wird, 
werden diese als unbedeutend angenommen. Dazu wird auf die Anmerkung 1 und 2 in Kapitel 6.2.5 in [3] verwiesen. 

Ebenso werden Schlaufen in Spannfeldmitte nicht berücksichtigt, wenn nach die Bedingungen nach [3] 
Kapitel 6.2.5 $l_v ≥ \sqrt{(h + f_{es} + f_{ed})^2 + w^2}$ bei parallel angeordneten Schlaufenebenen 
oder $l_v ≥ \sqrt{(h + f_{es} + f_{ed})^2 + w^2} +f_{ed}$ bei senkrecht angeordneten Schlaufenebenen erfüllt werden.
Ist eine der beiden genannten Bedingungen erfüllt, wird die Schlaufe in Spannfeldmitte nicht berücksichtigt, da der 
schräge Durchhang der Schlaufe zu gross ist, um die Seilzugkräfte beim Kurzschluss und die Bewegungen des Hauptleiters
dämpfend zu beeinflussen.

Für die Berechnung der Seilzugkräfte beim Kurzschluss mit Schlaufe in Spannfeldmitte werden die folgend 
aufgezeigten Kurzschlussstrompfade B und C berechnet und das Maximum der jeweiligen Seilzugkräfte ausgegeben, um beide 
Szenarien zu berücksichtigen. Im Hintergrund wird zusätzlich die Berechnung von Kurzschlussstrompfad A durchgeführt.

![Kurzschlusstrompfade.png](/src/assets/kurzschlusskraefte_leiterseile/Kurzschlusstrompfade.png)

Hinweis: Ist im Eingabefeld Seilbogenlänge $l_v$ im Programm keine Seilbogenlänge $l_v$ angegeben, wird die 
Seilbogenlänge $l_v$ über die empirische Gleichung $l_v = \sqrt{h^2 + w^2} \,1.05$ berechnet.

## Schlaufenebenen
Die Schlaufenebenen können parallel oder senkrecht zu den Hauptleitern angeordnet sein. Der tatsächliche Ausschwing-
winkel infolge der Begrenzung der Ausschwingbewegung wird durch die Anordnung der Schlaufe zu den Hauptleitern 
selbst beeinflusst. Es wird zwischen Schlaufen mit paralleler und senkrechter Anordnung zu den Hauptleitern unterschieden.
Aufgrund fehlender Konkretisierungen in [3] und [4], sowie in der weiterführenden Literatur, werden diese Anordnungen 
folgend näher erläutert:

* Ebene parallel: Die Schlaufe verläuft, aus der Draufsicht des Spannfeldes betrachtet, hauptsächlich in Richtung 
des Hauptleiters, also entlang der Hauptleiterachse. Der Winkel zwischen dem oberen und unteren Anschlusspunkt, 
aus der Draufsicht des Spannfeldes betrachtet, ist < 45°.

* Ebene senkrecht: Die Schlaufe verläuft, aus der Draufsicht des Spannfeldes betrachtet, hauptsächlich senkrecht zum Hauptleiter, 
also quer (senkrecht) zu den Hauptleitern. Der Winkel zwischen dem oberen und unteren Anschlusspunkt, aus der Draufsicht des Spannfeldes 
betrachtet, ist ≥ 45°.

Zur besseren Vorstellung von der Anordnung der Schlaufenebenen werden diese in der folgenden Abbildung dargestellt. 
Dabei ist blau die parallel zum Hauptleiter angeordnete Schlaufenebene, grün die senkrecht angeordnete Schlaufenebene 
und orange der Verlauf des Grenzwinkels von 45°. Rot sind die Positionen der Hochspannungsapparate bei paralleler und
senkrechter Anordnung der Schlaufenebenen dargestellt.

![Schlaufenebenen.png](/src/assets/kurzschlusskraefte_leiterseile/Schlaufenebenen.png)

Hinweis: Die Anordnung auf Schlaufenebene wird nur bei Berechnungen von Schlaufen in Spannfeldmitte berücksichtigt.

## Unterschlaufungen
Bei Unterschlaufungen handelt es sich um Verbindungen zwischen zwei Feldern mit abgespannten Leitungsseilen. 
Versuche haben gezeigt, dass die Schlaufe als eingespannt in den Seilklemmen betrachtet werden kann, und
der tiefste Punkt der Schlaufe sich auf einer Kreisbahn um einen Punkt unterhalb der Verbindungslinie
der Seilklemmen bewegt. [1], [7]

Die Einspannung verursacht eine Verformung der Ausschwingebene der Schlaufe, durch die ein Biegemoment 
im Seil der elektromagnetischen Kraft entgegenwirkt. Aus den Versuchsergebnissen wurde in [5] empirisch ermittelt,
dass dieses Moment bei der Berechnung des Parameters $r$ in Gleichung $r = \frac{F'}{1.2\,n \,m'_s\,g_n}$ durch eine 
Vergrösserung des Eigengewichtskraftbelags um 20% berücksichtigt werden kann. [1], [7]

## Federglieder
Federglieder sind im Programm nicht berücksichtigt. Die Steifgkeit der Federn kann jedoch der Steiﬁgkeit der 
Abspannung zugeschlagen werden. Mit den Federn ergibt sich ein resultierender Federkoefﬁzient beider Gerüste und der 
Abspannfedern zur Berechnung des statischen Durchhangs. [1], [7]
$$\frac{1}{S}= \frac{1}{S_{P1}}+\frac{1}{S_{P2}}+\frac{1}{S_{S1}}+\frac{1}{S_{S2}}$$

Während des Kurzschlußstromﬂusses erreichen die Federn ihre Endauslenkung und der resultierende Federkoefﬁzient 
springt auf einen wesentlich höheren Wert, der nur aus der Steiﬁgkeit der Gerüste folgt. [1], [7] 
$$\frac{1}{S}= \frac{1}{S_{P1}}+\frac{1}{S_{P2}}$$

## Resultierender Federkoeffizient

Die Formel $\frac{1}{S}= \frac{1}{S_{P1}}+\frac{1}{S_{P2}}$ gilt generell bei der Berechnung des resultierenden 
Federkoeffizienten der beiden Stützpunkte eines Spannfeldes. Die in [3] Kapitel 6.2.1 unter Anmerkung 3 gemachten 
Beispielwerte beziehen sich auf die Federkoeffizienten eines Abspanngerüstes, nicht beider Abspanngerüste. 
Folgend ist eine Beispielrechnung mit zwei Abspanngerüsten, welche den gleichen Federkoeffizienten aufweisen, aufgeführt:

$$S= \frac{1} {\frac{1}{S_{P1}}+\frac{1}{S_{P2}}}= \frac{1} {\frac{1}{1'000'000 \,N/m}+\frac{1}{1'000'000 \,N/m}}=500'000 \,N/m$$

## Designhinweise
* Eine zu kurz gewählte Schlaufe führt zwar zu einer Verringerung des Ausswingwinkels der Hauptleiter, jedoch auch zu höheren Seilzugkräften. [9]
* Bei Stützisolatoren oder Geräten mit Isolatoren sollte ein Sicherheitsfaktor von 0,7 gewählt werden. 
Untersuchungen an 110-kV-Isolatoren haben gezeigt, dass aufgrund von Alterungseffekten die Bruchlast mit zunehmenden Alter abnimmt. [7]
In ähnlicher Weise beschreibt es die Norm IEC 61869-1 für die Belastungen der Anschlüsse von Messwandlern. 
* Mit Ausnahme von Messwandlern werden gemäss den Normen für Hochspannungsapparate keine dynamischen Kräfte angegeben bzw. 
vorgeschrieben. Diese müssen beim Hersteller angefragt werden. Allenfalls müssen höhere Werte vereinbart werden.
* Bei der Bestimmung der statischen Seilzugkräfte $F_{st}$ sind Schlaufen als Einzellasten mit der Hälfte
des Leitergewichts der Schlaufe im Spannfeld zu berücksichtigen. [1], [2]
* Die Ergebnisse der Berechnungen der Seilzugkräfte beim Kurzschluss sind mit der Bruchlast des verwendeten Leiterseiles 
zu vergleichen.
* Der Einsatz und die Abstände von Abstandshaltern müssen wohlüberlegt werden. Zu kleine Abstände zwischen den Abstandshaltern
führen dazu, dass die Teilleiter erst bei hohen Kurzschlussströmen zusammenschlagen, was die Bündel-Seilzugkraft ansteigen lässt,
da das weitere Ansteigen der Kontraktionskräfte durch das Zusammenschlagen nicht verhindert wird. Das führt zu weiter 
ansteigenden Seilzugkräften. In der Literatur [6] S.238 werden für Abstände der Abstandshalter untereinander 5-10 m genannt,
wobei in der Tendenz eher 10 m anzustreben sind.
* Bei der Wahl der Teilleiterabstände ist zu berücksichtigen, dass die Bündel-Seilzugkraft mit zunehmen Teilleiterabständen 
zunimmt. Das ist dem Umstand geschuldet, das die Teilleiter bei grösseren Abständen erst später zusammenschlagen.
Für einen Vergleich zwischen den Teilleiterabständen wird auf [7] S.55 ff. und [8] verwiesen.
* Um unwirtschaftliche Konfigurationen mit hoher Bündel-Seilzugkraft zu vermeiden, sollten Teilleiterabstände und 
Abstandshalterabstände aufeinander abgestimmt werden. Je grösser die Teilleiterabstände, desto grösser auch die 
Abstände der Abstandshalter. 
* Der minimale Leiterabstand $a_{min}$ darf nach IEC 61936-1 50% spannungsabhängigen Abstände nicht unterschreiten.
* Die Positionierung eines Abstandhalters in der Spannfeldmitte, als kritische Stelle, kann als Ersatzmassnahme in 
Betracht gezogen werden, wenn der minimale Leiterabstand $a_{min}$ nicht erreicht werden kann. [9] S.148 Dabei sind jedoch
ca. 12% höhere Seilzugkräfte zu erwarten.

## Quellenverzeichnis

[1] Ergänzung des Berechnungsverfahrens nach IEC 60865-1VDE 0103 zur Ermittlung der Kurzschlußbeanspruchung von 
Leitungsseilen mit Schlaufen im Spannfeld, 2002 - FAU, Meyer

[2] PC-Programm für die Bemessung von Starkstromanlagen auf mechanische und thermische Kurzschlußfestigkeitnach, Bedienungsanleitung, 2006 - FAU, Herold, Jäger

[3] SN EN 60865-1:2012

[4] SN EN 60865-2:2017

[5] Das Spannfeld als physikalisches Pendel – eine analytische Lösung der Kurzschlußvorgänge, Archiv für Elektrotechnik, Ausgabe 70, 1987, S. 273–281 - Kießling

[6] Springer Handbook Power Systems, 1. Auflage, 2021 - Papailiou

[7] The mechanical effects of short-circuit currents in open air substations (part II), WG23.03, TB214, 2002 - Cigre

[8] Mechanische Wirkungen von Kurzschlusskräften bei Schaltanlagen mit Bündelleitern, Schlussbericht, AiF 12660, 2003 - FGH

[9] Test with Droppers and Interphase Spacers, 1998 - Declercq, 8th International Symposium on Short-Circuit Currents in Power Systems, Brussels