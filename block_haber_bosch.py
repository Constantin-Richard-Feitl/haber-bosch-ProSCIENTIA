# -*- coding: utf-8 -*-
"""
Block 1: Dünger aus Luft.

Roter Faden:
  K1  Der Rohstoff ist überall und niemand kommt heran.
  K2  Warum nicht. Ein einziger Maßstab erklärt es.
  K3  Der Ausweg ist kein größerer Druck, sondern ein anderer Weg.
  K4  Was Haber und Bosch daraus gemacht haben, im Guten wie im Bösen.
"""

import numpy as np
import streamlit as st

from bausteine import (
    BLAU, ORANGE, DUNKELGRAU, KJ_ZIMMER,
    balken_vergleich, boltzmann_anteil, seltenheit_anzeigen,
    wellenlaenge_nm, fachkasten, merksatz, kapitel_kopf, neue_figur,
    zeige, hoch, dez, schaetzfrage,
)

KAPITEL = [
    "1 · Ein Meer aus Stickstoff",
    "2 · Warum Luft nicht düngt",
    "3 · Der Katalysator",
    "4 · Haber und Bosch",
]
N_KAP = len(KAPITEL)

# Gemessene Bindungsenergien in kJ/mol (Tabellenwerte, 298 K)
BINDUNGEN = [
    ("N≡N   im Stickstoff", 945),
    ("C≡O   im Kohlenmonoxid", 1077),
    ("C=O   im Kohlendioxid", 799),
    ("O=O   im Sauerstoff", 498),
    ("H–H   im Wasserstoff", 436),
    ("C–C   im Diamant", 346),
    ("N–H   im Ammoniak", 391),
]


def zeichne(kapitel):
    [_k1, _k2, _k3, _k4][KAPITEL.index(kapitel)]()


# ==================================================================
# Kapitel 1
# ==================================================================
def _k1():
    kapitel_kopf(1, N_KAP, "Ein Meer aus Stickstoff",
                 "Der Rohstoff ist überall. Das ist genau das Problem.")

    st.markdown(
        """
Die Luft in diesem Raum besteht zu **78 Prozent aus Stickstoff**. Mit jedem
Atemzug ziehst du Milliarden Stickstoffmoleküle ein und atmest sie unverändert
wieder aus.

Gleichzeitig ist Stickstoff der Nährstoff, an dem Pflanzenwachstum als Erstes
scheitert. Er steckt in jedem Eiweiß, in jedem Stück DNA und in jedem Muskel.
"""
    )
    merksatz("Der Rohstoff ist überall und niemand kommt an ihn heran.")

    st.markdown(
        """
Über Jahrtausende war Stickstoff deshalb ein Engpass. Man sammelte Mist, holte
Guano von südamerikanischen Inseln und baute Salpeter in der Atacama-Wüste ab.
Um 1900 war absehbar, dass diese Quellen für eine wachsende Weltbevölkerung
nicht mehr reichen würden.

1909 löste Fritz Haber das Problem im Labor, 1913 baute Carl Bosch daraus eine
Fabrik. Die Reaktion, um die sich alles dreht, sieht harmlos aus:
"""
    )
    st.latex(r"\mathrm{N_2} + 3\,\mathrm{H_2} \;\longrightarrow\; "
             r"2\,\mathrm{NH_3}")
    st.markdown(
        "Links stehen zwei Gase, die es im Überfluss gibt. Rechts steht "
        "Ammoniak, aus dem Dünger wird."
    )

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Stickstoff in der Luft", "78 %")
    m2.metric("Menschen, die davon leben", "≈ 48 %")
    m3.metric("Anteil am Weltenergiebedarf", "1 bis 2 %")
    st.caption(
        "Rund die Hälfte der Menschheit isst heute Nahrung, deren Stickstoff "
        "aus diesem einen Verfahren stammt. Es verbraucht dafür ein bis zwei "
        "Prozent der gesamten von der Menschheit erzeugten Energie. "
        "(Quelle: *Green ammonia synthesis*, Nature Synthesis 2023.)"
    )

    st.divider()
    st.markdown(
        "Warum das über hundert Jahre lang trotzdem niemand hinbekommen hat, "
        "liegt an etwas, das man nicht sieht. Darum geht es im nächsten "
        "Kapitel."
    )


# ==================================================================
# Kapitel 2
# ==================================================================
def _k2():
    kapitel_kopf(2, N_KAP, "Warum Luft nicht düngt",
                 "Gleich kommen Energien ins Spiel. Dafür braucht es keine "
                 "Einheitenkunde, sondern einen einzigen Maßstab.")

    st.markdown(
        """
Stickstoff kommt in der Luft nie einzeln vor, sondern immer paarweise als
**N₂**. Die beiden Atome halten sich mit einer **Dreifachbindung** aneinander
fest, also mit drei Elektronenpaaren gleichzeitig. Es ist die stärkste
Bindung, die zwei gleiche Atome miteinander eingehen können.

Bevor Stickstoff düngen kann, muss diese Bindung auf. Vorher passiert nichts.
"""
    )

    # -------------------------------------------------- Schätzfrage
    st.divider()
    st.subheader("Erst raten")
    _, aufgeloest = schaetzfrage(
        "n2_vs_h2",
        "Wie viel mehr Aufwand kostet es, N≡N zu brechen als H–H, die "
        "Bindung im Wasserstoff?",
        1.0, 8.0, 3.0, 0.1, 945 / 436,
        einheit="mal so viel", format_str="%.1f", toleranz_gut=0.35,
        aufloesung_text=(
            "Der Faktor ist **2,2**. Die meisten tippen höher, weil eine "
            "Dreifachbindung nach dreimal so viel klingt. Der Unterschied "
            "zwischen den Bindungen ist gar nicht das Erstaunliche an dieser "
            "Geschichte."
        ),
    )

    if aufgeloest:
        zeige(balken_vergleich(BINDUNGEN,
                               hervorheben="N≡N   im Stickstoff"))
        st.caption(
            "N≡N ist stark, steht aber nicht allein an der Spitze. "
            "Kohlenmonoxid hält sogar noch fester zusammen. Der entscheidende "
            "Vergleich ist ein anderer."
        )

    # -------------------------------------------------- der Maßstab
    st.divider()
    st.subheader("Der einzige Maßstab, den du brauchst")
    st.markdown(
        f"""
Bindungsstärken werden in **kJ/mol** angegeben. Diese Einheit sagt niemandem
etwas, der nicht täglich damit arbeitet. Sie muss es auch nicht. Es gibt
einen einzigen Vergleichswert, der alles Weitere trägt:

**Wie viel Energie bekommt ein Molekül von der Umgebungswärme mit?**

Wärme ist nichts anderes als Bewegung. Je wärmer es ist, desto heftiger
zappeln die Moleküle und desto härter stoßen sie zusammen. Bei 20 °C liegt
diese Energie in der Größenordnung von **{dez(KJ_ZIMMER)} kJ/mol**. Das ist
das Kleingeld, mit dem die Chemie bei Zimmertemperatur einkaufen geht.
"""
    )

    fig, ax = neue_figur(1.9)
    ax.barh([1], [945], color=ORANGE, height=0.55)
    ax.barh([0], [KJ_ZIMMER], color=BLAU, height=0.55)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Wärme im Raum\nliefert", "N≡N\nverlangt"])
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Energie  [kJ/mol]")
    ax.text(960, 1, "945", va="center", fontsize=10, color=DUNKELGRAU)
    ax.annotate("2,4", xy=(KJ_ZIMMER, 0), xytext=(120, 0), va="center",
                fontsize=9, color=BLAU,
                arrowprops=dict(arrowstyle="->", color=BLAU, lw=1.2))
    ax.set_xlim(0, 1080)
    zeige(fig)

    # -------------------------------------------------- Boltzmann
    st.divider()
    st.subheader("Wärme ist aber nicht gleich verteilt")
    st.markdown(
        f"""
{dez(KJ_ZIMMER)} kJ/mol ist ein **Durchschnitt**. Manche Moleküle sind viel
langsamer, manche viel schneller. In jeder Sekunde gibt es Ausreißer weit über
dem Schnitt. Ob es davon genug gibt, sagt der Regler.
"""
    )

    temp = st.slider("Temperatur", 20, 3000, 20, 10, format="%d °C",
                     key="t_boltzmann")
    seltenheit_anzeigen(boltzmann_anteil(945.0, temp),
                        kontext=f", um N≡N bei {temp} °C zu brechen")

    if temp >= 1500:
        st.warning(
            "**Bei dieser Temperatur ginge es tatsächlich los.** Nur ist das "
            "kein Weg, denn Ammoniak selbst hält solche Temperaturen nicht "
            "aus. Man würde die Bindung knacken und das Produkt im selben "
            "Moment wieder zerlegen."
        )

    merksatz(
        "Bei Zimmertemperatur, also dort wo Pflanzen wachsen und wo die Luft "
        "steht, heißt diese Zahl nicht <i>selten</i>. Sie heißt <i>nie</i>."
    )

    # -------------------------------------------------- Licht
    st.divider()
    st.subheader("Warum auch die Sonne nicht hilft")
    lam = wellenlaenge_nm(945.0)
    st.markdown(
        f"""
Wärme ist nicht die einzige Energiequelle. Ein Lichtteilchen trägt seine
Energie in einem einzigen Paket und muss nichts zusammensparen. Um N≡N in
einem Schlag zu knacken, bräuchte es eine Wellenlänge von **{lam:.0f}
Nanometern**.
"""
    )
    c1, c2 = st.columns(2)
    c1.metric("Nötige Wellenlänge", f"{lam:.0f} nm")
    c2.metric("Was dein Auge noch sieht", "380 bis 750 nm")
    st.markdown(
        "Das ist tiefes Ultraviolett. Diese Strahlung wird in der hohen "
        "Atmosphäre vollständig weggefiltert, unter anderem von Stickstoff "
        "und Sauerstoff selbst."
    )
    merksatz(
        "Sonnenlicht am Boden kann Stickstoff nicht aufbrechen. Wäre es "
        "energiereich genug, gäbe es uns nicht."
    )
    st.caption(
        "Diese Rechnung kommt im Block Quantenwelt noch einmal vor. Dort "
        "wird aus einem Energieunterschied eine Farbe, mit derselben Formel."
    )

    st.divider()
    st.markdown(
        """
### Wo wir jetzt stehen

Hitze reicht nicht, Licht reicht nicht und Warten hilft schon gar nicht. Nach
diesem Kapitel sieht es aus, als sei die Sache erledigt.

Sie ist es nicht. Es gibt einen Ausweg. Er besteht nicht darin, fester zu
drücken.
"""
    )

    fachkasten(
        "Die Zahlen dahinter",
        """
**Bindungsdissoziationsenergien** (Tabellenwerte, 298 K): N≡N 945 kJ/mol,
C≡O 1077, C=O 799, O=O 498, H–H 436, N–H 391, C–C 346 kJ/mol.

**Thermische Energie**: *RT* mit *R* = 8,314 J/(mol·K). Bei 293 K sind das
2,44 kJ/mol, das Verhältnis 945 / 2,44 ist also rund 388. Die mittlere
kinetische Energie eines Gasteilchens ist mit 3/2 *RT* etwas größer, für eine
Größenordnungsbetrachtung ändert das nichts.

**Der Anteil energiereicher Moleküle** ist der Boltzmann-Faktor
*f* = e^(−E<sub>A</sub>/*RT*). Bei 293 K und E<sub>A</sub> = 945 kJ/mol ergibt
das 4 · 10⁻¹⁶⁹. Das ist eine Abschätzung der Größenordnung und keine
Reaktionsgeschwindigkeit. Dafür bräuchte es zusätzlich Stoßfrequenz und
Orientierungsfaktor. Beide verschieben das Ergebnis um wenige Zehnerpotenzen
und an der Aussage nichts.

**Photonenenergie**: *E* = *hc*/λ. 945 kJ/mol entsprechen 9,79 eV pro Molekül
und damit λ = 127 nm, also Vakuum-UV.

**1 eV = 96,485 kJ/mol.** Diese Umrechnung verbindet das Kapitel mit dem Block
Quantenwelt, wo alles in eV gerechnet wird.
""",
    )


# ==================================================================
# Kapitel 3
# ==================================================================
def _k3():
    kapitel_kopf(3, N_KAP, "Der Katalysator",
                 "Nicht fester drücken, sondern außen herum.")

    st.markdown(
        """
Im letzten Kapitel stand die Bindung wie eine Wand im Weg. Sie verlangt
945 kJ/mol, die Wärme im Raum liefert 2,4. Über die Wand kommt man nicht.

Die Lösung ist deshalb keine größere Kraft, sondern ein **anderer Weg**. Ein
Katalysator bricht die Bindung nicht auf. Er bietet dem Molekül eine Route an,
auf der es die Wand gar nicht überqueren muss.
"""
    )

    with st.expander("**Was am Eisen tatsächlich passiert**"):
        st.markdown(
            """
Der Katalysator ist Eisen mit ein paar Zusätzen. Auf seiner Oberfläche gibt es
Stellen, an denen sich ein Stickstoffmolekül festsetzt. Dabei greifen die
Eisenatome mit ihren eigenen Elektronen in die Dreifachbindung hinein und
lockern sie.

Was dann folgt, geschieht in vielen kleinen Schritten. Das N₂ zerfällt auf der
Oberfläche in zwei einzelne, festgehaltene Stickstoffatome. Wasserstoff setzt
sich daneben. Dann wandert ein H-Atom zum N-Atom, dann das nächste, dann das
dritte. Erst am Ende löst sich fertiges NH₃ ab.

Statt einer hohen Wand also eine Treppe mit lauter niedrigen Stufen. Am Ende
ist derselbe Punkt erreicht, aber kein einzelner Schritt musste die volle Höhe
schaffen.

Aufgeklärt hat diesen Mechanismus Gerhard Ertl. Er bekam dafür 2007 den
Nobelpreis für Chemie, fast hundert Jahre nachdem das Verfahren schon
industriell lief.
"""
        )

    st.divider()
    st.subheader("Was das für die Chancen bedeutet")
    st.markdown(
        "Der linke Regler senkt die Hürde, die ein Molekül nehmen muss. Die "
        "Temperatur bleibt dabei gleich. Verändert wird nur der Weg."
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        barriere = st.slider("Höhe der Hürde [kJ/mol]", 50, 945, 945, 5,
                             key="barriere")
    with c2:
        t_kat = st.slider("Temperatur [°C]", 20, 600, 450, 10, key="t_kat")

    if barriere > 800:
        st.caption("**Ganz rechts:** keine Hilfe, blanke Gasphase, also die "
                   "volle Dreifachbindung.")
    elif barriere > 250:
        st.caption("**Mitte:** ein mäßiger Katalysator.")
    else:
        st.caption("**Um 100 kJ/mol:** ungefähr dort liegt ein technischer "
                   "Eisenkatalysator.")

    seltenheit_anzeigen(boltzmann_anteil(barriere, t_kat),
                        kontext=f", um die Hürde bei {t_kat} °C zu nehmen")

    ohne = boltzmann_anteil(945.0, t_kat)
    mit = boltzmann_anteil(barriere, t_kat)
    if mit > 0 and ohne > 0 and barriere < 900:
        st.success(
            f"Gegenüber der ungebremsten Reaktion bei derselben Temperatur "
            f"ist das ein Vorteil von **{hoch(round(np.log10(mit / ohne)))}**. "
            f"Der Katalysator liefert keine Energie. Er ändert nur den Weg, "
            f"und das genügt."
        )

    merksatz(
        "Ein Katalysator macht das Unmögliche nicht möglich. Er macht das "
        "Aussichtslose alltäglich."
    )

    fachkasten(
        "Zur Aktivierungsenergie",
        """
Für technische Eisenkatalysatoren werden scheinbare Aktivierungsenergien in
der Größenordnung 80 bis 200 kJ/mol berichtet, je nach Katalysator,
Promotoren und Bedingungen. Die 100 kJ/mol dieser App sind ein runder
Mittelwert und kein Tabellenwert.

Der Vergleichsfaktor oben ist das Verhältnis zweier Boltzmann-Faktoren,
e^(−E₁/RT) / e^(−E₂/RT). Er zeigt, wie stark eine gesenkte Hürde durchschlägt. Er sagt nicht,
um wie viel eine reale Anlage schneller wird.
""",
    )


# ==================================================================
# Kapitel 4
# ==================================================================
def _k4():
    kapitel_kopf(4, N_KAP, "Haber und Bosch",
                 "Zwei Personen, zwei Probleme und eine Erfindung mit zwei "
                 "Gesichtern.")

    st.markdown(
        """
### Was Fritz Haber gemacht hat

Haber war Chemiker in Karlsruhe. Er hat als Erster gezeigt, dass sich Ammoniak
aus Luftstickstoff und Wasserstoff wirklich herstellen lässt. Sein Aufbau war
ein Tischgerät: ein kleines Rohr, ein Katalysator aus dem seltenen Metall
Osmium, rund 500 °C und ein Druck von etwa 175 bar. Im Juli 1909 tropfte
daraus zum ersten Mal flüssiges Ammoniak.

Es war wenig, aber es genügte als Beweis. Die Bedingungen dafür kennst du aus
den letzten beiden Kapiteln: heiß genug, damit es schnell geht, dazu unter
hohem Druck, damit trotz der Hitze etwas übrig bleibt. Das billige Eisen, mit
dem heute jede Anlage arbeitet, fand erst danach Alwin Mittasch bei der BASF,
indem er systematisch tausende Stoffe durchprobierte.
"""
    )

    st.markdown(
        """
### Was Carl Bosch gemacht hat

Bosch arbeitete bei der BASF und bekam die Aufgabe, aus dem Tischgerät eine
Fabrik zu machen. Sein Problem war nicht chemischer, sondern stählerner Natur.

Heißer Wasserstoff unter 200 bar frisst sich in Stahl hinein. Er dringt in das
Metall ein, reagiert dort mit dem Kohlenstoff, der den Stahl hart macht, und
lässt ihn von innen brüchig werden. Die ersten Versuchsrohre hielten Stunden
bis Tage, dann platzten sie.

Boschs Lösung war eine doppelte Wand: innen ein Rohr aus weichem, praktisch
kohlenstofffreiem Eisen, das dem Wasserstoff nichts zu bieten hat, außen ein
Druckmantel aus Stahl, der die Last trägt. Dazwischen sitzen kleine Bohrungen,
durch die durchgewanderter Wasserstoff entweichen kann. 1913 ging die erste
Anlage in Oppau in Betrieb.
"""
    )
    merksatz(
        "Das Haber-Bosch-Verfahren ist zur einen Hälfte eine Entdeckung und "
        "zur anderen Hälfte eine Materialfrage. Nur die eine Hälfte kommt in "
        "Chemiebüchern vor."
    )

    st.divider()
    st.markdown(
        """
### Brot

Aus Ammoniak wird Dünger. Die Weltbevölkerung ist seit 1900 von rund
1,6 auf über 8 Milliarden Menschen gewachsen. Ohne synthetischen
Stickstoff wäre das nicht möglich gewesen. Etwa die Hälfte des Stickstoffs in
unserem Körper ist irgendwann durch eine solche Anlage gelaufen.

Kein anderes chemisches Verfahren hat so viele Leben ermöglicht.
"""
    )

    st.markdown(
        """
### Sprengstoff

Aus Ammoniak wird über Salpetersäure aber auch Sprengstoff. Es gibt nicht zwei
Wege, einen guten und einen schlechten. Es ist derselbe Weg bis kurz vor
Schluss.

Vor 1914 bezog das Deutsche Reich seinen Salpeter aus Chile. Mit der
britischen Seeblockade war dieser Weg zu. Nach gängiger Einschätzung wäre
der Munitionsnachschub binnen etwa eines Jahres zu Ende gewesen. Die
Ammoniakanlagen der BASF ersetzten diesen Import. Der Erste Weltkrieg konnte
auch deshalb jahrelang weitergeführt werden.
"""
    )

    st.markdown(
        """
### Giftgas

Haber blieb dabei nicht Zulieferer. Er baute den deutschen Gaskrieg selbst
auf, wählte das Chlorgas aus, organisierte die Stahlflaschen und die Einheiten
an der Front und war beim ersten großen Angriff bei Ypern im April 1915
persönlich anwesend. Tausende Soldaten starben oder wurden dauerhaft
geschädigt.

Haber verteidigte das öffentlich. Seine bekannteste Formulierung lautet, im
Frieden gehöre der Wissenschaftler der Menschheit, im Krieg dem Vaterland.
Seine Frau Clara Immerwahr, selbst promovierte Chemikerin, nahm sich wenige
Tage nach Ypern das Leben.

Er gehörte außerdem zu den Unterzeichnern des Manifests der 93, mit dem im
Oktober 1914 prominente deutsche Wissenschaftler und Künstler die deutsche
Kriegführung öffentlich rechtfertigten. Wissenschaftliche Autorität wurde dort
gezielt als Argument eingesetzt.
"""
    )

    st.markdown(
        """
### Wie es ausging

1919 erhielt Haber den Nobelpreis für Chemie für die Ammoniaksynthese,
rückwirkend für das Jahr 1918. Die Entscheidung war international heftig
umstritten, weil für viele ein Kriegsverbrecher ausgezeichnet wurde. Bosch
bekam 1931 ebenfalls einen Nobelpreis, ausdrücklich für die Hochdrucktechnik.

1933 verlor Haber als Jude seine Stellung und musste Deutschland verlassen.
Er starb 1934 im Exil in Basel. In den Instituten, die er mit aufgebaut hatte,
wurde später ein Schädlingsbekämpfungsmittel weiterentwickelt, das die
Nationalsozialisten in den Vernichtungslagern einsetzten. Mehrere Angehörige
seiner Familie wurden dort ermordet.
"""
    )

    merksatz(
        "Dieselbe Reaktion, dieselbe Anlage, dieselbe Person. Deshalb steht "
        "dieser Fall in einem interdisziplinären Arbeitskreis und nicht nur "
        "im Chemiebuch."
    )

    fachkasten(
        "Belege und Zahlen",
        """
**Betriebsbedingungen.** Moderne Anlagen fahren typischerweise 400 bis 500 °C
und 150 bis 300 bar. Das ist ein Kompromiss: kalt wäre die Ausbeute besser,
weil die Reaktion Wärme abgibt, aber der Katalysator zu langsam. Der Ammoniak
wird laufend auskondensiert und die nicht umgesetzten Gase im Kreis
zurückgeführt, deshalb ist die niedrige Ausbeute pro Durchgang verkraftbar.

**Bevölkerung und Ernährung.** Smil, V. (2001): *Enriching the Earth*, MIT
Press, ist das Standardwerk zur Wirkung des Verfahrens auf die
Weltbevölkerung. Der Anteil von 48 Prozent stammt aus *Green ammonia
synthesis*, Nature Synthesis 2 (2023).

**Haber-Biographie.** Szöllösi-Janze, M. (1998): *Fritz Haber 1868 bis 1934.
Eine Biographie*, München: Beck. Dort auch die Belegstellen zu Ypern, zum
Manifest der 93 und zur Rolle der BASF-Anlagen im Ersten Weltkrieg.

**Nobelpreis.** Der Chemiepreis für 1918 wurde 1919 vergeben und im Juni 1920
überreicht. Die Proteste dagegen sind in den Akten des Nobelkomitees
dokumentiert.
""",
    )
