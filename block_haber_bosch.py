# -*- coding: utf-8 -*-
"""
Block Haber-Bosch.

Roter Faden: Der Rohstoff ist überall, aber niemand kommt heran (K0).
Warum nicht – und was "Energie" dabei überhaupt heißt (K1). Wie man das
Problem trotzdem löst, und warum die Lösung ein Kompromiss ist (K2).
Dass man das alles auch ohne Labor ausrechnen kann (K3). Und was daraus
geworden ist (K4, K5).
"""

import json
import os

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import chemie as ch
from bausteine import (
    BLAU, ORANGE, GRUEN, ROT, DUNKELGRAU, HARTREE_KJ,
    alltag, energie_karten, balken_vergleich, boltzmann_anteil,
    seltenheit_anzeigen, waermeportion, code_feld, fachkasten, merksatz,
    kapitel_kopf, neue_figur, zeige, hoch, dez, schaetzfrage,
)

try:
    import hf_pure
    HF_DA = True
except ImportError:
    HF_DA = False

KAPITEL = [
    "0 · Wir stehen in einem Meer aus Dünger",
    "1 · Warum Luft nicht düngt",
    "2 · Der Trick, der alles änderte",
    "3 · Moleküle aus dem Nichts berechnen",
    "4 · Brot und Sprengstoff",
    "5 · Diskussion",
]
N_KAP = len(KAPITEL)

# Gemessene Bindungsenergien in kJ/mol (Standardwerte aus Tabellenwerken)
BINDUNGEN = [
    ("N≡N   im Stickstoff", 945),
    ("C≡O   im Kohlenmonoxid", 1077),
    ("C=O   im Kohlendioxid", 799),
    ("O=O   im Sauerstoff", 498),
    ("H–H   im Wasserstoff", 436),
    ("C–C   im Diamant", 346),
    ("N–H   im Ammoniak", 391),
]


def abweichung(wert, referenz, stellen=2):
    """Abstand zum Referenzwert als lesbarer Text."""
    d = abs(wert - referenz)
    if d < 0.005:
        return "praktisch genau richtig"
    return f"{dez(d, stellen)} Å"


NH3_GEOMETRIE = (
    ("N", (0.000000, 0.000000, 0.116489)),
    ("H", (0.000000, 0.939731, -0.271808)),
    ("H", (0.813831, -0.469865, -0.271808)),
    ("H", (-0.813831, -0.469865, -0.271808)),
)


# ==================================================================
# Vorberechnete Quantenchemie
# ==================================================================
@st.cache_data(show_spinner=False)
def vorberechnet():
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "vorberechnet.json")
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def qm_energie(atome, spin=0):
    """Gesamtenergie eines Moleküls per Hartree-Fock (STO-3G), in Hartree."""
    return hf_pure.energie(list(atome), spin=spin)


# ==================================================================
def zeichne(kapitel):
    i = KAPITEL.index(kapitel)
    [_k0, _k1, _k2, _k3, _k4, _k5][i]()


# ==================================================================
# Kapitel 0
# ==================================================================
def _k0():
    kapitel_kopf(0, N_KAP, "Wir stehen in einem Meer aus Dünger",
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
    merksatz("Die Ausgangslage ist absurd: <b>Der Rohstoff ist überall, "
             "und niemand kommt an ihn heran.</b>")

    st.info(
        "Über Jahrtausende war Stickstoff deshalb ein Engpass. Man sammelte "
        "Mist, holte Guano von südamerikanischen Inseln, baute Salpeter in der "
        "Atacama-Wüste ab. Um 1900 war absehbar, dass diese Quellen für eine "
        "wachsende Weltbevölkerung nicht reichen würden."
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Stickstoff in der Luft", "78 %")
    m2.metric("Menschen, die davon leben", "≈ 48 %")
    m3.metric("Anteil am Weltenergiebedarf", "1–2 %")
    st.caption(
        "Rund die Hälfte der Menschheit isst heute Nahrung, deren Stickstoff "
        "aus diesem einen Verfahren stammt. Es verbraucht dafür ein bis zwei "
        "Prozent der gesamten Energie, die die Menschheit erzeugt."
    )

    st.divider()
    st.markdown(
        "1909 löste Fritz Haber das Problem im Labor, 1913 baute Carl Bosch "
        "daraus eine Fabrik. Die Reaktion, um die sich alles dreht, sieht "
        "harmlos aus:"
    )
    st.latex(r"\mathrm{N_2} + 3\,\mathrm{H_2} \;\longrightarrow\; 2\,\mathrm{NH_3}")
    st.markdown(
        "Links zwei Gase, die es im Überfluss gibt. Rechts Ammoniak, aus dem "
        "Dünger wird. Warum das trotzdem über hundert Jahre lang niemand "
        "hinbekommen hat, liegt an etwas, das man nicht sieht."
    )

    st.divider()
    code_feld(
        "luft",
        '''# Wie viel Stickstoff steht gerade in diesem Raum herum?
# Trag eure Raumgroesse ein und drueck auf Ausfuehren.

laenge = 10     # Meter
breite = 8
hoehe  = 3

volumen = laenge * breite * hoehe        # Kubikmeter
luft_kg = volumen * 1.2                  # Luft wiegt 1,2 kg pro Kubikmeter
stickstoff_kg = luft_kg * 0.755          # 75,5 Massenprozent

print(f"Raumvolumen:        {volumen} m3")
print(f"Luft im Raum:       {luft_kg:.0f} kg")
print(f"Davon Stickstoff:   {stickstoff_kg:.0f} kg")
print()

# Ein Hektar Weizen braucht ungefaehr 150 kg Stickstoff pro Jahr.
print(f"Das reicht rechnerisch fuer {stickstoff_kg/150:.1f} Hektar Weizen.")
print("Wenn man drankaeme. Genau das ist das Problem.")
''',
        hinweis="Schätz die Größe eures Seminarraums und ändere die drei "
                "Zahlen. Kaputtmachen kannst du nichts.",
        hoehe=300,
        titel="Selbst nachrechnen",
    )


# ==================================================================
# Kapitel 1 – das Energiekapitel
# ==================================================================
def _k1():
    kapitel_kopf(
        1, N_KAP, "Warum Luft nicht düngt",
        "Gleich kommen Energien ins Spiel. Wir brauchen dafür keine "
        "Einheiten, sondern nur einen einzigen Maßstab.")

    st.markdown(
        """
Stickstoff kommt in der Luft nie einzeln vor, sondern immer paarweise: **N₂**.
Die beiden Atome halten sich mit einer **Dreifachbindung** aneinander fest –
drei Elektronenpaare gleichzeitig, die stärkste Bindung, die zwei gleiche
Atome miteinander eingehen können.

Bevor Stickstoff düngen kann, muss diese Bindung auf. Vorher passiert nichts.
"""
    )

    # -------------------------------------------------- Schätzfrage
    st.divider()
    st.subheader("Erst raten")
    _, aufgeloest = schaetzfrage(
        "n2_vs_h2",
        "Wie viel mehr Aufwand kostet es, N≡N zu brechen als H–H, "
        "die Bindung im Wasserstoff?",
        1.0, 8.0, 3.0, 0.1, 945 / 436,
        einheit="mal so viel", format_str="%.1f",
        toleranz_gut=0.35,
        aufloesung_text=(
            "Der Faktor ist **2,2**. Die meisten tippen höher – die "
            "Dreifachbindung klingt nach dreimal so viel. Das täuscht: "
            "Der Unterschied zwischen den Bindungen ist gar nicht das "
            "Erstaunliche an dieser Geschichte."
        ),
    )

    if aufgeloest:
        st.markdown("Im Verhältnis zueinander sehen die Bindungen so aus:")
        zeige(balken_vergleich(BINDUNGEN, hervorheben="N≡N   im Stickstoff"))
        st.caption(
            "N≡N ist stark, aber nicht einsam an der Spitze. Kohlenmonoxid "
            "hält sogar noch fester zusammen. Die Frage ist also nicht, "
            "warum diese Bindung so stark ist – sondern womit man sie "
            "eigentlich vergleichen sollte."
        )

    # -------------------------------------------------- der Maßstab
    st.divider()
    st.subheader("Der einzige Maßstab, den du brauchst")
    st.markdown(
        """
Bindungsstärken werden in **kJ/mol** angegeben, der üblichen Währung der
Chemie. Diese Einheit sagt niemandem etwas, der nicht täglich damit arbeitet,
und sie muss es auch nicht. Es gibt einen einzigen Vergleichswert, der alles
Weitere trägt:

**Wie viel Energie hat ein Molekül bei Zimmertemperatur zur Verfügung?**

Wärme ist nichts anderes als Bewegung. Je wärmer, desto heftiger zappeln die
Moleküle, desto härter stoßen sie zusammen. Bei 20 °C liefert diese Wärme
jedem Molekül eine Portion von rund **2,4 kJ/mol**. Das ist das Kleingeld,
mit dem die Chemie bei Zimmertemperatur einkaufen geht.
"""
    )

    portion = waermeportion(20.0)
    fig, ax = neue_figur(1.9)
    ax.barh([1], [945], color=ORANGE, height=0.55)
    ax.barh([0], [portion], color=BLAU, height=0.55)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Wärme im Raum\nliefert", "N≡N\nverlangt"])
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Energie  [kJ/mol]")
    ax.text(960, 1, "945", va="center", fontsize=10, color=DUNKELGRAU)
    ax.annotate("2,4 – der Strich ganz links", xy=(portion, 0),
                xytext=(120, 0), va="center", fontsize=9, color=BLAU,
                arrowprops=dict(arrowstyle="->", color=BLAU, lw=1.2))
    ax.set_xlim(0, 1080)
    zeige(fig)

    st.markdown(
        f"""
Der untere Balken ist kein Fehler im Diagramm. Er ist wirklich so klein.
Das Verhältnis ist **1 zu {945/portion:.0f}**.
"""
    )
    merksatz(
        "Stell dir vor, du sollst ein Haus bar bezahlen und verdienst ein "
        "durchschnittliches Monatsgehalt. Du bräuchtest rund 390 Monate, also "
        "gut 30 Jahre. Genau in diesem Verhältnis steht die Wärme in diesem "
        "Raum zu der Bindung, die aufgebrochen werden soll."
    )

    # -------------------------------------------------- Boltzmann
    st.divider()
    st.subheader("Aber Wärme ist nicht gerecht verteilt")
    st.markdown(
        """
Jetzt kommt der Einwand, der weiterführt: 2,4 kJ/mol ist ein **Durchschnitt**.
Manche Moleküle sind viel langsamer, manche viel schneller. In jeder Sekunde
gibt es Ausreißer, die weit über dem Schnitt liegen.

Reicht das? Gibt es genug Glückstreffer, damit wenigstens ab und zu ein N₂
auseinanderfliegt? Dreh an der Temperatur und schau selbst.
"""
    )

    temp = st.slider("Temperatur", 20, 3000, 20, 10, format="%d °C",
                     key="t_boltzmann")
    anteil = boltzmann_anteil(945.0, temp)
    seltenheit_anzeigen(anteil, kontext=f", um N≡N bei {temp} °C zu brechen")

    if temp >= 1500:
        rest = ch.nh3_ausbeute(min(temp, 1200), 200)
        st.warning(
            f"**Bei dieser Temperatur ginge es tatsächlich los.** Nur ist das "
            f"kein Weg: Ammoniak selbst hält solche Temperaturen nicht aus. "
            f"Schon bei 1200 °C und 200 bar wären im Gleichgewicht nur noch "
            f"{dez(rest, 2)} % Ammoniak übrig. Du würdest die Bindung knacken und "
            f"das Produkt im selben Moment wieder zerlegen."
        )

    merksatz(
        "Diese Zahl ist der eigentliche Inhalt des Kapitels. Bei "
        "Zimmertemperatur – also dort, wo Pflanzen wachsen und wo die Luft "
        "steht – bedeutet sie nicht <i>selten</i>. Sie bedeutet, dass es in "
        "der Geschichte des Universums kein einziges Mal passiert ist."
    )

    # -------------------------------------------------- Licht
    st.divider()
    st.subheader("Warum auch die Sonne nicht hilft")
    a = alltag(945.0)
    st.markdown(
        f"""
Wärme ist nicht die einzige Energiequelle. Licht wäre eine andere: Ein
Lichtteilchen trägt seine Energie in einem einzigen Paket, es muss nichts
zusammensparen.

Wie viel Energie müsste dieses Lichtteilchen haben, um N≡N in einem Schlag zu
knacken? Rechnet man das um, kommt eine **Wellenlänge von
{a['wellenlaenge_nm']:.0f} Nanometern** heraus.
"""
    )
    c1, c2 = st.columns(2)
    c1.metric("Nötige Wellenlänge", f"{a['wellenlaenge_nm']:.0f} nm")
    c2.metric("Was dein Auge noch sieht", "380 – 750 nm")
    st.markdown(
        """
Das ist tiefes Ultraviolett, weit jenseits dessen, was unten ankommt. Genau
diese Strahlung wird in der hohen Atmosphäre vollständig weggefiltert – unter
anderem vom Stickstoff und Sauerstoff selbst.
"""
    )
    merksatz(
        "Sonnenlicht am Boden kann Stickstoff nicht aufbrechen. Wäre es "
        "energiereich genug, gäbe es uns nicht."
    )
    st.caption(
        "Diese Rechnung taucht im Block Quantenwelt noch einmal auf: Dort "
        "wird aus einem Energieunterschied eine Farbe. Es ist dieselbe Formel."
    )

    st.divider()
    energie_karten(945.0, "Und wenn man es doch mit roher Gewalt versuchte")

    st.divider()
    st.markdown(
        """
### Wo wir jetzt stehen

Hitze reicht nicht, Licht reicht nicht, und Warten hilft schon gar nicht. Nach
diesem Kapitel sieht es so aus, als sei die Sache erledigt.

Sie ist es nicht. Es gibt einen Ausweg, und er besteht nicht darin, fester zu
drücken.
"""
    )

    fachkasten(
        "Die Zahlen dahinter",
        """
**Bindungsdissoziationsenergien** (Standardwerte, 298 K):
N≡N 945 kJ/mol, C≡O 1077, C=O 799, O=O 498, N–H 391, C–C 346, H–H 436 kJ/mol.

**Thermische Energie**: *RT* mit *R* = 8,314 J/(mol·K).
Bei 293 K sind das 2,44 kJ/mol.
Verhältnis 945 / 2,44 ≈ 387.

**Der Anteil energiereicher Moleküle** ist der Boltzmann-Faktor

$$f = e^{-E_\\mathrm{A}/RT}$$

Bei 293 K und *E*<sub>A</sub> = 945 kJ/mol ergibt das 4 · 10⁻¹⁶⁹.
Das ist eine Größenordnungsabschätzung, keine Reaktionsgeschwindigkeit: Ein
vollständiger Ansatz bräuchte zusätzlich die Stoßfrequenz und einen
Orientierungsfaktor. Beide ändern das Ergebnis um wenige Zehnerpotenzen und
damit an der Aussage nichts.

**Photonenenergie**: *E* = *hc*/λ. 945 kJ/mol entsprechen 9,79 eV pro
Molekül und damit λ = 127 nm (Vakuum-UV).

**1 eV = 96,485 kJ/mol.** Diese Umrechnung verbindet dieses Kapitel mit
dem Block Quantenwelt, wo alles in eV gerechnet wird.
""",
    )


# ==================================================================
# Kapitel 2 – Katalysator und Reaktor
# ==================================================================
@st.cache_data(show_spinner=False)
def _ausbeute_karte():
    """Ausbeute-Landkarte für das Reaktor-Spiel. Einmal rechnen, dann liegt sie."""
    Ts = np.linspace(250, 620, 60)
    Ps = np.linspace(10, 400, 60)
    Z = np.array([[ch.nh3_ausbeute(T, P) for T in Ts] for P in Ps])
    OK = np.array([[1.0 if ch.bewertung(T, P)[0] else 0.0 for T in Ts]
                   for P in Ps])
    return Ts, Ps, Z, OK


def _k2():
    kapitel_kopf(
        2, N_KAP, "Der Trick, der alles änderte",
        "Nicht fester drücken, sondern außen herum. Und dann den Preis dafür "
        "bezahlen.")

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

Was dann folgt, geschieht nicht in einem Sprung, sondern in vielen kleinen
Schritten: Das N₂ zerfällt auf der Oberfläche in zwei einzelne, festgehaltene
Stickstoffatome. Wasserstoff setzt sich daneben. Dann wandert ein H-Atom zum
N-Atom, dann das nächste, dann das dritte. Erst am Ende löst sich fertiges
NH₃ ab.

Statt einer hohen Wand also eine Treppe mit lauter niedrigen Stufen. Am Ende
ist derselbe Punkt erreicht, aber nie musste ein einzelner Schritt die volle
Höhe schaffen.

Wer diesen Mechanismus im Detail aufgeklärt hat, war Gerhard Ertl. Er bekam
dafür 2007 den Nobelpreis für Chemie – fast hundert Jahre nachdem das
Verfahren bereits im industriellen Einsatz war. Man hat also fast ein
Jahrhundert lang etwas benutzt, ohne genau zu wissen, warum es funktioniert.
"""
        )

    # -------------------------------------------------- Barriere-Regler
    st.divider()
    st.subheader("Was das für die Chancen bedeutet")
    st.markdown(
        "Der Regler unten senkt die Hürde, die ein Molekül nehmen muss. "
        "Die Temperatur bleibt dabei gleich. Verändert wird nur der Weg."
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        barriere = st.slider(
            "Höhe der Hürde [kJ/mol]", 50, 945, 945, 5, key="barriere")
    with c2:
        t_kat = st.slider("Temperatur [°C]", 20, 600, 450, 10, key="t_kat")

    if barriere > 800:
        st.caption("**Ganz rechts:** keine Hilfe, blanke Gasphase – "
                   "die volle Dreifachbindung.")
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
        faktor_log = np.log10(mit / ohne)
        st.success(
            f"Gegenüber der ungebremsten Reaktion bei derselben Temperatur ist "
            f"das ein Vorteil von **{hoch(round(faktor_log))}**. Der "
            f"Katalysator liefert keine Energie. Er ändert nur den Weg – und "
            f"das genügt."
        )

    merksatz(
        "Ein Katalysator macht das Unmögliche nicht möglich. Er macht das "
        "Aussichtslose alltäglich."
    )

    # -------------------------------------------------- Die Schere
    st.divider()
    st.subheader("Und jetzt das Problem, das Bosch bekam")
    st.markdown(
        """
Der Katalysator arbeitet umso schneller, je wärmer es ist. So weit, so gut.

Nur hat die Reaktion eine zweite Eigenschaft: Sie **setzt Energie frei**. Und
Reaktionen, die Wärme abgeben, laufen bei Hitze ungern zu Ende. Je heißer der
Reaktor, desto weniger Ammoniak steht am Schluss darin – ganz gleich, wie
lange man wartet.

Zwei Anforderungen, die in entgegengesetzte Richtungen ziehen:
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
        "Die grüne Linie liegt genau dort, wo beide Kurven noch gerade eben "
        "erträglich sind. Sie ist kein chemisches Optimum. Sie ist ein "
        "**Kompromiss**."
    )

    # -------------------------------------------------- Das Spiel
    st.divider()
    st.subheader("Bau deinen eigenen Reaktor")
    st.markdown(
        "Drei Bedingungen musst du gleichzeitig erfüllen: genug Ausbeute, "
        "genug Tempo, und die Anlage darf nicht kaputtgehen. Finde ein "
        "Wertepaar, das alle drei schafft."
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
              f"{dez(v_spiel, 2)} ×" if v_spiel >= 0.01 else f"{v_spiel:.0e} ×")

    for name, erfuellt, text in pruefungen:
        st.markdown(f"{'✅' if erfuellt else '❌'} **{name}** – {text}")

    for art, text in ch.reaktor_check(T_spiel, P_spiel):
        {"fehler": st.error, "warnung": st.warning, "ok": st.info}[art](text)

    if geschafft:
        st.success(
            f"**Geschafft.** Deine Anlage läuft bei {T_spiel} °C und "
            f"{P_spiel} bar. Zum Vergleich: Echte Ammoniakanlagen arbeiten "
            f"bei rund {ch.BETRIEB_T:.0f} °C und {ch.BETRIEB_P:.0f} bar. "
            "Wenn du in der Nähe gelandet bist, hast du gerade dieselbe "
            "Abwägung getroffen wie Carl Bosch 1913 – nur schneller."
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

Haber hatte die Reaktion. Bosch hatte das Problem, sie in eine Fabrik zu
bauen – und dieses Problem war nicht chemischer, sondern **stählerner** Natur.

Heißer Wasserstoff unter 200 bar frisst sich in Stahl hinein. Er dringt in das
Metall ein, reagiert dort mit dem Kohlenstoff, der den Stahl hart macht, und
lässt ihn von innen brüchig werden. Die ersten Versuchsrohre hielten Stunden
bis Tage, dann platzten sie.

Boschs Lösung war eine doppelte Wand: innen ein Rohr aus weichem, praktisch
kohlenstofffreiem Eisen, das dem Wasserstoff nichts zu bieten hat, außen ein
Druckmantel aus Stahl, der die Last trägt. Und dazwischen kleine Bohrungen,
durch die durchgewanderter Wasserstoff entweichen kann, statt sich zwischen den
Wänden aufzustauen.
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
**Gleichgewicht.** Berechnet aus ΔH° = −91,8 kJ/mol und
ΔS° = −198,1 J/(mol·K) bei 298 K, mit einer Temperaturkorrektur über
ΔC<sub>p</sub> ≈ −45 J/(mol·K), daraus *K*(T) = exp(−ΔG/RT). Gelöst wird
das Massenwirkungsgesetz für ein stöchiometrisches Gemisch (1 : 3).

Ein rein ideales Gasmodell liegt bei hohen Drücken systematisch etwa 15 %
zu niedrig, weil reale Gase dort nicht mehr ideal sind. Deshalb steckt ein
empirischer Realgas-Zuschlag exp(0,00199 · *p*) drin. Er wurde gegen die
klassische Messtabelle von Larson & Dodge (1923/24) angepasst und trifft
sie zwischen 10 und 600 bar und 200 bis 600 °C auf etwa einen Prozentpunkt.

**Geschwindigkeit.** Reine Arrhenius-Abschätzung
*v* ∝ exp(−E<sub>A</sub>/RT) mit E<sub>A</sub> = 100 kJ/mol, normiert auf
450 °C. Sie bildet die Temperaturabhängigkeit richtig ab, sagt aber nichts
über absolute Durchsätze.

**Aktivierungsenergie am Eisen.** Für technische Eisenkatalysatoren werden
scheinbare Aktivierungsenergien in der Größenordnung 80 bis 200 kJ/mol
berichtet, je nach Katalysator, Promotoren und Bedingungen. 100 kJ/mol ist
hier ein runder Mittelwert, kein Tabellenwert.

**Betriebspunkt.** Moderne Anlagen fahren typischerweise 400–500 °C und
150–300 bar; Boschs erste Anlage in Oppau lief bei etwa 200 bar. Der
Ammoniak wird laufend auskondensiert und die nicht umgesetzten Gase im
Kreis zurückgeführt – deshalb ist die niedrige Gleichgewichtsausbeute pro
Durchgang verkraftbar.
""",
    )


# ==================================================================
# Kapitel 3 – Quantenchemie
# ==================================================================
def _k3():
    kapitel_kopf(
        3, N_KAP, "Moleküle aus dem Nichts berechnen",
        "Bis hier kamen alle Zahlen aus Messungen. Jetzt kommt keine mehr.")

    st.markdown(
        """
Alles, was bisher da stand – Bindungsstärken, Reaktionsenergien, Ausbeuten –
stammt aus dem Labor. Jemand hat gemessen.

Seit 1926 gibt es einen zweiten Weg. Die Schrödinger-Gleichung behauptet: Wenn
du sagst, **wo die Atomkerne stehen** und **wie viele Elektronen es gibt**,
folgt alles Übrige daraus. Bindungslängen, Energien, Farben. Ohne Experiment.

Diese Behauptung prüfen wir jetzt nach. Die Rechnung läuft gleich wirklich
in dieser App – nichts davon ist vorher nachgeschlagen.
"""
    )

    if not HF_DA:
        st.error(
            "Die Datei `hf_pure.py` liegt nicht neben der App. Ohne sie kann "
            "dieses Kapitel nicht rechnen."
        )
        st.stop()

    daten = vorberechnet()

    with st.expander("**Wie macht der Computer das?** (eine Analogie)"):
        st.markdown(
            """
Ein Molekül ist ein Haufen Elektronen, die sich alle gegenseitig abstoßen.
Sobald es mehr als zwei sind, lässt sich das nicht mehr exakt lösen – nicht
weil die Rechner zu langsam wären, sondern weil es keine geschlossene Lösung
gibt.

Das Verfahren hier heißt **Hartree-Fock** und macht eine Vereinfachung: Stell
dir eine volle Party vor. Statt auszurechnen, wie jeder Gast jedem einzelnen
anderen ausweicht, tut man so, als bewege sich jeder nur durch eine
**gleichmäßige Menschenmenge**. Jeder spürt den Durchschnitt aller anderen,
niemand spürt einen einzelnen.

Das ist grob. Es ist aber schnell, und es ist ehrlich – man weiß genau,
was man weggelassen hat. Später in diesem Kapitel sehen wir, wo genau diese
Vereinfachung zusammenbricht.
"""
        )

    # ---------------------------------------------- Schritt 1: raten
    st.divider()
    st.subheader("Schritt 1 · Rate gegen den Computer")
    st.markdown(
        """
Wir nehmen das einfachste Molekül überhaupt: **H₂**, zwei Wasserstoffatome,
zwei Elektronen. Die einzige Frage lautet: Wie weit stehen die beiden Kerne
voneinander entfernt?

Ein Ångström ist ein Zehnmilliardstel Meter. Ein Atom hat ungefähr diese
Größe.
"""
    )

    tipp = st.slider("Dein Tipp für den Abstand [Ångström]",
                     0.40, 2.20, 1.20, 0.01, key="tipp_h2")

    if st.button("Rechnen lassen und vergleichen", type="primary",
                 key="btn_h2"):
        balken = st.progress(0.0, "Schrödinger-Gleichung wird gelöst …")
        rs = np.round(np.arange(0.40, 2.41, 0.05), 3)
        es = []
        for k, r in enumerate(rs):
            es.append(qm_energie((("H", (0, 0, 0)), ("H", (0, 0, float(r))))))
            balken.progress((k + 1) / len(rs),
                            f"Abstand {r:.2f} Å gerechnet "
                            f"({k+1} von {len(rs)})")
        balken.empty()
        st.session_state["h2_kurve"] = (rs.tolist(), es, tipp)

    if "h2_kurve" in st.session_state:
        rs, es, tipp_gespeichert = st.session_state["h2_kurve"]
        rs = np.array(rs)
        es = np.array(es)
        i = int(np.argmin(es))
        r_rechnung = rs[i]
        r_messung = 0.741

        fig, ax = neue_figur(3.4)
        rel = (es - es[i]) * HARTREE_KJ
        ax.plot(rs, rel, "-", color=BLAU, lw=2.5)
        ax.scatter([r_rechnung], [0], color=ORANGE, s=110, zorder=5)
        ax.axvline(r_messung, color=GRUEN, ls="--", lw=1.5)
        ax.axvline(tipp_gespeichert, color=ROT, ls=":", lw=1.8)
        ax.set_ylim(-40, min(600, rel.max()))
        ax.text(r_messung + 0.02, 480, "gemessen", color=GRUEN, fontsize=9)
        ax.text(tipp_gespeichert + 0.02, 400, "dein Tipp", color=ROT,
                fontsize=9)
        ax.set_xlabel("Abstand der beiden Kerne [Ångström]")
        ax.set_ylabel("Energie über dem Minimum [kJ/mol]")
        zeige(fig)

        d1, d2, d3 = st.columns(3)
        d1.metric("Dein Tipp", f"{dez(tipp_gespeichert, 2)} Å")
        d2.metric("Der Computer", f"{dez(r_rechnung, 2)} Å")
        d3.metric("Das Labor", f"{dez(r_messung, 3)} Å")
        st.caption(
            f"Dein Tipp lag {abweichung(tipp_gespeichert, r_messung)} neben "
            f"dem Messwert, die Rechnung "
            f"{abweichung(r_rechnung, r_messung)}."
        )

        if abs(tipp_gespeichert - r_messung) < abs(r_rechnung - r_messung):
            st.success(
                "**Du warst näher dran als die Rechnung.** Das ist kein "
                "Zufallstreffer und auch keine Blamage für die Quantenmechanik: "
                "Der Computer hatte keine Vorkenntnis, du schon. Er hat den "
                "Wert hergeleitet, du hast ihn geschätzt."
            )
        else:
            st.success(
                "**Der Computer war näher.** Bemerkenswert daran ist nicht, "
                "dass er gewinnt, sondern womit: Eingegeben wurden zwei "
                "Protonen und zwei Elektronen. Sonst nichts."
            )

        st.markdown(
            """
Die Kurve erzählt die ganze Geschichte einer chemischen Bindung. Links, bei
kleinen Abständen, stoßen sich die beiden Kerne ab – die Energie schießt hoch.
Rechts, bei großen Abständen, ist die Bindung schlicht nicht mehr da. Das
**Tal in der Mitte** ist die Bindung. Seine Lage ist die Bindungslänge, seine
Tiefe die Bindungsstärke.
"""
        )
        tiefe = (2 * daten["E_H_atom"] - es[i]) * HARTREE_KJ
        e1, e2 = st.columns(2)
        e1.metric("Berechnete Tiefe des Tals", f"{tiefe:.0f} kJ/mol")
        e2.metric("Im Labor gemessen", "436 kJ/mol")
        st.caption(
            f"Das Tal ist rund {abs(tiefe-436)/436*100:.0f} Prozent zu tief – "
            "die Rechnung macht die Bindung etwas stärker, als sie ist. Für "
            "ein Ergebnis, in das kein einziger Messwert eingeflossen ist, "
            "ist das erstaunlich nah."
        )

    # ---------------------------------------------- Schritt 2: Reaktion
    st.divider()
    st.subheader("Schritt 2 · Die Haber-Bosch-Reaktion selbst")
    st.latex(r"\mathrm{N_2} + 3\,\mathrm{H_2} \;\longrightarrow\; 2\,\mathrm{NH_3}")
    st.markdown(
        "Derselbe Trick, dreimal angewandt: einmal für N₂, einmal für H₂, "
        "einmal für NH₃. Aus den drei Energien folgt, ob die Reaktion Energie "
        "freisetzt oder welche braucht."
    )

    tipp_vz = st.radio(
        "**Bevor gerechnet wird: Was glaubst du?**",
        ["Die Reaktion braucht Energie",
         "Ungefähr null, es hebt sich auf",
         "Die Reaktion setzt Energie frei"],
        index=None,
        key="vz_tipp",
    )
    if tipp_vz is None:
        st.caption("Leg dich fest, bevor du rechnen lässt.")

    if st.button("Jetzt rechnen (dauert ein paar Sekunden)", type="primary",
                 key="btn_hb", disabled=tipp_vz is None):
        balken = st.progress(0.0, "Drei Moleküle werden durchgerechnet …")
        E_H2 = qm_energie((("H", (0, 0, 0)), ("H", (0, 0, 0.74))))
        balken.progress(0.33, "H₂ fertig, jetzt N₂ …")
        E_N2 = qm_energie((("N", (0, 0, 0)), ("N", (0, 0, 1.10))))
        balken.progress(0.66, "N₂ fertig, jetzt NH₃ …")
        E_NH3 = qm_energie(NH3_GEOMETRIE)
        balken.empty()
        st.session_state["hb_dE"] = (2 * E_NH3 - (E_N2 + 3 * E_H2)) * HARTREE_KJ

    if "hb_dE" in st.session_state:
        dE = st.session_state["hb_dE"]
        richtig = bool(tipp_vz) and tipp_vz.startswith("Die Reaktion setzt")
        st.metric("Berechnete Reaktionsenergie", f"{dE:+.0f} kJ/mol",
                  delta="gemessen: −92 kJ/mol", delta_color="off")
        if richtig:
            st.success(
                "**Dein Tipp stimmt, und die Rechnung bestätigt ihn.** Das "
                "Minuszeichen heißt: Energie wird frei. Die Reaktion will "
                "grundsätzlich in diese Richtung. Genau das hatte Haber 1909 "
                "im Labor gefunden – nur haben wir es eben ohne Labor "
                "nachvollzogen."
            )
        else:
            st.info(
                "**Das Vorzeichen ist negativ: Energie wird frei.** Das ist "
                "erstaunlich, wenn man Kapitel 1 im Kopf hat: Die Reaktion "
                "*will* laufen. Sie kommt nur nicht los. Bei Haber-Bosch geht "
                "es nie darum, die Reaktion energetisch zu ermöglichen, "
                "sondern nur darum, ihr den Weg zu bahnen."
            )
        st.warning(
            f"**Der Zahlenwert ist deutlich daneben.** Berechnet "
            f"{dE:+.0f}, gemessen −92 kJ/mol. Das Vorzeichen stimmt, die "
            "Größenordnung stimmt, der Wert nicht. Warum, steht im nächsten "
            "Abschnitt – und der ist der interessanteste des Kapitels."
        )

    # ---------------------------------------------- Schritt 3: Scheitern
    st.divider()
    st.subheader("Schritt 3 · Wo das Modell zusammenbricht")
    st.markdown(
        """
Bisher lief es gut: Bindungslänge fast richtig, Bindungsstärke etwas zu hoch,
Vorzeichen richtig. Man könnte den Eindruck bekommen, das Verfahren sei
zuverlässig.

Ist es nicht. Und die Stelle, an der es versagt, ist ausgerechnet die, um die
sich dieses ganze Kapitel dreht.
"""
    )

    if st.button("Die N≡N-Dreifachbindung berechnen lassen", key="btn_n2"):
        st.session_state["zeige_n2"] = True

    if st.session_state.get("zeige_n2"):
        rs_n2 = np.array(daten["rs_n2"])
        es_n2 = np.array(daten["es_n2"])
        j = int(np.argmin(es_n2))
        tiefe_n2 = (2 * daten["E_N_atom"] - es_n2[j]) * HARTREE_KJ

        fig, ax = neue_figur(3.2)
        ax.plot(rs_n2, (es_n2 - es_n2[j]) * HARTREE_KJ, color=BLAU, lw=2.5)
        ax.scatter([rs_n2[j]], [0], color=ORANGE, s=110, zorder=5)
        ax.axvline(1.098, color=GRUEN, ls="--", lw=1.5)
        ax.text(1.12, 600, "gemessen: 1,098 Å", color=GRUEN, fontsize=9)
        ax.set_xlabel("Abstand der Stickstoffkerne [Ångström]")
        ax.set_ylabel("Energie über dem Minimum [kJ/mol]")
        zeige(fig)

        n1, n2 = st.columns(2)
        n1.metric("Berechnete Bindungsstärke", f"{tiefe_n2:.0f} kJ/mol")
        n2.metric("Gemessen", "945 kJ/mol",
                  delta=f"{tiefe_n2 - 945:+.0f} Abweichung",
                  delta_color="off")

        st.error(
            f"**Das ist kein kleiner Fehler, das ist ein Faktor "
            f"{945/tiefe_n2:.0f}.** Die Bindungslänge trifft das Modell noch "
            f"passabel ({dez(rs_n2[j], 2)} statt 1,098 Å). Die Bindungsstärke "
            "verfehlt es vollständig."
        )
        st.markdown(
            """
Der Grund führt zurück zur Party-Analogie. Hartree-Fock lässt jedes Elektron
nur den **Durchschnitt** aller anderen spüren. In Wirklichkeit weichen sich
Elektronen einzeln und im Moment aus – sie halten Abstand voneinander, und
dieses gegenseitige Ausweichen spart Energie. Das nennt man Korrelation, und
Hartree-Fock lässt sie weg.

Bei zwei Elektronen im H₂ fällt das kaum ins Gewicht. Bei einer
Dreifachbindung, in der sechs Elektronen auf engstem Raum zwischen zwei Kernen
zusammengedrängt sind, ist es der halbe Effekt.
"""
        )
        merksatz(
            "Das Verfahren scheitert genau an der Bindung, an der auch die "
            "Chemie hundert Jahre lang gescheitert ist. Beides hat dieselbe "
            "Ursache: Diese Dreifachbindung ist ein Sonderfall."
        )
        st.info(
            "**Das ist der eigentliche Punkt dieses Kapitels.** Ein Modell "
            "ist nicht richtig oder falsch, sondern innerhalb eines Bereichs "
            "brauchbar. Wer nur die H₂-Kurve gesehen hätte, würde diesem "
            "Verfahren zu viel zutrauen. Die Grenzen eines Modells zu kennen "
            "gehört zum Modell dazu – und wer sie nicht kennt, hat es nicht "
            "verstanden, sondern nur bedient."
        )

    # ---------------------------------------------- Spielwiese
    st.divider()
    code_feld(
        "qm",
        '''# Die Quantenchemie steht dir hier komplett zur Verfuegung.
#
#   qm_energie(atome, spin=0)  ->  Energie in Hartree
#   atome: Liste aus (Element, (x, y, z)) in Angstrom
#   Verfuegbar: H, C, N, O
#   HARTREE_KJ rechnet Hartree in kJ/mol um.

# Beispiel: die Bindungslaenge von Kohlenmonoxid suchen
print("Abstand    Energie")
bester, beste_E = None, 0
for abstand in [0.9, 1.0, 1.1, 1.13, 1.2, 1.3]:
    E = qm_energie([("C", (0, 0, 0)), ("O", (0, 0, abstand))])
    print(f"  {abstand:.2f} A   {E:+.4f} Hartree")
    if E < beste_E:
        bester, beste_E = abstand, E

print()
print(f"Tiefster Punkt bei {bester} Angstrom.")
print("Im Labor gemessen: 1.128 Angstrom.")

# Ideen zum Weiterspielen:
# - Wasser bauen: O in der Mitte, zwei H im Winkel von 104.5 Grad
# - ein Atom weit wegschieben und zusehen, wie die Bindung verschwindet
''',
        hinweis="Ändere Elemente, Positionen, Abstände. Zurücksetzen holt "
                "jederzeit das Original zurück.",
        hoehe=380,
        extras={
            "qm_energie": lambda atome, spin=0: hf_pure.energie(
                list(atome), spin=spin),
            "HARTREE_KJ": HARTREE_KJ,
            "NH3_GEOMETRIE": NH3_GEOMETRIE,
        },
        titel="Selbst mit der Quantenchemie spielen",
    )

    fachkasten(
        "Methode, Grenzen, Zahlen",
        f"""
**Verfahren.** Restricted bzw. Unrestricted Hartree-Fock im Basissatz
STO-3G, implementiert in `hf_pure.py` – reines numpy, keine externe
Quantenchemie-Bibliothek. Die Zwei-Elektronen-Integrale laufen über das
McMurchie-Davidson-Schema, die Boys-Funktion über eine Reihenentwicklung
mit Abwärtsrekursion.

**Basissatz.** STO-3G ist der kleinste gebräuchliche Satz: pro
Atomorbital drei Gaußfunktionen. Er beschreibt die Elektronenwolken sehr
grob. Größere Basissätze (6-31G*, cc-pVTZ) kämen näher heran, kosten aber
ein Vielfaches an Rechenzeit.

**Was fehlt.** Elektronenkorrelation. Hartree-Fock ersetzt die
Wechselwirkung jedes Elektrons mit jedem anderen durch ein gemitteltes
Feld. Der dabei verlorene Energiebeitrag ist bei Mehrfachbindungen groß.

**Ergebnisse dieser App gegen Messwerte:**

| Größe | gerechnet | gemessen |
|---|---|---|
| Bindungslänge H₂ | {dez(daten["r_min_h2"], 2)} Å | 0,741 Å |
| Bindungsstärke H–H | {daten['D_HH']:.0f} kJ/mol | 436 kJ/mol |
| Bindungslänge N₂ | {dez(daten["r_min_n2"], 2)} Å | 1,098 Å |
| Bindungsstärke N≡N | {daten['D_NN']:.0f} kJ/mol | 945 kJ/mol |
| Reaktionsenergie | {daten['dE_reaktion']:.0f} kJ/mol | −92 kJ/mol |

Die N₂-Kurve ist vorberechnet und liegt als `vorberechnet.json` bei, weil
sie live rund eine Minute bräuchte. Alles andere rechnet die App im Moment
des Knopfdrucks.
""",
    )


# ==================================================================
# Kapitel 4
# ==================================================================
def _k4():
    kapitel_kopf(4, N_KAP, "Brot und Sprengstoff",
                 "Dieselbe Anlage, dieselben Menschen, zwei Ergebnisse.")

    st.markdown(
        """
Bis hierher war es eine Erfolgsgeschichte: ein Engpass, eine Reaktion, ein
Kompromiss aus Temperatur und Druck, eine Fabrik. Jetzt der andere Teil.

**Ammoniak ist der Ausgangsstoff für beides.** Aus NH₃ wird über Salpetersäure
sowohl Kunstdünger als auch Sprengstoff. Es ist nicht so, dass es zwei Wege
gäbe, einen guten und einen schlechten. Es ist derselbe Weg bis kurz vor
Schluss.
"""
    )

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Ammoniak weltweit", "≈ 170 Mio. t/Jahr")
    m2.metric("Anteil am Weltenergiebedarf", "1–2 %")
    m3.metric("Anteil am Erdgasverbrauch", "3–5 %")
    st.caption(
        "Quelle: *Green ammonia synthesis*, Editorial, Nature Synthesis 2023. "
        "Dort auch die Angabe, dass 48 % der Weltbevölkerung von Nahrung "
        "leben, die mit synthetischem Dünger gewachsen ist."
    )

    st.divider()
    code_feld(
        "menschen",
        '''# Wie viele Menschen haengen an diesem Verfahren?

weltbevoelkerung = 8.2        # Milliarden
anteil_kunstduenger = 0.48    # Nature Synthesis 2023

menschen = weltbevoelkerung * anteil_kunstduenger
print(f"Rund {menschen:.1f} Milliarden Menschen essen Nahrung,")
print("deren Stickstoff aus diesem Verfahren stammt.")
print()

# Und die andere Seite:
ammoniak_welt = 170           # Millionen Tonnen pro Jahr
anteil_duenger = 0.80

print(f"Weltproduktion Ammoniak:  {ammoniak_welt} Mio. Tonnen/Jahr")
print(f"davon fuer Duenger:       {ammoniak_welt*anteil_duenger:.0f} Mio. t")
print(f"fuer alles andere:        {ammoniak_welt*(1-anteil_duenger):.0f} Mio. t")
print()
print("'Alles andere' heisst: Kunststoffe, Reinigungsmittel - und Sprengstoff.")
''',
        hinweis="Verschieb den Anteil und überleg: Ab welchem Wert wird die "
                "Abschaffung dieses Verfahrens undenkbar?",
        hoehe=380,
        titel="Die Größenordnung selbst ausrechnen",
    )

    st.divider()
    st.markdown(
        """
### Die andere Seite

Vor 1914 importierte das Deutsche Reich seinen Salpeter aus Chile. Mit der
britischen Seeblockade war dieser Weg zu. Nach gängiger Einschätzung hätte der
Munitionsnachschub binnen etwa eines Jahres geendet.

Die Ammoniakanlagen der BASF ersetzten diesen Import. **Der Erste Weltkrieg
konnte auch deshalb jahrelang weitergeführt werden** (vgl. Szöllösi-Janze 1998,
S. 270 f.).

Fritz Haber ging darüber hinaus. Er organisierte den Einsatz chemischer
Kampfstoffe an der Front und war bei Ypern 1915 persönlich anwesend
(vgl. Szöllösi-Janze 1998, S. 320 f.). Seine Frau Clara Immerwahr, selbst
promovierte Chemikerin, nahm sich wenige Tage danach das Leben.

1918 erhielt Haber den Nobelpreis für Chemie – für die Ammoniaksynthese.
1933 musste er als Jude aus Deutschland emigrieren. Er starb 1934 im Exil.
"""
    )
    st.warning(
        "**Die Versuchung ist, sich für eine Seite zu entscheiden.** Held oder "
        "Kriegsverbrecher, Ernährer oder Giftgasorganisator. Beides ist "
        "belegbar, und beides ist zu einfach.\n\n"
        "Interessanter ist die Frage, was der Fall über die Struktur "
        "wissenschaftlicher Arbeit sagt – und ob eine andere Person an Habers "
        "Stelle anders gehandelt hätte."
    )

    st.divider()
    st.markdown(
        """
### Und eine Folge, die niemand geplant hat

Der Stickstoff verschwindet nicht, wenn die Pflanze ihn nicht aufnimmt. Er
sickert ins Grundwasser, er landet in Flüssen und Meeren, wo er Algen wachsen
lässt, die beim Verrotten den Sauerstoff verbrauchen. Ein Teil entweicht als
Lachgas – ein Treibhausgas, das pro Molekül rund 270-mal stärker wirkt als
Kohlendioxid und dazu die Ozonschicht angreift.

Der Mensch bringt heute mehr reaktiven Stickstoff in Umlauf als alle
natürlichen Prozesse der Landökosysteme zusammen. Der Stickstoffkreislauf
gilt in der Forschung zu planetaren Belastungsgrenzen als deutlicher
überschritten als das Klima.
"""
    )


# ==================================================================
# Kapitel 5
# ==================================================================
def _k5():
    kapitel_kopf(5, N_KAP, "Diskussion",
                 "Fünf Fragen für die interdisziplinäre Runde.")

    fragen = [
        ("Ist die Erkenntnis schuldig oder erst die Anwendung?",
         "Die Reaktionsgleichung N₂ + 3 H₂ → 2 NH₃ ist wertfrei. Aus dem "
         "Produkt wird Brot oder Munition, je nachdem, wer die Anlage "
         "besitzt.\n\n"
         "Lässt sich diese Trennung durchhalten? Oder ist sie eine bequeme "
         "Ausrede, zumal Haber die militärische Verwendung nicht nur hinnahm, "
         "sondern selbst betrieb?"),
        ("Hätte man es lassen können?",
         "Angenommen, Haber hätte 1909 abgebrochen. Das Problem wurde weltweit "
         "bearbeitet, die Vorarbeiten lagen vor, der Bedarf war enorm.\n\n"
         "Wenn eine Entdeckung ohnehin fällig ist, ändert individueller "
         "Verzicht dann überhaupt etwas? Und falls nicht: bleibt trotzdem eine "
         "persönliche Verantwortung?"),
        ("Was ist mit den Folgen, die niemand wollte?",
         "Der Stickstoff aus diesen Anlagen landet heute in Grundwasser, in "
         "überdüngten Flüssen und als Lachgas in der Atmosphäre. Diese Folgen "
         "hat weder Haber noch Bosch beabsichtigt oder auch nur gekannt.\n\n"
         "Kann man für etwas verantwortlich sein, das zum Zeitpunkt der "
         "Handlung nicht absehbar war? Hans Jonas hat genau daraus eine neue "
         "Ethik abgeleitet."),
        ("Wer hat das Verfahren eigentlich erfunden?",
         "In Kapitel 2 stand: Die Hälfte des Problems war Chemie, die andere "
         "Hälfte war Stahl. Haber bekam den Nobelpreis 1918, Bosch erst 1931 "
         "und ausdrücklich für Hochdrucktechnik. Gerhard Ertl bekam 2007 einen "
         "dritten – dafür, dass er endlich erklären konnte, warum das Ganze "
         "funktioniert.\n\n"
         "Wen meinen wir, wenn wir von einer Entdeckung sprechen? Die Person "
         "mit der Idee, die mit dem funktionierenden Apparat, oder die mit der "
         "Erklärung? Und was sagt die übliche Antwort über das Fach aus, aus "
         "dem sie kommt?"),
        ("Warum so schnell – und die Quantenmechanik so langsam?",
         "Zwischen Habers Laborreaktion (1909) und der industriellen Anlage "
         "(1913) lagen vier Jahre. Zwischen Schrödingers Gleichung (1926) und "
         "den Rechnungen, die wir gerade in Sekunden gemacht haben, lagen "
         "Jahrzehnte an Theorie und Rechenleistung.\n\n"
         "Woran liegt dieser Unterschied? An der Wissenschaft, an der "
         "wirtschaftlichen Nachfrage, am Krieg? Und was heißt das für die "
         "Frage, wann Forschung überhaupt steuerbar ist?"),
    ]

    for titel, text in fragen:
        with st.expander(titel):
            st.write(text)
