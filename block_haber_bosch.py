# -*- coding: utf-8 -*-
"""
Block 1 – Dünger aus Luft.

Roter Faden:
  K1  Der Rohstoff ist überall, und niemand kommt heran.
  K2  Warum nicht. Ein einziger Maßstab erklärt es.
  K3  Der Ausweg ist kein größerer Druck, sondern ein anderer Weg.
  K4  Der Weg funktioniert nur als Kompromiss – baue ihn selbst.
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import chemie as ch
from bausteine import (
    BLAU, ORANGE, GRUEN, ROT, DUNKELGRAU, KJ_ZIMMER,
    balken_vergleich, boltzmann_anteil, seltenheit_anzeigen,
    wellenlaenge_nm, fachkasten, merksatz, kapitel_kopf, neue_figur,
    zeige, hoch, dez, schaetzfrage,
)

KAPITEL = [
    "1 · Ein Meer aus Stickstoff",
    "2 · Warum Luft nicht düngt",
    "3 · Der Katalysator",
    "4 · Der Reaktor",
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
scheitert. Er steckt in jedem Eiweiß, in jedem Stück DNA, in jedem Muskel.
"""
    )
    merksatz("Der Rohstoff ist überall – und niemand kommt an ihn heran.")

    st.markdown(
        """
Über Jahrtausende war Stickstoff deshalb ein Engpass. Man sammelte Mist, holte
Guano von südamerikanischen Inseln, baute Salpeter in der Atacama-Wüste ab. Um
1900 war absehbar, dass diese Quellen für eine wachsende Weltbevölkerung nicht
reichen würden.

1909 löste Fritz Haber das Problem im Labor, 1913 baute Carl Bosch daraus eine
Fabrik. Die Reaktion, um die sich alles dreht, sieht harmlos aus:
"""
    )
    st.latex(r"\mathrm{N_2} + 3\,\mathrm{H_2} \;\longrightarrow\; "
             r"2\,\mathrm{NH_3}")
    st.markdown(
        "Links zwei Gase, die es im Überfluss gibt. Rechts Ammoniak, aus dem "
        "Dünger wird. **Bau die drei Moleküle mit dem Baukasten auf dem "
        "Tisch nach** – dann steht die Gleichung als Objekt vor dir, bevor "
        "wir sie durchrechnen."
    )

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Stickstoff in der Luft", "78 %")
    m2.metric("Menschen, die davon leben", "≈ 48 %")
    m3.metric("Anteil am Weltenergiebedarf", "1–2 %")
    st.caption(
        "Rund die Hälfte der Menschheit isst heute Nahrung, deren Stickstoff "
        "aus diesem einen Verfahren stammt. Es verbraucht dafür ein bis zwei "
        "Prozent der gesamten von der Menschheit erzeugten Energie. "
        "(Quelle: *Green ammonia synthesis*, Nature Synthesis 2023.)"
    )

    st.divider()
    st.markdown(
        "Warum das trotzdem über hundert Jahre lang niemand hinbekommen hat, "
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
Stickstoff kommt in der Luft nie einzeln vor, sondern immer paarweise: **N₂**.
Die beiden Atome halten sich mit einer **Dreifachbindung** aneinander fest –
drei Elektronenpaare gleichzeitig. Es ist die stärkste Bindung, die zwei
gleiche Atome miteinander eingehen können.

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
            "zwischen den Bindungen ist gar nicht das Erstaunliche an "
            "dieser Geschichte."
        ),
    )

    if aufgeloest:
        zeige(balken_vergleich(BINDUNGEN,
                               hervorheben="N≡N   im Stickstoff"))
        st.caption(
            "N≡N ist stark, steht aber nicht allein an der Spitze – "
            "Kohlenmonoxid hält noch fester zusammen. Der entscheidende "
            "Vergleich ist ein anderer."
        )

    # -------------------------------------------------- der Maßstab
    st.divider()
    st.subheader("Der einzige Maßstab, den du brauchst")
    st.markdown(
        f"""
Bindungsstärken werden in **kJ/mol** angegeben. Diese Einheit sagt niemandem
etwas, der nicht täglich damit arbeitet, und sie muss es auch nicht. Es gibt
einen einzigen Vergleichswert, der alles Weitere trägt:

**Wie viel Energie bekommt ein Molekül von der Umgebungswärme mit?**

Wärme ist nichts anderes als Bewegung: Je wärmer, desto heftiger zappeln die
Moleküle, desto härter stoßen sie zusammen. Bei 20 °C liegt diese Energie in
der Größenordnung von **{dez(KJ_ZIMMER)} kJ/mol**. Das ist das Kleingeld, mit
dem die Chemie bei Zimmertemperatur einkaufen geht.
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
    ax.annotate("2,4 – der Strich ganz links", xy=(KJ_ZIMMER, 0),
                xytext=(120, 0), va="center", fontsize=9, color=BLAU,
                arrowprops=dict(arrowstyle="->", color=BLAU, lw=1.2))
    ax.set_xlim(0, 1080)
    zeige(fig)

    merksatz(
        f"Der untere Balken ist kein Fehler im Diagramm. Das Verhältnis ist "
        f"<b>1 zu {945/KJ_ZIMMER:.0f}</b> – so wie ein Monatsgehalt zum Preis "
        f"eines Hauses."
    )

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
            "kein Weg: Ammoniak selbst hält solche Temperaturen nicht aus. "
            "Man würde die Bindung knacken und das Produkt im selben Moment "
            "wieder zerlegen."
        )

    merksatz(
        "Bei Zimmertemperatur – also dort, wo Pflanzen wachsen und wo die "
        "Luft steht – heißt diese Zahl nicht <i>selten</i>. Sie heißt "
        "<i>nie</i>."
    )

    # -------------------------------------------------- Licht
    st.divider()
    st.subheader("Warum auch die Sonne nicht hilft")
    lam = wellenlaenge_nm(945.0)
    st.markdown(
        f"""
Wärme ist nicht die einzige Energiequelle. Ein Lichtteilchen trägt seine
Energie in einem einzigen Paket, es muss nichts zusammensparen. Um N≡N in
einem Schlag zu knacken, bräuchte es eine Wellenlänge von **{lam:.0f}
Nanometern**.
"""
    )
    c1, c2 = st.columns(2)
    c1.metric("Nötige Wellenlänge", f"{lam:.0f} nm")
    c2.metric("Was dein Auge noch sieht", "380 – 750 nm")
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
        "wird aus einem Energieunterschied eine Farbe – dieselbe Formel."
    )

    st.divider()
    st.markdown(
        """
### Wo wir jetzt stehen

Hitze reicht nicht, Licht reicht nicht, Warten hilft schon gar nicht. Nach
diesem Kapitel sieht es aus, als sei die Sache erledigt.

Sie ist es nicht. Es gibt einen Ausweg, und er besteht nicht darin, fester zu
drücken.
"""
    )

    fachkasten(
        "Die Zahlen dahinter",
        """
**Bindungsdissoziationsenergien** (Tabellenwerte, 298 K): N≡N 945 kJ/mol,
C≡O 1077, C=O 799, O=O 498, H–H 436, N–H 391, C–C 346 kJ/mol.

**Thermische Energie**: *RT* mit *R* = 8,314 J/(mol·K). Bei 293 K sind das
2,44 kJ/mol. Verhältnis 945 / 2,44 ≈ 388. Die mittlere kinetische Energie
eines Gasteilchens ist mit 3/2 *RT* etwas größer; für eine
Größenordnungsbetrachtung ändert das nichts.

**Der Anteil energiereicher Moleküle** ist der Boltzmann-Faktor
*f* = e^(−E<sub>A</sub>/*RT*). Bei 293 K und E<sub>A</sub> = 945 kJ/mol ergibt
das 4 · 10⁻¹⁶⁹. Das ist eine Abschätzung der Größenordnung, keine
Reaktionsgeschwindigkeit: Dafür bräuchte es zusätzlich Stoßfrequenz und
Orientierungsfaktor. Beide verschieben das Ergebnis um wenige Zehnerpotenzen
und an der Aussage nichts.

**Photonenenergie**: *E* = *hc*/λ. 945 kJ/mol entsprechen 9,79 eV pro Molekül
und damit λ = 127 nm (Vakuum-UV).

**1 eV = 96,485 kJ/mol.** Diese Umrechnung verbindet das Kapitel mit dem
Block Quantenwelt, wo alles in eV gerechnet wird.
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
Im letzten Kapitel stand die Bindung wie eine Wand im Weg: 945 kJ/mol, und die
Wärme im Raum liefert 2,4. Über die Wand kommt man nicht.

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

Was dann folgt, geschieht in vielen kleinen Schritten: Das N₂ zerfällt auf der
Oberfläche in zwei einzelne, festgehaltene Stickstoffatome. Wasserstoff setzt
sich daneben. Dann wandert ein H-Atom zum N-Atom, dann das nächste, dann das
dritte. Erst am Ende löst sich fertiges NH₃ ab.

Statt einer hohen Wand also eine Treppe mit lauter niedrigen Stufen. Am Ende
ist derselbe Punkt erreicht, aber kein einzelner Schritt musste die volle Höhe
schaffen.

Aufgeklärt hat diesen Mechanismus Gerhard Ertl; er bekam dafür 2007 den
Nobelpreis für Chemie – fast hundert Jahre, nachdem das Verfahren bereits
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
        st.caption("**Ganz rechts:** keine Hilfe, blanke Gasphase – die "
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
            f"Der Katalysator liefert keine Energie. Er ändert nur den Weg – "
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
Mittelwert, kein Tabellenwert.

Der Vergleichsfaktor oben ist das Verhältnis zweier Boltzmann-Faktoren,
e^(−E₁/RT) / e^(−E₂/RT). Er zeigt, wie stark eine gesenkte Hürde durchschlägt,
und nicht, um wie viel eine reale Anlage schneller wird.
""",
    )


# ==================================================================
# Kapitel 4
# ==================================================================
@st.cache_data(show_spinner=False)
def _ausbeute_karte():
    """Landkarte für das Reaktor-Spiel. Einmal rechnen, dann liegt sie."""
    Ts = np.linspace(250, 620, 60)
    Ps = np.linspace(10, 400, 60)
    Z = np.array([[ch.nh3_ausbeute(T, P) for T in Ts] for P in Ps])
    OK = np.array([[1.0 if ch.bewertung(T, P)[0] else 0.0 for T in Ts]
                   for P in Ps])
    return Ts, Ps, Z, OK


def _k4():
    kapitel_kopf(4, N_KAP, "Der Reaktor",
                 "Zwei Anforderungen, die in entgegengesetzte Richtungen "
                 "ziehen.")

    st.markdown(
        """
Der Katalysator arbeitet umso schneller, je wärmer es ist. So weit, so gut.

Nur hat die Reaktion eine zweite Eigenschaft: Sie **setzt Energie frei**. Und
Reaktionen, die Wärme abgeben, laufen bei Hitze ungern zu Ende. Je heißer der
Reaktor, desto weniger Ammoniak steht am Schluss darin – ganz gleich, wie
lange man wartet.
"""
    )

    p_fest = st.slider("Druck im Reaktor [bar]", 10, 400, 200, 10,
                       key="p_schere")
    Ts = np.linspace(250, 620, 200)
    ausb = [ch.nh3_ausbeute(T, p_fest) for T in Ts]
    tempo = [ch.relative_geschwindigkeit(T) for T in Ts]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 4.6), sharex=True)
    ax1.plot(Ts, ausb, color=BLAU, lw=2.5)
    ax1.set_ylabel("Ausbeute [%]")
    ax1.set_title("Wie viel am Ende drin ist – je kälter, desto besser",
                  fontsize=10, color=DUNKELGRAU, loc="left")
    ax2.semilogy(Ts, tempo, color=ORANGE, lw=2.5)
    ax2.set_ylabel("Tempo (relativ)")
    ax2.set_xlabel("Temperatur [°C]")
    ax2.set_title("Wie schnell es geht – je heißer, desto besser",
                  fontsize=10, color=DUNKELGRAU, loc="left")
    for ax in (ax1, ax2):
        ax.axvline(ch.BETRIEB_T, color=GRUEN, ls="--", lw=1.4)
        ax.spines[["top", "right"]].set_visible(False)
    ax1.text(ch.BETRIEB_T + 8, max(ausb) * 0.82, "echte Anlagen",
             color=GRUEN, fontsize=9)
    fig.tight_layout()
    zeige(fig)

    st.markdown(
        "Die grüne Linie liegt dort, wo beide Kurven gerade noch erträglich "
        "sind. Sie ist kein chemisches Optimum, sondern ein **Kompromiss**."
    )

    # -------------------------------------------------- Das Spiel
    st.divider()
    st.subheader("Bau deinen eigenen Reaktor")
    st.markdown(
        "Drei Bedingungen musst du gleichzeitig erfüllen: genug Ausbeute, "
        "genug Tempo, und die Anlage darf nicht kaputtgehen."
    )

    g1, g2 = st.columns(2)
    with g1:
        T_spiel = st.slider("Temperatur [°C]", 250, 620, 300, 10,
                            key="t_spiel")
    with g2:
        P_spiel = st.slider("Druck [bar]", 10, 400, 50, 10, key="p_spiel")

    a_spiel = ch.nh3_ausbeute(T_spiel, P_spiel)
    v_spiel = ch.relative_geschwindigkeit(T_spiel)
    geschafft, pruefungen = ch.bewertung(T_spiel, P_spiel)

    m1, m2 = st.columns(2)
    m1.metric("Ammoniak im Gleichgewicht", f"{dez(a_spiel)} %")
    m2.metric("Tempo gegenüber echten Anlagen",
              f"{dez(v_spiel, 2)} ×" if v_spiel >= 0.01
              else f"{v_spiel:.0e} ×")

    for name, erfuellt, text in pruefungen:
        st.markdown(f"{'✅' if erfuellt else '❌'} **{name}** – {text}")

    for art, text in ch.reaktor_check(T_spiel, P_spiel):
        {"fehler": st.error, "warnung": st.warning, "ok": st.info}[art](text)

    if geschafft:
        st.success(
            f"**Geschafft.** Deine Anlage läuft bei {T_spiel} °C und "
            f"{P_spiel} bar. Echte Ammoniakanlagen arbeiten bei rund "
            f"{ch.BETRIEB_T:.0f} °C und {ch.BETRIEB_P:.0f} bar. Wer in der "
            "Nähe landet, hat dieselbe Abwägung getroffen wie Carl Bosch "
            "1913 – nur schneller."
        )

    Ts_k, Ps_k, Z, OK = _ausbeute_karte()
    fig, ax = neue_figur(4.0)
    bild = ax.pcolormesh(Ts_k, Ps_k, Z, cmap="Blues", shading="auto",
                         vmin=0, vmax=80)
    ax.contour(Ts_k, Ps_k, OK, levels=[0.5], colors=[GRUEN], linewidths=2.2)
    ax.scatter([ch.BETRIEB_T], [ch.BETRIEB_P], s=150, marker="*",
               color=GRUEN, edgecolor="white", zorder=6, linewidth=1.2)
    ax.annotate("echte Anlagen", (ch.BETRIEB_T, ch.BETRIEB_P),
                xytext=(-4, 16), textcoords="offset points",
                ha="right", color=GRUEN, fontsize=9, fontweight="bold")
    ax.scatter([T_spiel], [P_spiel], s=130, marker="X",
               color=ROT, edgecolor="white", zorder=7, linewidth=1.2)
    ax.annotate("du", (T_spiel, P_spiel), xytext=(8, -16),
                textcoords="offset points", color=ROT, fontsize=9,
                fontweight="bold")
    ax.set_xlabel("Temperatur [°C]")
    ax.set_ylabel("Druck [bar]")
    fig.colorbar(bild, ax=ax, label="Ammoniak [%]")
    fig.tight_layout()
    zeige(fig)
    st.caption(
        "Dunkelblau heißt viel Ammoniak. Innerhalb der grünen Linie sind alle "
        "drei Bedingungen erfüllt. Das begehbare Gebiet ist ein schmaler Keil "
        "– und er liegt ausgerechnet dort, wo die Ausbeute mäßig ist."
    )

    # -------------------------------------------------- Bosch
    st.divider()
    st.markdown(
        """
### Warum das Verfahren zwei Namen trägt

Haber hatte die Reaktion. Bosch hatte das Problem, sie in eine Fabrik zu bauen
– und dieses Problem war nicht chemischer, sondern **stählerner** Natur.

Heißer Wasserstoff unter 200 bar frisst sich in Stahl hinein. Er dringt in das
Metall ein, reagiert dort mit dem Kohlenstoff, der den Stahl hart macht, und
lässt ihn von innen brüchig werden. Die ersten Versuchsrohre hielten Stunden
bis Tage, dann platzten sie.

Boschs Lösung war eine doppelte Wand: innen ein Rohr aus weichem, praktisch
kohlenstofffreiem Eisen, das dem Wasserstoff nichts zu bieten hat, außen ein
Druckmantel aus Stahl, der die Last trägt. Dazwischen kleine Bohrungen, durch
die durchgewanderter Wasserstoff entweichen kann.
"""
    )
    merksatz(
        "Das Haber-Bosch-Verfahren ist zur einen Hälfte eine Entdeckung und "
        "zur anderen Hälfte eine Materialfrage. Nur die eine Hälfte kommt in "
        "Chemiebüchern vor."
    )

    fachkasten(
        "Modell und Zahlen dieses Kapitels",
        """
**Gleichgewicht.** Berechnet aus ΔH° = −91,8 kJ/mol und ΔS° = −198,1
J/(mol·K) bei 298 K, mit einer Temperaturkorrektur über ΔC<sub>p</sub> ≈ −45
J/(mol·K), daraus *K*(T) = exp(−ΔG/RT). Gelöst wird das Massenwirkungsgesetz
für ein stöchiometrisches Gemisch (1 : 3).

Ein rein ideales Gasmodell liegt bei hohen Drücken systematisch zu niedrig.
Deshalb steckt ein empirischer Realgas-Zuschlag exp(0,00199 · *p*) darin. Er
wurde gegen die klassische Messtabelle von Larson & Dodge (1923/24) angepasst
und trifft sie zwischen 10 und 600 bar und 200 bis 600 °C auf etwa einen
Prozentpunkt.

**Geschwindigkeit.** Reine Arrhenius-Abschätzung *v* ∝ exp(−E<sub>A</sub>/RT)
mit E<sub>A</sub> = 100 kJ/mol, normiert auf 450 °C. Sie bildet die
Temperaturabhängigkeit richtig ab, sagt aber nichts über absolute Durchsätze.

**Betriebspunkt.** Moderne Anlagen fahren typischerweise 400–500 °C und
150–300 bar; Boschs erste Anlage in Oppau lief bei etwa 200 bar. Der Ammoniak
wird laufend auskondensiert und die nicht umgesetzten Gase im Kreis
zurückgeführt – deshalb ist die niedrige Gleichgewichtsausbeute pro Durchgang
verkraftbar.
""",
    )
