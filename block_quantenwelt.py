# -*- coding: utf-8 -*-
"""
Block 2: Die Quantenwelt.

Roter Faden:
  K1  Ein Problem, das die klassische Physik nicht lösen konnte.
  K2  Das einfachste Modell überhaupt: ein Teilchen in einem Kasten.
  K3  Aus dem Modell folgt eine Energieleiter und die Antwort auf K1.
  K4  Aus einem Sprung auf der Leiter wird Licht, das man messen kann.
  K5  Dieselbe Gleichung rechnet echte Moleküle, live in dieser App.
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from bausteine import (
    BLAU, ORANGE, GRAU, GRUEN, ROT, H_PLANCK, C_LICHT, M_E, EV,
    HARTREE_KJ, EV_ZIMMER, EV_IN_KJ_MOL, dez, ev_einordnung, merksatz,
    kapitel_kopf, zeige, neue_figur, fachkasten, schaetzfrage, code_feld,
)

try:
    import hf_pure
    HF_DA = True
except ImportError:
    HF_DA = False

KAPITEL = [
    "1 · Warum es die Quantenmechanik gibt",
    "2 · Das Teilchen im Kasten",
    "3 · Die Energieleiter",
    "4 · Farbe aus dem Sprung",
    "5 · Moleküle selbst rechnen",
]
N_KAP = len(KAPITEL)

# Ammoniak, Geometrie aus dem Experiment (Bindungslänge 1,012 Å,
# Winkel 106,7 Grad), in Ångström.
NH3_GEOMETRIE = (
    ("N", (0.000000, 0.000000, 0.116489)),
    ("H", (0.000000, 0.939731, -0.271808)),
    ("H", (0.813831, -0.469865, -0.271808)),
    ("H", (-0.813831, -0.469865, -0.271808)),
)

# Gemessene Vergleichswerte für Kapitel 5.
# D_e ist die Tiefe des Energietals. Der geläufige Tabellenwert liegt
# darunter, weil ein Molekül nie ganz am Boden des Tals sitzt.
R_H2, DE_H2 = 0.741, 458.0        # Å, kJ/mol
R_N2, DE_N2 = 1.098, 956.0        # Å, kJ/mol
DH_REAKTION = -92.0               # kJ/mol, Reaktionsenthalpie bei 25 °C


# ==================================================================
# Physik des Kastens
# ==================================================================
def energie(n, L, m=M_E):
    """Energie des n-ten Zustands im Kasten der Breite L (SI-Einheiten)."""
    return (n ** 2 * H_PLANCK ** 2) / (8 * m * L ** 2)


def psi(n, L, x):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)


def wellenlaenge_zu_farbe(wl_nm):
    """Grobe Umrechnung sichtbare Wellenlänge in RGB. Nur zur Anschauung."""
    wl = wl_nm
    if wl < 380 or wl > 750:
        return "#444444"
    if wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def plot_zustand(n, L_nm, modus="welle"):
    L = L_nm * 1e-9
    x = np.linspace(0, L, 600)
    y = psi(n, L, x)
    x_nm = x * 1e9

    fig, ax = plt.subplots(figsize=(7, 3.2))
    if modus == "wahrscheinlichkeit":
        y = y ** 2
        ax.fill_between(x_nm, y, alpha=0.4, color=ORANGE)
        ax.plot(x_nm, y, color=ORANGE, lw=2)
        ax.set_ylabel("Wahrscheinlichkeit")
        ax.set_ylim(bottom=0)
    else:
        ax.plot(x_nm, y, color=BLAU, lw=2.5)
        ax.axhline(0, color="grey", lw=0.8)
        ax.set_ylabel("Welle ψ")
    ax.axvline(0, color="black", lw=5)
    ax.axvline(L_nm, color="black", lw=5)
    ax.set_xlabel("Ort im Kasten [Nanometer]")
    ax.set_xlim(-0.05 * L_nm, 1.05 * L_nm)
    ax.set_yticks([])
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    return fig


# ==================================================================
# Quantenchemie
# ==================================================================
@st.cache_data(show_spinner=False)
def qm_energie(atome, spin=0):
    """Gesamtenergie eines Moleküls, in Hartree."""
    return hf_pure.energie(list(atome), spin=spin)


def zeichne(kapitel):
    [_k1, _k2, _k3, _k4, _k5][KAPITEL.index(kapitel)]()


# ==================================================================
# Kapitel 1
# ==================================================================
def _k1():
    kapitel_kopf(1, N_KAP, "Warum es die Quantenmechanik gibt",
                 "Ein Problem, das die klassische Physik nicht lösen konnte.")
    st.markdown(
        """
Um 1900 war die Physik ziemlich zufrieden mit sich. Man konnte Planeten
berechnen, Dampfmaschinen bauen und Brücken auslegen. Die Welt schien im
Prinzip verstanden.

Dann kamen Experimente, die **nicht passten**. Und zwar nicht ein bisschen
daneben, sondern grundsätzlich.

Das bekannteste Problem: Ein Atom besteht aus einem Kern und aus Elektronen,
die um ihn herum sind. Nach der klassischen Physik müsste ein kreisendes
Elektron ständig Energie abstrahlen, langsamer werden und **innerhalb von
Sekundenbruchteilen in den Kern stürzen**.

Tut es aber nicht. Du bist der Beweis: Du bestehst aus Atomen und die sind
seit Milliarden Jahren stabil.
"""
    )
    merksatz("Die klassische Physik konnte nicht erklären, warum es dich gibt.")
    st.markdown(
        """
Die Antwort darauf heißt Quantenmechanik. Erwin Schrödinger brachte sie 1926
in eine einzige Gleichung. Sie gilt als unverständlich. Ihr Kern ist es nicht.
Genau den bauen wir in den nächsten vier Kapiteln auf.

Unser Werkzeug dafür ist das einfachste Beispiel, das es gibt: **ein Teilchen,
das in einem Kasten eingesperrt ist.** Mehr nicht.
"""
    )


# ==================================================================
# Kapitel 2
# ==================================================================
def _k2():
    kapitel_kopf(2, N_KAP, "Das Teilchen im Kasten",
                 "Erst etwas Vertrautes, dann dasselbe mit einem Elektron.")

    st.markdown(
        """
Eine Gitarrensaite ist an **beiden Enden festgeklemmt**. Genau das ist der
Punkt. Wenn du sie zupfst, kann sie nicht irgendwie schwingen, sondern nur so,
dass sie an den Enden stillsteht. Es passen also nur bestimmte Wellen hinein.
"""
    )

    saite = st.slider("Wie viele Bäuche soll die Saite haben?", 1, 6, 1)
    x = np.linspace(0, 1, 500)
    fig, ax = plt.subplots(figsize=(7, 2.4))
    for phase in np.linspace(-1, 1, 7):
        ax.plot(x, phase * np.sin(saite * np.pi * x), color=BLAU,
                alpha=0.25, lw=1)
    ax.plot(x, np.sin(saite * np.pi * x), color=BLAU, lw=2.5)
    ax.plot(x, -np.sin(saite * np.pi * x), color=BLAU, lw=2.5)
    ax.axvline(0, color="black", lw=6)
    ax.axvline(1, color="black", lw=6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[:].set_visible(False)
    fig.tight_layout()
    zeige(fig)

    st.markdown(
        """
Zwei Beobachtungen, auf denen alles Weitere aufbaut:

**Eingesperrt sein erzeugt Auswahl.** Eine freie Welle im Raum kann jede Form
annehmen. Eine eingeklemmte kann das nicht mehr.

**Die Auswahl ist abzählbar.** Man kann die erlaubten Schwingungen
durchnummerieren: die erste, die zweite, die dritte. Keine Zwischenstufen.

Das ist keine geheimnisvolle Physik, sondern Handwerk. Jeder Instrumentenbauer
weiß es seit Jahrhunderten.
"""
    )
    merksatz("Die Behauptung der Quantenmechanik lautet: "
             "<b>Materie macht das auch.</b>")

    # -------------------------------------------------- der Kasten
    st.divider()
    st.subheader("Dasselbe mit einem Elektron")
    st.markdown(
        """
Jetzt sperren wir statt einer Saite ein **Elektron** ein, in einen winzigen
Kasten, aus dem es nicht heraus kann. Es verhält sich wie die eingeklemmte
Saite. Es hat eine **Welle** und diese Welle muss an den Wänden auf null
gehen.
"""
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        n = st.slider("Quantenzahl n", 1, 8, 1)
    with c2:
        L_nm = st.slider("Kastenbreite L [Nanometer]", 0.2, 3.0, 1.0, 0.1)
    with c3:
        modus = st.radio("Ansicht", ["Welle ψ", "Aufenthalt ψ²"])

    zeige(plot_zustand(
        n, L_nm, "wahrscheinlichkeit" if "ψ²" in modus else "welle"))

    E_n = energie(n, L_nm * 1e-9)
    k1, k2, k3 = st.columns(3)
    k1.metric("Energie", f"{dez(E_n / EV, 3)} eV")
    k2.metric("Bäuche", f"{n}")
    k3.metric("Nullstellen innen", f"{n - 1}")
    st.caption(ev_einordnung(E_n / EV))

    st.markdown(
        """
**n ist eine Hausnummer und keine Messgröße.** Sie zählt durch, um welche der
erlaubten Wellen es geht. n gleich 1 ist die einfachste, ein einziger Bauch,
der ruhigste Zustand. n ist immer eine ganze Zahl, ein n gleich 1,5 gibt es
nicht.

**Und die Welle ist keine Welle aus einem Stoff.** Das Elektron wackelt nicht
auf und ab wie ein Seil. Diese Welle heißt **Wellenfunktion ψ** und ist eine
Rechengröße. Ihre Bedeutung steckt im Quadrat: Wo ψ² groß ist, findet man das
Teilchen wahrscheinlich, wo es null ist, nie. Schalte oben auf *Aufenthalt ψ²*
um, dann siehst du es.
"""
    )

    with st.expander("**Was ist ein eV?**"):
        st.markdown(
            f"""
Ein **Elektronenvolt** ist die Portionsgröße, wenn man über einzelne
Elektronen spricht, so wie man Reis in Körnern zählt und nicht in Kilogramm.
Man muss sich nur einen einzigen Wert merken, dann ordnet sich alles ein:

| Energie | Was das ist |
|---|---|
| 0,025 eV | die Wärme in diesem Raum, pro Teilchen |
| 1,8 bis 3,1 eV | sichtbares Licht, von Rot bis Violett |
| 4 eV | UV-Strahlung, die Sonnenbrand macht |
| 9,8 eV | die Dreifachbindung im Stickstoff aus Block 1 |
| 13,6 eV | genug, um ein Wasserstoffatom zu zerlegen |

Dein Elektron im Kasten hat gerade **{dez(E_n/EV, 3)} eV**, also das
{dez(E_n/EV/EV_ZIMMER, 0)}-fache der Zimmerwärme.

Für die aus der Chemie: 1 eV entspricht 96,5 kJ/mol.
"""
        )


# ==================================================================
# Kapitel 3
# ==================================================================
def _k3():
    kapitel_kopf(3, N_KAP, "Die Energieleiter",
                 "Eine Treppe ohne Rampe und die Antwort auf Kapitel 1.")
    st.markdown(
        "Jede erlaubte Welle gehört zu einer bestimmten Energie. Da es nur "
        "bestimmte Wellen gibt, gibt es auch **nur bestimmte Energien**."
    )

    st.subheader("Erst raten")
    schaetzfrage(
        "kasten_halb",
        "Du machst den Kasten halb so breit. Um welchen Faktor steigt die "
        "Energie des untersten Zustands?",
        1.0, 10.0, 2.0, 0.5, 4.0,
        einheit="fach", format_str="%.1f", toleranz_gut=0.6,
        aufloesung_text=(
            "**Vierfach.** Die Energie wächst mit dem Quadrat der Quantenzahl "
            "und fällt mit dem Quadrat der Breite. Halbe Breite heißt also "
            "vierfache Energie. Genau diese Empfindlichkeit ist der Grund, "
            "warum die Quantenmechanik im Kleinen alles bestimmt und im "
            "Großen nicht auffällt."
        ),
    )

    st.divider()
    L_nm = st.slider("Kastenbreite L [Nanometer]", 0.2, 3.0, 1.0, 0.1,
                     key="l3")
    n_sel = st.slider("Markierter Zustand n", 1, 8, 1, key="n3")
    L = L_nm * 1e-9

    fig, ax = plt.subplots(figsize=(7, 3.6))
    for k in range(1, 9):
        E_k = energie(k, L) / EV
        farbe = ORANGE if k == n_sel else GRAU
        ax.hlines(E_k, 0, 1, color=farbe, lw=3 if k == n_sel else 1.5)
        ax.text(1.03, E_k, f"n={k}", va="center", fontsize=9, color=farbe)
    ax.set_ylabel("Energie [eV]")
    ax.set_xticks([])
    ax.set_xlim(0, 1.3)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    fig.tight_layout()
    zeige(fig)

    E_sel = energie(n_sel, L) / EV
    m1, m2 = st.columns(2)
    m1.metric(f"Energie bei n = {n_sel}", f"{dez(E_sel, 3)} eV")
    m2.metric("In Chemikersprache", f"{dez(E_sel * EV_IN_KJ_MOL, 0)} kJ/mol")
    st.caption(ev_einordnung(E_sel))

    st.markdown(
        """
**Das ist eine Treppe ohne Rampe.** Zwischen den Stufen ist nichts. Nicht
schwer erreichbar, sondern nicht existent. Genau daher kommt der Name:
*quantum* heißt auf Lateinisch „wie viel“, ein Quantum ist eine abgezählte
Portion.

Zwei Dinge sieht man sofort. Erstens werden die Stufen nach oben immer weiter
auseinander, weil die Energie mit n² wächst. Zweitens gilt: Je enger der
Kasten, desto größer die Abstände. Zieh den Breiten-Regler klein und schau zu.
"""
    )
    st.warning(
        "**Das ist der Satz, auf den es ankommt:**\n\n"
        "Je enger du ein Teilchen einsperrst, desto heftiger wehrt es sich. "
        "Ein eingesperrtes Teilchen kann nicht stillstehen, es hat immer eine "
        "Mindestenergie. Sie heißt **Nullpunktsenergie**.\n\n"
        "Damit ist Kapitel 1 beantwortet. Ein Elektron im Atomkern wäre "
        "extrem eng eingesperrt und bräuchte dafür absurd viel Energie. Die "
        "hat es nicht. Also bleibt es draußen und Atome sind stabil."
    )

    # -------------------------------------------------- Makro-Probe
    st.divider()
    st.subheader("Warum du davon nichts merkst")
    st.markdown(
        "Dieselbe Formel, andere Zahlen. Wir sperren statt eines Elektrons "
        "**dich** in einen Raum."
    )

    c1, c2 = st.columns(2)
    with c1:
        masse = st.number_input("Dein Gewicht [kg]", 30.0, 200.0, 70.0, 5.0)
    with c2:
        raum = st.number_input("Raumbreite [m]", 1.0, 20.0, 5.0, 0.5)

    sprung = energie(2, raum, masse) - energie(1, raum, masse)
    st.metric("Dein Sprung von n = 1 auf n = 2", f"{sprung:.2e} Joule")
    st.markdown(
        f"""
Zum Vergleich: Ein Sandkorn einen Millimeter anzuheben kostet ungefähr
0,00000001 Joule, also rund **{1e-8 / sprung:.0e} mal mehr**.

Deine Energiestufen sind also da. Sie liegen nur so absurd eng beieinander,
dass keine Messung der Welt sie unterscheiden könnte.
"""
    )
    merksatz(
        "Die Quantenmechanik hat die klassische Physik nicht widerlegt, "
        "sondern <b>eingeordnet</b>. Newton ist nicht falsch, sondern ein "
        "Grenzfall für große, schwere Dinge. Dieser stimmt dort so gut, dass "
        "wir bis heute Raumsonden damit steuern."
    )

    fachkasten(
        "Die Formel und ihre Grenzen",
        """
**Energie im Kasten:** *E<sub>n</sub>* = *n*² *h*² / (8 *m* *L*²) mit
*h* = 6,626 · 10⁻³⁴ J·s.

**Das Modell ist eine Idealisierung.** Es setzt unendlich hohe Wände voraus,
ein einziges Teilchen ohne Wechselwirkung, eine einzige Raumrichtung und keine
Relativität. Ein echtes Elektron in einem echten Kristall sitzt in keinem
solchen Kasten. Die Rechnung mit einem Menschen im Zimmer ist ein
Gedankenexperiment und kein Messvorschlag.

Trotzdem trifft das Modell die Größenordnung von Quantenpunkten, von
Farbstoffmolekülen mit langen konjugierten Ketten und von Elektronen in dünnen
Halbleiterschichten. Überall dort also, wo Eingesperrtsein die wesentliche
Eigenschaft ist.

**Brücke zu Block 1:** 1 eV = 96,485 kJ/mol. Ein Elektron im 1-nm-Kasten hat
im Grundzustand 0,376 eV, also 36 kJ/mol. Das ist etwa ein Sechsundzwanzigstel
der Stickstoff-Dreifachbindung.
""",
    )


# ==================================================================
# Kapitel 4
# ==================================================================
def _k4():
    kapitel_kopf(4, N_KAP, "Farbe aus dem Sprung",
                 "Hier wird die Theorie zum ersten Mal sichtbar.")
    st.markdown(
        """
Fällt ein Teilchen von einer Stufe auf eine tiefere, muss die Energiedifferenz
irgendwo hin. Sie wird als **Lichtteilchen** abgegeben. Dessen Energie
bestimmt die **Farbe**. Große Differenz heißt blau, kleine Differenz heißt
rot.
"""
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        n_hoch = st.selectbox("Von n =", [2, 3, 4, 5, 6], index=0)
    with c2:
        n_tief = st.selectbox("Nach n =", [1, 2, 3, 4, 5], index=0)
    with c3:
        L_nm = st.slider("L [nm]", 0.4, 2.0, 0.7, 0.05, key="l4")

    if n_hoch <= n_tief:
        st.error("Der Startzustand muss höher liegen als der Zielzustand.")
        return

    L = L_nm * 1e-9
    dE = energie(n_hoch, L) - energie(n_tief, L)
    wl_nm = (H_PLANCK * C_LICHT / dE) * 1e9

    m1, m2 = st.columns(2)
    m1.metric("Freigesetzte Energie", f"{dez(dE / EV, 2)} eV")
    m2.metric("Wellenlänge", f"{dez(wl_nm, 0)} nm")

    fig, ax = plt.subplots(figsize=(7, 1.0))
    ax.add_patch(plt.Rectangle((0, 0), 1, 1,
                               color=wellenlaenge_zu_farbe(wl_nm)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.tight_layout()
    zeige(fig)

    if 380 <= wl_nm <= 750:
        st.success(f"Sichtbares Licht bei {wl_nm:.0f} nm.")
    elif wl_nm < 380:
        st.info(f"{wl_nm:.0f} nm, also Ultraviolett und für dein Auge "
                "unsichtbar.")
    else:
        st.info(f"{wl_nm:.0f} nm, also Infrarot und spürbar als Wärme.")
    st.caption(
        "Grau heißt nicht „keine Farbe“, sondern „außerhalb dessen, was dein "
        "Auge aufnimmt“. Die Strahlung ist da, du siehst sie nur nicht."
    )

    merksatz("Aus der Treppe wird Licht, das man messen kann. So prüft man "
             "diese ganze Theorie überhaupt nach.")

    st.divider()
    st.subheader("Das steckt in deinem Fernseher")
    st.markdown(
        """
Winzige Kristalle von wenigen Nanometern Größe heißen **Quantenpunkte**. Ihre
Farbe hängt nicht nur vom Material ab, sondern vor allem von ihrer **Größe**,
genau nach dem Prinzip, an dem du gerade drehst.

Kleiner Punkt heißt enger Kasten, enger Kasten heißt größere Sprünge, größere
Sprünge heißen blaueres Licht.

In QLED-Fernsehern steckt genau das. Die Kastenbreite, an der du hier
herumschiebst, ist dort eine Fertigungstoleranz.
"""
    )

    st.divider()
    st.subheader("Und der Bogen zurück zum Dünger")
    st.markdown(
        """
Dieselbe Formel, die hier aus einem Energieunterschied eine Farbe macht,
beantwortet auch die offene Frage aus Block 1.

Die Dreifachbindung im Stickstoff entspricht **9,8 eV**. Ein Lichtteilchen mit
dieser Energie hätte eine Wellenlänge von **127 Nanometern**. Das ist tiefes
Ultraviolett. Die Atmosphäre filtert es vollständig weg.
"""
    )
    st.info(
        "**Deshalb düngt Sonnenlicht nicht.** Es ist nicht zu schwach im Sinne "
        "von zu wenig, sondern die einzelnen Portionen sind zu klein. Tausend "
        "rote Photonen ersetzen kein ultraviolettes. Das ist dasselbe Prinzip "
        "wie bei der Treppe ohne Rampe."
    )


# ==================================================================
# Kapitel 5
# ==================================================================
def _k5():
    kapitel_kopf(5, N_KAP, "Moleküle selbst rechnen",
                 "Bis hierher kamen alle Zahlen aus Messungen. Jetzt keine "
                 "mehr.")

    st.markdown(
        """
Alles, was in Block 1 stand, also Bindungsstärken, Reaktionsenergien und
Ausbeuten, stammt aus dem Labor. Jemand hat gemessen.

Seit 1926 gibt es einen zweiten Weg. Schrödingers Gleichung behauptet: Wenn du
sagst, **wo die Atomkerne stehen** und **wie viele Elektronen es gibt**, folgt
alles Übrige daraus. Sonst braucht es nichts.

Diese Behauptung prüfen wir jetzt nach. Jede Zahl auf dieser Seite entsteht im
Moment des Knopfdrucks.
"""
    )

    if not HF_DA:
        st.error("Die Datei `hf_pure.py` liegt nicht neben der App. Ohne sie "
                 "kann dieses Kapitel nicht rechnen.")
        st.stop()

    with st.expander("**Wie macht der Computer das?**"):
        st.markdown(
            """
Exakt lösen lässt sich die Gleichung nur für ein einziges Elektron. Sobald es
mehrere sind, hängt jedes davon ab, wo alle anderen gerade sind. Alle hängen
also gleichzeitig voneinander ab. Dafür gibt es keine geschlossene Lösung.

Der Ausweg ist eine Vereinfachung. Man tut so, als spüre jedes Elektron nicht
die einzelnen anderen, sondern nur deren Durchschnitt. Stell dir eine volle
Halle vor: Statt auszurechnen, wie jeder Gast jedem einzelnen anderen
ausweicht, nimmt man an, jeder gehe einfach durch eine gleichmäßig dichte
Menge.

Damit wird die Rechnung machbar, aber sie beißt sich in den Schwanz. Der
Durchschnitt hängt davon ab, wo die Elektronen sind. Wo sie sind, hängt
vom Durchschnitt ab. Also rät der Computer eine erste Verteilung, rechnet
daraus eine neue, rechnet daraus wieder eine neue und wiederholt das, bis sich
nichts mehr ändert. Was dann übrig bleibt, ist die Antwort.

Das ist grob, aber schnell. Man weiß außerdem genau, was weggelassen wurde. Am Ende
dieses Kapitels sehen wir, wo die Vereinfachung zusammenbricht.
"""
        )

    # ---------------------------------------------- Schritt 1
    st.divider()
    st.subheader("Schritt 1 · Rate gegen den Computer")
    st.markdown(
        """
Wir nehmen das einfachste Molekül überhaupt: **H₂**, also zwei
Wasserstoffatome mit zwei Elektronen. Die einzige Frage lautet, wie weit die
beiden Kerne voneinander entfernt stehen. Ein Ångström ist ein
Zehnmilliardstel Meter und ungefähr die Größe eines Atoms.
"""
    )

    tipp = st.slider("Dein Tipp für den Abstand [Ångström]",
                     0.40, 2.20, 1.20, 0.01, key="tipp_h2")

    if st.button("Rechnen lassen und vergleichen", type="primary",
                 key="btn_h2"):
        balken = st.progress(0.0, "Schrödinger-Gleichung wird gelöst …")
        rs = np.round(np.arange(0.40, 2.41, 0.04), 3)
        es = []
        for k, r in enumerate(rs):
            es.append(qm_energie((("H", (0, 0, 0)), ("H", (0, 0, float(r))))))
            balken.progress((k + 1) / len(rs),
                            f"Abstand {r:.2f} Å ({k+1} von {len(rs)})")
        E_H = qm_energie((("H", (0, 0, 0)),), spin=1)
        balken.empty()
        st.session_state["h2"] = (rs.tolist(), es, tipp, E_H)

    if "h2" in st.session_state:
        rs, es, tipp_alt, E_H = st.session_state["h2"]
        rs, es = np.array(rs), np.array(es)
        i = int(np.argmin(es))
        r_rechnung = rs[i]
        tiefe = (2 * E_H - es[i]) * HARTREE_KJ

        fig, ax = neue_figur(3.4)
        ax.plot(rs, (es - es[i]) * HARTREE_KJ, "-", color=BLAU, lw=2.5)
        ax.scatter([r_rechnung], [0], color=ORANGE, s=110, zorder=5)
        ax.axvline(R_H2, color=GRUEN, ls="--", lw=1.5)
        ax.axvline(tipp_alt, color=ROT, ls=":", lw=1.8)
        ax.set_ylim(-40, 600)
        ax.text(R_H2 + 0.02, 480, "gemessen", color=GRUEN, fontsize=9)
        ax.text(tipp_alt + 0.02, 400, "dein Tipp", color=ROT, fontsize=9)
        ax.set_xlabel("Abstand der beiden Kerne [Ångström]")
        ax.set_ylabel("Energie über dem Minimum [kJ/mol]")
        zeige(fig)

        d1, d2, d3 = st.columns(3)
        d1.metric("Dein Tipp", f"{dez(tipp_alt, 2)} Å")
        d2.metric("Der Computer", f"{dez(r_rechnung, 2)} Å")
        d3.metric("Das Labor", f"{dez(R_H2, 3)} Å")

        if abs(tipp_alt - R_H2) < abs(r_rechnung - R_H2):
            st.success(
                "**Du warst näher dran als die Rechnung.** Das ist keine "
                "Blamage für die Quantenmechanik. Der Computer hatte keine "
                "Vorkenntnis, du schon. Er hat den Wert hergeleitet, du hast "
                "ihn geschätzt."
            )
        else:
            st.success(
                "**Der Computer war näher.** Bemerkenswert ist nicht, dass er "
                "gewinnt, sondern womit. Eingegeben wurden zwei Protonen und "
                "zwei Elektronen."
            )

        st.markdown(
            """
Die Kurve erzählt die ganze Geschichte einer chemischen Bindung. Links stoßen
sich die Kerne ab und die Energie schießt hoch. Rechts ist die Bindung
schlicht nicht mehr da. Das **Tal in der Mitte** ist die Bindung. Seine Lage
ist die Bindungslänge, seine Tiefe die Bindungsstärke.
"""
        )
        e1, e2 = st.columns(2)
        e1.metric("Berechnete Tiefe des Tals", f"{tiefe:.0f} kJ/mol")
        e2.metric("Gemessene Tiefe", f"{DE_H2:.0f} kJ/mol")
        st.caption(
            f"Die Rechnung macht die Bindung rund "
            f"{abs(tiefe-DE_H2)/DE_H2*100:.0f} Prozent zu stark. Für ein "
            "Ergebnis, in das kein einziger Messwert eingeflossen ist, ist "
            "das erstaunlich nah. Der geläufige Tabellenwert von 436 kJ/mol "
            "ist übrigens kleiner als diese Taltiefe, weil ein Molekül nie "
            "ganz am Boden des Tals sitzt. Es behält die Nullpunktsenergie "
            "aus Kapitel 3."
        )

    # ---------------------------------------------- Schritt 2
    st.divider()
    st.subheader("Schritt 2 · Die Haber-Bosch-Reaktion")
    st.latex(r"\mathrm{N_2} + 3\,\mathrm{H_2} \;\longrightarrow\; "
             r"2\,\mathrm{NH_3}")
    st.markdown(
        "Derselbe Trick, dreimal angewandt: für N₂, für H₂ und für NH₃. Aus "
        "den drei Energien folgt, ob die Reaktion Energie freisetzt oder "
        "welche braucht."
    )

    tipp_vz = st.radio(
        "**Bevor gerechnet wird: Was glaubst du?**",
        ["Die Reaktion braucht Energie",
         "Ungefähr null, es hebt sich auf",
         "Die Reaktion setzt Energie frei"],
        index=None, key="vz_tipp",
    )

    if st.button("Jetzt rechnen (ein paar Sekunden)", type="primary",
                 key="btn_hb", disabled=tipp_vz is None):
        balken = st.progress(0.0, "Drei Moleküle werden durchgerechnet …")
        E_H2 = qm_energie((("H", (0, 0, 0)), ("H", (0, 0, 0.74))))
        balken.progress(0.33, "H₂ fertig, jetzt N₂ …")
        E_N2 = qm_energie((("N", (0, 0, 0)), ("N", (0, 0, R_N2))))
        balken.progress(0.66, "N₂ fertig, jetzt NH₃ …")
        E_NH3 = qm_energie(NH3_GEOMETRIE)
        balken.empty()
        st.session_state["dE"] = (2 * E_NH3 - (E_N2 + 3 * E_H2)) * HARTREE_KJ

    if "dE" in st.session_state:
        dE = st.session_state["dE"]
        st.metric("Berechnete Reaktionsenergie", f"{dE:+.0f} kJ/mol")
        if bool(tipp_vz) and tipp_vz.startswith("Die Reaktion setzt"):
            st.success(
                "**Dein Tipp stimmt und die Rechnung bestätigt ihn.** Das "
                "Minuszeichen heißt: Energie wird frei."
            )
        else:
            st.info(
                "**Das Vorzeichen ist negativ, also wird Energie frei.** Das "
                "ist erstaunlich, wenn man Block 1 im Kopf hat. Die Reaktion "
                "*will* laufen, sie kommt nur nicht los. Bei Haber-Bosch geht "
                "es nie darum, die Reaktion energetisch zu ermöglichen, "
                "sondern nur darum, ihr den Weg zu bahnen."
            )
        st.markdown(
            f"""
Gemessen werden für diese Reaktion **{DH_REAKTION:.0f} kJ/mol**, berechnet
sind es {dE:+.0f}. Der Unterschied sieht nach einem groben Fehler aus, ist
aber größtenteils keiner. Die Rechnung kennt nur die Elektronen bei
festgehaltenen Kernen. Die Kerne stehen aber nie still, denn jedes Molekül
behält die Nullpunktsenergie aus Kapitel 3. Ammoniak hat davon deutlich
mehr als N₂ und H₂ zusammen. Zählt man sie dazu, bleiben rund 10 kJ/mol
Unterschied.
"""
        )

    # ---------------------------------------------- Schritt 3
    st.divider()
    st.subheader("Schritt 3 · Wo das Verfahren zusammenbricht")
    st.markdown(
        "Bindungslänge fast richtig, Vorzeichen richtig, Reaktionsenergie "
        "brauchbar. Man könnte den Eindruck bekommen, das Verfahren sei "
        "zuverlässig. Ist es nicht. Es versagt ausgerechnet an der "
        "Bindung, um die sich der ganze Nachmittag dreht."
    )

    if st.button("Die N≡N-Dreifachbindung berechnen lassen", key="btn_n2"):
        with st.spinner("Stickstoff wird gerechnet …"):
            E_N2 = qm_energie((("N", (0, 0, 0)), ("N", (0, 0, R_N2))))
            E_N = qm_energie((("N", (0, 0, 0)),), spin=3)
        st.session_state["n2"] = (2 * E_N - E_N2) * HARTREE_KJ

    if "n2" in st.session_state:
        tiefe_n2 = st.session_state["n2"]
        n1, n2 = st.columns(2)
        n1.metric("Berechnete Bindungsstärke", f"{tiefe_n2:.0f} kJ/mol")
        n2.metric("Gemessen", f"{DE_N2:.0f} kJ/mol")
        st.error(
            f"**Das ist kein kleiner Fehler, das ist ein Faktor "
            f"{DE_N2/tiefe_n2:.0f}.**"
        )
        st.markdown(
            """
Der Grund führt zurück zur vollen Halle. Die Rechnung lässt jedes Elektron nur
den **Durchschnitt** aller anderen spüren. In Wirklichkeit weichen sich
Elektronen einzeln und im selben Moment aus, so wie Menschen in einer Menge
einander tatsächlich ausweichen statt durcheinanderzugehen. Dieses Ausweichen
spart Energie. Die Rechnung lässt es weg.

Bei zwei Elektronen im H₂ fällt das kaum ins Gewicht. In einer
Dreifachbindung, wo sechs Elektronen auf engstem Raum zwischen zwei Kernen
zusammengedrängt sind, ist es der halbe Effekt.

Warum die Reaktionsenergie in Schritt 2 trotzdem passt, liegt daran, dass dort
auf beiden Seiten ganze Moleküle stehen. Derselbe Fehler tritt links wie
rechts auf und hebt sich weitgehend auf. Hier dagegen steht ein Molekül gegen
zwei einzelne Atome. Es gibt nichts, was sich aufheben könnte.
"""
        )
        merksatz(
            "Ein Modell ist nicht richtig oder falsch, sondern innerhalb "
            "eines Bereichs brauchbar. Die Grenzen zu kennen gehört zum "
            "Modell dazu. Wer sie nicht kennt, hat es nicht verstanden, "
            "sondern nur bedient."
        )

    # ---------------------------------------------- Spielwiese
    st.divider()
    code_feld(
        "qm",
        '''#   qm_energie(atome, spin=0)  ->  Energie eines Moleküls
#   atome: Liste aus (Element, (x, y, z)) in Ångström, Elemente H, C, N, O
#   Einzelwerte sagen nichts, nur Unterschiede. Mal HARTREE_KJ gibt kJ/mol.

# Kernabstand im Kohlenmonoxid suchen
abstaende = [0.9, 1.0, 1.1, 1.13, 1.2, 1.3]
energien = [qm_energie([("C", (0, 0, 0)), ("O", (0, 0, a))])
            for a in abstaende]
tiefste = min(energien)

print("Abstand    über dem tiefsten Punkt")
for a, E in zip(abstaende, energien):
    print(f"  {a:.2f} A    {(E - tiefste) * HARTREE_KJ:7.1f} kJ/mol")

print()
print(f"Tiefster Punkt bei {abstaende[energien.index(tiefste)]} Ångström.")
print("Gemessen im Kohlenmonoxid: 1.128 Ångström.")

# Mehratomige Moleküle gehen genauso, zum Beispiel Wasser:
#   [("O", (0.0000, 0.0, 0.0000)),
#    ("H", (0.7578, 0.0, 0.5867)),
#    ("H", (-0.7578, 0.0, 0.5867))]
#
# Gemessene Kernabstände in Ångström:
#   H2 0.741   N2 1.098   CO 1.128   O-H im Wasser 0.958
# O2 braucht spin=2, gemessen 1.208.
''',
        hinweis="Ändere Elemente, Positionen und Abstände. Kaputtmachen "
                "kannst du nichts, *Zurücksetzen* holt das Original zurück.",
        hoehe=400,
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
**Verfahren.** Hartree-Fock im Basissatz STO-3G, implementiert in `hf_pure.py`
in reinem numpy, ohne externe Quantenchemie-Bibliothek. Die
Zwei-Elektronen-Integrale laufen über das McMurchie-Davidson-Schema. Das oben
beschriebene Raten und Nachrechnen bis zur Selbstkonsistenz ist das
SCF-Verfahren.

**Basissatz.** STO-3G ist der kleinste gebräuchliche Satz mit drei
Gaußfunktionen pro Atomorbital. Größere Sätze wie 6-31G* oder cc-pVTZ kämen
näher heran, kosten aber ein Vielfaches an Rechenzeit.

**Was fehlt.** Die Elektronenkorrelation. Der dabei verlorene Energiebeitrag
ist bei Mehrfachbindungen groß. Aus demselben Grund wird auch eine stark
gedehnte Bindung zu teuer gerechnet. In der Nähe des Gleichgewichts stimmt
das Verfahren dagegen auf wenige Prozent.

**Was verglichen wird.** Die Rechnung liefert die Tiefe *D*<sub>e</sub> des
Energietals bei festgehaltenen Kernen. Der geläufige Tabellenwert einer
Bindungsenergie ist kleiner, weil er die Nullpunktsschwingung enthält:
H₂ *D*<sub>e</sub> = {DE_H2:.0f} kJ/mol gegenüber 436 kJ/mol im Tabellenwerk,
N₂ {DE_N2:.0f} gegenüber 945.

**Reaktionsenergie.** Berechnet wird die reine Elektronenenergie. Für den
Vergleich mit der gemessenen Reaktionsenthalpie von {DH_REAKTION:.0f} kJ/mol
bei 25 °C fehlen die Nullpunktsschwingungen mit etwa +78 kJ/mol, weil zwei
NH₃ deutlich mehr Schwingungsenergie tragen als N₂ und drei H₂, sowie
kleinere thermische Beiträge und die Volumenarbeit mit zusammen etwa
−15 kJ/mol. Damit landet die Rechnung rund 10 kJ/mol neben dem Messwert.
""",
    )
