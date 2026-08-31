# -*- coding: utf-8 -*-
"""
Block Quantenmechanik – Teilchen im Kasten.

Diese App ersetzt den Impulsvortrag. Links durchklicken, rechts erklären
und mitspielen lassen.

Gegenüber der ursprünglichen Fassung sind vor allem die Energien
übersetzt: Jede eV-Angabe steht neben einem Vergleich, und die
Verbindung zum Haber-Bosch-Block läuft über die Photonenenergie.
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from bausteine import (
    BLAU, ORANGE, GRAU, H_PLANCK, C_LICHT, M_E, EV,
    dez, EV_ZIMMER, ev_einordnung, ev_karten, merksatz, kapitel_kopf, zeige,
    fachkasten, schaetzfrage,
)

KAPITEL = [
    "0 · Worum geht es hier?",
    "1 · Die Gitarrensaite",
    "2 · Das Teilchen im Kasten",
    "3 · Die Energieleiter",
    "4 · Farbe aus dem Sprung",
    "5 · Wo ist das Teilchen?",
    "6 · Warum merkst du nichts?",
    "7 · Diskussion",
]
N_KAP = len(KAPITEL)


# ==================================================================
# Physik
# ==================================================================
def energie(n, L, m=M_E):
    """Energie des n-ten Zustands im Kasten der Breite L (SI-Einheiten)."""
    return (n ** 2 * H_PLANCK ** 2) / (8 * m * L ** 2)


def psi(n, L, x):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)


def wellenlaenge_zu_farbe(wl_nm):
    """Grobe Umrechnung sichtbare Wellenlänge -> RGB-Hex. Nur zur Anschauung."""
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
        ax.set_ylabel("Welle")
    ax.axvline(0, color="black", lw=5)
    ax.axvline(L_nm, color="black", lw=5)
    ax.set_xlabel("Ort im Kasten [Nanometer]")
    ax.set_xlim(-0.05 * L_nm, 1.05 * L_nm)
    ax.set_yticks([])
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    return fig


# ==================================================================
def zeichne(kapitel):
    i = KAPITEL.index(kapitel)
    [_k0, _k1, _k2, _k3, _k4, _k5, _k6, _k7][i]()


# ==================================================================
def _k0():
    kapitel_kopf(0, N_KAP, "Worum geht es hier?",
                 "Ein Problem, das die klassische Physik nicht lösen konnte.")
    st.markdown(
        """
Um 1900 war die Physik ziemlich zufrieden mit sich. Man konnte Planeten
berechnen, Dampfmaschinen bauen, Brücken auslegen. Die Welt schien im Prinzip
verstanden – es fehlten nur noch ein paar Nachkommastellen.

Dann kamen ein paar Experimente, die einfach **nicht passten**. Und zwar nicht
ein bisschen daneben, sondern grundsätzlich.

Das bekannteste Problem: Ein Atom besteht aus einem Kern und Elektronen, die
um ihn herum sind. Nach der klassischen Physik müsste ein kreisendes Elektron
ständig Energie abstrahlen, langsamer werden und **innerhalb von
Sekundenbruchteilen in den Kern stürzen**.

Tut es aber nicht. Du bist der Beweis: Du bestehst aus Atomen, und die sind
seit Milliarden Jahren stabil.
"""
    )
    merksatz("Die klassische Physik konnte nicht erklären, warum es dich gibt.")
    st.info(
        "**Die Antwort**, die daraus entstand, heißt Quantenmechanik. "
        "Sie ist berüchtigt dafür, unverständlich zu sein. "
        "Ist sie aber nicht, zumindest nicht der Kern davon. "
        "Den bauen wir in den nächsten Minuten auf."
    )
    st.markdown(
        """
Unser Werkzeug dafür ist das einfachste Beispiel, das es gibt: **ein Teilchen,
das in einem Kasten eingesperrt ist.** Mehr nicht. Daran kann man fast alles
zeigen, was an der Quantenmechanik neu und verstörend war.
"""
    )
    st.caption("→ Weiter zu Kapitel 1 in der Navigation links. "
               "Alle Fachwörter stehen im Werkzeugkasten.")


# ==================================================================
def _k1():
    kapitel_kopf(1, N_KAP, "Die Gitarrensaite",
                 "Etwas Vertrautes, bevor es ungewohnt wird.")
    st.markdown(
        """
Eine Gitarrensaite ist an **beiden Enden festgeklemmt**. Genau das ist der
entscheidende Punkt. Wenn du sie zupfst, kann sie nicht irgendwie schwingen,
sie kann nur so schwingen, dass sie an den Enden stillsteht.

Es passen also nur bestimmte Wellen hinein:
"""
    )

    saite = st.slider("Wie viele Bäuche soll die Saite haben?", 1, 6, 1)

    x = np.linspace(0, 1, 500)
    fig, ax = plt.subplots(figsize=(7, 2.6))
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
        f"""
Bei **{saite} {'Bauch' if saite == 1 else 'Bäuchen'}** klingt die Saite in
einem ganz bestimmten Ton. Dazwischen gibt es nichts. Es gibt keinen Ton
„zwischen“ dem ersten und dem zweiten Oberton – jedenfalls nicht auf dieser
Saite mit dieser Länge.

Und jetzt die zwei Beobachtungen, auf die alles Weitere aufbaut:
"""
    )
    st.success(
        "**1. Eingesperrt sein erzeugt Auswahl.** Eine freie Welle im Raum "
        "kann jede beliebige Form annehmen. Eine eingeklemmte kann das nicht "
        "mehr."
    )
    st.success(
        "**2. Die Auswahl ist abzählbar.** Du kannst die erlaubten "
        "Schwingungen durchnummerieren: die erste, die zweite, die dritte. "
        "Keine Zwischenstufen."
    )
    st.markdown(
        """
Das ist keine geheimnisvolle Physik. Das ist Handwerk – jeder Instrumentenbauer
weiß das seit Jahrhunderten.
"""
    )
    merksatz("Die einzige Behauptung der Quantenmechanik lautet: "
             "<b>Materie macht das auch.</b>")


# ==================================================================
def _k2():
    kapitel_kopf(2, N_KAP, "Das Teilchen im Kasten",
                 "Dieselbe Regel, anderes Objekt.")
    st.markdown(
        """
Jetzt sperren wir statt einer Saite ein **Elektron** ein. In einen winzigen
Kasten, aus dem es nicht heraus kann.

Der überraschende Befund der Quantenmechanik: Ein eingesperrtes Teilchen
verhält sich wie eine eingeklemmte Saite. Es hat eine **Welle**, und diese
Welle muss an den Wänden auf null gehen.
"""
    )

    c1, c2 = st.columns(2)
    with c1:
        n = st.slider("Quantenzahl n", 1, 8, 1)
    with c2:
        L_nm = st.slider("Kastenbreite L [Nanometer]", 0.2, 3.0, 1.0, 0.1)

    zeige(plot_zustand(n, L_nm, "welle"))

    L = L_nm * 1e-9
    E_n = energie(n, L)

    k1, k2, k3 = st.columns(3)
    k1.metric("Energie", f"{dez(E_n / EV, 3)} eV")
    k2.metric("Bäuche", f"{n}")
    k3.metric("Nullstellen innen", f"{n - 1}")
    st.caption(ev_einordnung(E_n / EV))

    with st.expander("**Was ist ein eV eigentlich?** (kurz und schmerzlos)"):
        st.markdown(
            f"""
Ein **Elektronenvolt** ist die natürliche Portionsgröße, wenn man über
einzelne Elektronen spricht – so wie man Reis in Körnern zählt und nicht in
Kilogramm.

Man muss sich nur einen einzigen Wert merken, dann ordnet sich alles ein:

| Energie | Was das ist |
|---|---|
| 0,025 eV | die Wärme in diesem Raum, pro Teilchen |
| 1,8 – 3,1 eV | sichtbares Licht, von Rot bis Violett |
| 4 eV | UV-Strahlung, die Sonnenbrand macht |
| 9,8 eV | die Dreifachbindung im Stickstoff, um die es im anderen Block geht |
| 13,6 eV | genug, um ein Wasserstoffatom komplett zu zerlegen |

Dein Elektron im Kasten hat gerade **{dez(E_n/EV, 3)} eV**. Das ist das
{dez(E_n/EV/EV_ZIMMER, 0)}-fache der Zimmerwärme.

Und für die, die aus der Chemie kommen: 1 eV entspricht 96,5 kJ/mol.
"""
        )

    st.divider()
    st.subheader("Was ist die Quantenzahl n?")
    st.markdown(
        """
**n ist einfach eine Hausnummer.** Sie zählt durch, um welche der erlaubten
Wellen es sich handelt.

- n = 1 → die einfachste mögliche Welle, ein Bauch. Der ruhigste Zustand.
- n = 2 → zwei Bäuche, mehr Zappeln, mehr Energie.
- n = 3 → drei Bäuche. Und so weiter.

n ist immer eine **ganze Zahl**. Es gibt kein n = 1,5.
"""
    )
    st.info(
        "**Merksatz für die Runde:** Eine Quantenzahl ist keine Messgröße, "
        "sondern eine Abzählung. Sie sagt nicht *wie viel*, sondern *welcher*."
    )

    st.subheader("Und was ist diese „Welle“ überhaupt?")
    st.markdown(
        """
**Es ist keine Welle aus irgendeinem Stoff.** Das Elektron wackelt nicht auf
und ab wie ein Seil.

Diese Welle heißt **Wellenfunktion**, geschrieben ψ (griechisch „psi“).
Sie ist eine Rechengröße. Ihre Bedeutung ist:

> Wo die Welle groß ist, findest du das Teilchen wahrscheinlich.
> Wo sie null ist, findest du es nie.

Das ist die eigentliche Zumutung der Theorie, und darum geht es in Kapitel 5.
"""
    )
    st.markdown(
        "**Probier es aus:** Zieh die Kastenbreite kleiner. Was passiert mit "
        "der Energie? Warum wohl? (Antwort in Kapitel 3.)"
    )


# ==================================================================
def _k3():
    kapitel_kopf(3, N_KAP, "Die Energieleiter",
                 "Eine Treppe ohne Rampe.")
    st.markdown(
        """
Jede erlaubte Welle gehört zu einer bestimmten Energie. Da es nur bestimmte
Wellen gibt, gibt es auch **nur bestimmte Energien**.
"""
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
            "warum die Quantenmechanik im Kleinen alles bestimmt und im Großen "
            "nicht auffällt."
        ),
    )

    st.divider()
    L_nm = st.slider("Kastenbreite L [Nanometer]", 0.2, 3.0, 1.0, 0.1, key="l3")
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

    ev_karten(energie(n_sel, L) / EV,
              f"Der markierte Zustand n = {n_sel} im Vergleich")

    st.markdown(
        """
**Das ist eine Treppe ohne Rampe.** Zwischen den Stufen ist nichts. Nicht
„schwer erreichbar“, sondern schlicht nicht existent. Das Teilchen kann diese
Energien haben und keine anderen.

Genau dieses Wort, dass Energie in Stufen kommt statt fließend, ist der Grund
für den Namen: **Quant** heißt auf Lateinisch „wie viel“, ein Quantum ist eine
abgezählte Portion.
"""
    )

    st.divider()
    st.subheader("Zwei Dinge, die man sofort sieht")
    st.markdown(
        """
**Erstens: Die Stufen werden nach oben immer weiter auseinander.**
Die Energie wächst mit n². Von n = 1 auf n = 2 vervierfacht sie sich, von
n = 1 auf n = 3 verneunfacht sie sich.

**Zweitens: Enger Kasten = größere Abstände.** Zieh den Breiten-Regler klein
und schau, wie die Leiter auseinanderzieht.
"""
    )
    st.warning(
        "**Das ist der Satz, auf den es ankommt:**\n\n"
        "Je enger du ein Teilchen einsperrst, desto heftiger wehrt es sich. "
        "Ein eingesperrtes Teilchen kann nicht einfach stillstehen, es hat "
        "immer eine Mindestenergie, die sogenannte Nullpunktsenergie.\n\n"
        "Und genau deshalb stürzen Elektronen nicht in den Atomkern. "
        "Ein Elektron im Kern wäre extrem eng eingesperrt und bräuchte dafür "
        "absurd viel Energie. Die hat es nicht. Also bleibt es draußen."
    )


# ==================================================================
def _k4():
    kapitel_kopf(4, N_KAP, "Farbe aus dem Sprung",
                 "Hier wird die Theorie zum ersten Mal sichtbar.")
    st.markdown(
        """
Wenn ein Teilchen von einer Stufe auf eine tiefere fällt, muss die
Energiedifferenz irgendwo hin. Sie wird als **Lichtteilchen** (Photon)
abgegeben.

Und die Energie des Photons bestimmt seine **Farbe**. Große Differenz = blau,
kleine Differenz = rot.
"""
    )
    merksatz("Aus der Treppe wird Licht, das man messen kann. "
             "So prüft man diese ganze Theorie überhaupt nach.")

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
    farbe = wellenlaenge_zu_farbe(wl_nm)

    m1, m2 = st.columns(2)
    m1.metric("Freigesetzte Energie", f"{dez(dE / EV, 2)} eV")
    m2.metric("Wellenlänge", f"{dez(wl_nm, 0)} nm")

    fig, ax = plt.subplots(figsize=(7, 1.2))
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=farbe))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.tight_layout()
    zeige(fig)

    if 380 <= wl_nm <= 750:
        st.success(f"Sichtbares Licht bei {wl_nm:.0f} nm.")
    elif wl_nm < 380:
        st.info(f"{wl_nm:.0f} nm – Ultraviolett, für dein Auge unsichtbar.")
    else:
        st.info(f"{wl_nm:.0f} nm – Infrarot, spürbar als Wärme.")

    st.caption(
        "Das graue Feld heißt nicht „keine Farbe“, sondern „außerhalb dessen, "
        "was dein Auge aufnimmt“. Die Strahlung ist da, du siehst sie nur nicht."
    )

    st.divider()
    st.subheader("Warum das kein Spielzeug ist")
    st.markdown(
        """
Spiel mit dem Breiten-Regler und beobachte, wie sich die Farbe ändert.

Winzige Kristalle von wenigen Nanometern Größe heißen Quantenpunkte. Ihre
Farbe hängt nicht von ihrem Material ab, sondern von ihrer **Größe**, genau
nach dem Prinzip, das du hier gerade verstellst.

Kleiner Punkt → enger Kasten → größere Sprünge → blaueres Licht.

In QLED-Fernsehern steckt genau das. Die Kastenbreite, an der du gerade
drehst, ist dort eine Fertigungstoleranz in der Produktion.
"""
    )

    st.divider()
    st.subheader("Und der Bogen zurück zum Dünger")
    st.markdown(
        """
Dieselbe Formel, die hier aus einem Energieunterschied eine Farbe macht,
beantwortet auch eine Frage aus dem anderen Block.

Die Dreifachbindung im Stickstoff entspricht **9,8 eV**. Ein Lichtteilchen mit
dieser Energie hätte eine Wellenlänge von **127 Nanometern** – tiefes
Ultraviolett, das die Atmosphäre vollständig wegfiltert.
"""
    )
    st.info(
        "**Deshalb düngt Sonnenlicht nicht.** Es ist nicht zu schwach im "
        "Sinne von zu wenig, sondern die einzelnen Portionen sind zu klein. "
        "Tausend rote Photonen ersetzen kein ultraviolettes. Das ist "
        "derselbe Gedanke wie bei der Treppe ohne Rampe."
    )
    st.info(
        "**Für den Diskursraum:** Zwischen Schrödingers Gleichung (1926) und "
        "dem Fernseher im Wohnzimmer liegen rund 90 Jahre. Bei Haber-Bosch "
        "lagen zwischen Laborreaktion und Weltproduktion keine zehn. "
        "Warum eigentlich so unterschiedlich?"
    )


# ==================================================================
def _k5():
    kapitel_kopf(5, N_KAP, "Wo ist das Teilchen?",
                 "Ab hier wird es unangenehm.")
    st.markdown(
        """
Bis jetzt klang alles noch harmlos – Wellen, Stufen, Licht. Jetzt kommt der
Bruch mit dem alten Weltbild.

**Frage: Wo genau ist das Elektron im Kasten?**

Antwort der klassischen Physik: An einem bestimmten Ort. Wir wissen ihn
vielleicht nicht, aber es gibt ihn.

Antwort der Quantenmechanik: **Die Frage hat keine Antwort.** Es gibt keinen
Ort, an dem es ist. Es gibt nur die Wahrscheinlichkeit, es irgendwo zu finden,
wenn man nachschaut.
"""
    )

    c1, c2 = st.columns(2)
    with c1:
        n = st.slider("Quantenzahl n", 1, 6, 2, key="n5")
    with c2:
        modus = st.radio("Ansicht", ["Welle (ψ)", "Wahrscheinlichkeit (ψ²)"],
                         horizontal=True)

    zeige(plot_zustand(
        n, 1.0, "wahrscheinlichkeit" if "Wahrsch" in modus else "welle"))

    if n >= 2 and "Wahrsch" in modus:
        st.warning(
            f"**Schau dir die Nullstellen an.** Bei n = {n} gibt es {n-1} "
            f"{'Stelle' if n == 2 else 'Stellen'} im Kasten, an denen das "
            "Teilchen **nie** gefunden wird.\n\n"
            "Wie kommt das Teilchen von links nach rechts, wenn es in der "
            "Mitte niemals sein kann?\n\n"
            "Die Antwort ist nicht „es springt darüber“. Die Antwort ist, dass "
            "die Frage eine falsche Vorstellung enthält, nämlich die, dass das "
            "Teilchen eine Bahn hat, auf der es entlangläuft. Hat es aber nicht."
        )

    st.divider()
    st.markdown(
        """
### Was hier wirklich passiert ist

Die Quantenmechanik nimmt einen Begriff aus dem Weltbild heraus, den vorher
niemand für verhandelbar gehalten hätte: **dass Dinge einen Ort haben.**

Das ist keine Messungenauigkeit. Es ist keine Frage besserer Geräte. Nach
allem, was wir wissen, hat das Elektron zwischen zwei Messungen schlicht keinen
definierten Ort.

Einstein hat das bis zu seinem Tod nicht akzeptiert. Sein berühmter Einwand,
Gott würfle nicht, war kein Scherz, sondern ein ernst gemeinter Protest gegen
genau diesen Punkt. Die Experimente haben ihm später unrecht gegeben.
"""
    )
    st.info(
        "**Die Transformation:** Hier verändert sich nicht das Wissen über die "
        "Welt, sondern die Vorstellung davon, welche Fragen überhaupt sinnvoll "
        "sind. Das ist eine andere Art von Umbruch als bei Haber-Bosch."
    )


# ==================================================================
def _k6():
    kapitel_kopf(6, N_KAP, "Warum merkst du davon nichts?",
                 "Die Gegenprobe mit dir selbst.")
    st.markdown(
        """
Berechtigter Einwand: Warum ist die Welt um dich herum dann so normal?

Machen wir die Probe. Wir sperren statt eines Elektrons **dich** in einen Raum.
Dieselbe Formel, andere Zahlen.
"""
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
0,00000001 Joule. Das ist etwa **{1e-8 / sprung:.0e} mal mehr** als dein
Quantensprung.

Deine Energiestufen sind also da. Sie sind nur so absurd eng beieinander, dass
keine Messung der Welt sie unterscheiden könnte. Die Treppe ist noch da,
aber die Stufen sind niedriger als die Rauheit des Materials.
"""
    )
    st.success(
        "**Das ist ein wichtiger Punkt gegen ein verbreitetes "
        "Missverständnis:**\n\n"
        "Die Quantenmechanik hat die klassische Physik nicht widerlegt. "
        "Sie hat sie **eingeordnet**. Newton ist nicht falsch, sondern ein "
        "Grenzfall für große, schwere Dinge. Und der stimmt dort so gut, dass "
        "wir bis heute Raumsonden damit steuern.\n\n"
        "Wissenschaftlicher Fortschritt heißt hier nicht: das Alte war Unsinn. "
        "Sondern: Wir wissen jetzt, wo seine Grenzen liegen."
    )
    merksatz(
        "Eine Transformation des Weltbilds bedeutet selten, dass alles "
        "Vorherige weg ist. Meistens wird das Alte zu einem <b>Spezialfall</b> "
        "des Neuen."
    )

    fachkasten(
        "Die Formel und ihre Grenzen",
        """
**Energie im Kasten:** *E<sub>n</sub>* = *n*² *h*² / (8 *m* *L*²)
mit *h* = 6,626 · 10⁻³⁴ J·s.

**Das Modell ist eine Idealisierung.** Es setzt unendlich hohe Wände
voraus, ein einziges Teilchen ohne Wechselwirkung, eine einzige
Raumrichtung und keine Relativität. Ein echtes Elektron in einem echten
Kristall sitzt in keinem solchen Kasten.

Trotzdem trifft das Modell die Größenordnung von Quantenpunkten, von
Farbstoffmolekülen mit langen konjugierten Ketten und von Elektronen in
dünnen Halbleiterschichten erstaunlich gut – überall dort, wo
„eingesperrt“ die wesentliche Eigenschaft ist.

**Für den Vergleich mit dem anderen Block:** 1 eV = 96,485 kJ/mol.
Ein Elektron im 1-nm-Kasten hat im Grundzustand 0,376 eV, also
36 kJ/mol – etwa ein Fünfundzwanzigstel der Stickstoff-Dreifachbindung.
""",
    )


# ==================================================================
def _k7():
    kapitel_kopf(7, N_KAP, "Diskussion",
                 "Vier Fragen für die interdisziplinäre Runde.")

    fragen = [
        ("Was passiert mit einem Weltbild, wenn es kippt?",
         "1898 hätte jeder Physiker gesagt: Energie ist eine kontinuierliche "
         "Größe, und Dinge haben einen Ort. Dreißig Jahre später war beides "
         "nicht mehr haltbar.\n\n"
         "Woher wollen wir wissen, dass unsere heutigen "
         "Selbstverständlichkeiten stabiler sind? Und was folgt daraus für "
         "Fächer, die keine Experimente machen können?"),
        ("Erkenntnis oder Anwendung, was transformiert eigentlich?",
         "Haber-Bosch veränderte binnen weniger Jahre, wie viele Menschen die "
         "Erde ernähren kann – und zugleich, wie Kriege geführt werden. Die "
         "Quantenmechanik veränderte zunächst nur, wie wir die Welt denken.\n\n"
         "Ist eine Erkenntnis, die nichts verändert, weniger transformativ? "
         "Oder mehr, weil sie tiefer sitzt?"),
        ("Wer trägt Verantwortung für die Folgen?",
         "Schrödinger und Bohr haben keine Fernseher, keine Solarzellen und "
         "keine Atombomben gebaut. Ihre Gleichungen stehen aber hinter allen "
         "dreien.\n\n"
         "Endet Verantwortung an der Labortür? Und falls nicht, wie weit "
         "reicht sie, wenn zwischen Erkenntnis und Anwendung Jahrzehnte "
         "liegen?"),
        ("Was heißt Verstehen, wenn Anschauung versagt?",
         "Wir haben heute Bilder benutzt: Saiten, Kästen, Treppen. Alle sind "
         "streng genommen falsch. Richtig ist nur die Mathematik.\n\n"
         "Ist das ein Problem? Kann man etwas verstehen, das man sich nicht "
         "vorstellen kann? Und gibt es das in euren Fächern auch?"),
    ]

    for titel, text in fragen:
        with st.expander(titel):
            st.write(text)
