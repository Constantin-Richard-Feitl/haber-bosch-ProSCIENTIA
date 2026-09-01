# -*- coding: utf-8 -*-
"""
Gemeinsame Bausteine für beide Blöcke.

Eine Regel trägt die ganze App:
Keine Fachzahl steht allein. Neben jeder Zahl steht ein Vergleich, ein
Balken oder ein Bild. Die nackten Werte und die Vorbehalte liegen in
ausklappbaren Kästen für die, die sie sehen wollen.
"""

import io
import os
import math
import hashlib
import contextlib
import traceback

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ==================================================================
# Farben
# ==================================================================
BLAU = "#1b6ca8"
ORANGE = "#d95f02"
GRUEN = "#2a9d5c"
ROT = "#c0392b"
GRAU = "#c9c9c9"
DUNKELGRAU = "#555555"

# ==================================================================
# Naturkonstanten
# ==================================================================
R_GAS = 8.314462618          # J/(mol*K)
N_A = 6.02214076e23          # 1/mol
H_PLANCK = 6.62607015e-34    # J*s
C_LICHT = 299792458.0        # m/s
M_E = 9.1093837015e-31       # kg
EV = 1.602176634e-19         # J
EV_IN_KJ_MOL = 96.48533212   # 1 eV entspricht 96,485 kJ/mol
HARTREE_KJ = 2625.499639     # 1 Hartree in kJ/mol

# Thermische Energie bei 20 Grad: als kJ/mol (Chemie) und als eV (Physik).
# Das ist der Maßstab, an dem in dieser App jede Energie gemessen wird.
KJ_ZIMMER = R_GAS * 293.15 / 1000.0        # 2,44 kJ/mol
EV_ZIMMER = KJ_ZIMMER / EV_IN_KJ_MOL       # 0,0253 eV


# ==================================================================
# Darstellung
# ==================================================================
HOCH = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def hoch(n):
    """10 hoch n als lesbarer Text: hoch(168) -> '10¹⁶⁸'."""
    return "10" + str(int(n)).translate(HOCH)


def dez(zahl, stellen=1):
    """Deutsche Schreibweise: dez(2.8) -> '2,8', dez(12345.6, 0) -> '12.346'."""
    text = f"{zahl:,.{stellen}f}"
    return text.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def stil_setzen():
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#999999",
        "axes.labelcolor": "#333333",
        "axes.labelsize": 10,
        "xtick.color": "#555555",
        "ytick.color": "#555555",
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "font.size": 10,
        "legend.frameon": False,
        "figure.autolayout": True,
    })


def neue_figur(hoehe=3.2, breite=7.0):
    fig, ax = plt.subplots(figsize=(breite, hoehe))
    ax.spines[["top", "right"]].set_visible(False)
    return fig, ax


def zeige(fig):
    st.pyplot(fig)
    plt.close(fig)


def kapitel_kopf(nummer, gesamt, titel, unterzeile=None):
    st.caption(f"Kapitel {nummer} von {gesamt}")
    st.title(titel)
    if unterzeile:
        st.markdown(
            f"<div style='color:#666;font-size:1.06rem;margin-top:-0.6rem;"
            f"margin-bottom:1.2rem'>{unterzeile}</div>",
            unsafe_allow_html=True,
        )


def merksatz(text):
    """Ein Satz, der hängen bleiben soll."""
    st.markdown(
        f"<div style='border-left:4px solid {ORANGE};background:#fff8f2;"
        f"padding:0.85rem 1.1rem;margin:1.1rem 0;border-radius:4px;"
        f"font-size:1.02rem'>{text}</div>",
        unsafe_allow_html=True,
    )


def fachkasten(titel, inhalt):
    """Hier und nur hier stehen die nackten Zahlen und die Vorbehalte."""
    with st.expander(f"🔬 {titel}"):
        st.markdown(inhalt)


# ==================================================================
# Energie übersetzen
# ==================================================================
def wellenlaenge_nm(kJ_pro_mol):
    """Wellenlänge eines Lichtteilchens mit genau dieser Energie."""
    if kJ_pro_mol <= 0:
        return float("inf")
    e_pro_teilchen = kJ_pro_mol * 1000.0 / N_A
    return H_PLANCK * C_LICHT / e_pro_teilchen * 1e9


# Bänder statt Einzelwerte, damit die Einordnung nie danebengreift.
EV_BAENDER = [
    (0.05, "weniger als die Wärme, die in diesem Raum ohnehin herumfliegt"),
    (1.6, "Infrarot, also Wärmestrahlung unterhalb dessen, was dein "
          "Auge noch sieht"),
    (2.0, "rotes Licht"),
    (2.6, "grünes bis gelbes Licht"),
    (3.1, "blaues bis violettes Licht"),
    (5.0, "Ultraviolett, die Strahlung, die Sonnenbrand macht"),
    (10.0, "energiereiches Ultraviolett; in dieser Gegend liegt auch die "
           "Dreifachbindung im Stickstoff mit 9,8 eV"),
    (float("inf"),
     "genug, um Atome auseinanderzureißen. Ein Wasserstoffatom braucht "
     "dafür 13,6 eV"),
]


def ev_einordnung(E_eV):
    """Ordnet eine Energie in eV in etwas Anschauliches ein."""
    if E_eV <= 0:
        return "Keine Energie, also auch nichts zu vergleichen."
    band = next(t for grenze, t in EV_BAENDER if E_eV < grenze)
    v = E_eV / EV_ZIMMER
    if 0.75 < v < 1.35:
        rel = "**ungefähr genau so viel**"
    elif v >= 1:
        rel = f"das **{dez(v, 0)}-fache**"
    else:
        rel = f"**{dez(1 / v, 1)}-mal weniger**"
    return (f"Das ist {band}. Gegenüber der Wärme bei Zimmertemperatur "
            f"ist es {rel}.")


# ==================================================================
# Wie selten ist selten?
# ==================================================================
def boltzmann_anteil(Ea_kJ_pro_mol, T_celsius):
    """Boltzmann-Faktor exp(-Ea/RT).

    Der Anteil der Zusammenstöße, die genug Energie mitbringen, um eine
    Hürde der Höhe Ea zu nehmen. Eine Abschätzung der Größenordnung,
    keine Reaktionsgeschwindigkeit. Für die Frage "passiert das
    überhaupt" reicht sie vollkommen.
    """
    T = T_celsius + 273.15
    exponent = -Ea_kJ_pro_mol * 1000.0 / (R_GAS * T)
    if exponent < -700:
        return 10.0 ** (exponent / math.log(10))   # verhindert Unterlauf
    return math.exp(exponent)


# Zehnerpotenzen, an denen man große Zahlen festmachen kann.
LEITER = [
    (4, "Zuschauer in einer großen Konzerthalle"),
    (7, "Einwohner Österreichs"),
    (10, "Menschen auf der Erde"),
    (19, "Sandkörner an allen Stränden der Welt"),
    (22, "Moleküle in einem Liter Luft"),
    (44, "Moleküle in der gesamten Erdatmosphäre"),
    (50, "Atome, aus denen die Erde besteht"),
    (57, "Atome in der Sonne"),
    (80, "Atome im gesamten sichtbaren Universum"),
]


def seltenheit_anzeigen(anteil, kontext=""):
    """Zeigt einen winzigen Anteil als 'eines von 10^x' mit Vergleich."""
    if anteil <= 0 or math.isnan(anteil):
        n = 400
    else:
        n = -math.log10(anteil)

    if n < 1:
        st.metric("Anteil der Moleküle mit genug Energie",
                  f"{anteil*100:.0f} von 100")
        st.success("Das ist keine Seltenheit mehr. Die Reaktion läuft.")
        return

    st.markdown(
        f"<div style='font-size:2.1rem;line-height:1.25;font-weight:600;"
        f"color:{BLAU}'>eines von {hoch(round(n))}</div>"
        f"<div style='color:#666;margin-bottom:0.6rem'>Molekülen hat genug "
        f"Energie{kontext}</div>",
        unsafe_allow_html=True,
    )

    if n > 80:
        st.error(
            f"**Für {hoch(round(n))} gibt es keinen Vergleich mehr.** Im "
            f"gesamten sichtbaren Universum gibt es rund {hoch(80)} Atome. "
            "Selbst das ist gegen diese Zahl verschwindend klein.\n\n"
            "Praktisch heißt das nicht *selten*. Es heißt *nie*."
        )
    else:
        stufe = min(LEITER, key=lambda e: abs(e[0] - n))
        st.info(f"Zum Vergleich: **{hoch(stufe[0])}** ist ungefähr die "
                f"Anzahl {stufe[1]}.")


# ==================================================================
# Balkenvergleich
# ==================================================================
def balken_vergleich(paare, hervorheben=None,
                     xlabel="Aufwand, um die Bindung zu brechen  [kJ/mol]"):
    """Waagrechte Balken. paare: Liste (Name, Wert)."""
    namen = [p[0] for p in paare]
    werte = [p[1] for p in paare]
    farben = [ORANGE if n == hervorheben else BLAU for n in namen]

    fig, ax = plt.subplots(figsize=(7, 0.52 * len(paare) + 1.0))
    y = np.arange(len(paare))
    ax.barh(y, werte, color=farben, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(namen)
    ax.invert_yaxis()
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    spanne = max(werte) if werte else 1
    for yi, w in zip(y, werte):
        ax.text(w + spanne * 0.015, yi, f"{w:.0f}", va="center",
                fontsize=9, color=DUNKELGRAU)
    ax.set_xlim(0, spanne * 1.16)
    ax.set_xlabel(xlabel)
    fig.tight_layout()
    return fig


# ==================================================================
# Erst raten, dann auflösen
# ==================================================================
def schaetzfrage(key, frage, minimum, maximum, start, schritt, echt,
                 einheit="", format_str="%.1f", aufloesung_text=None,
                 toleranz_gut=None):
    """Erst tippen lassen, dann auflösen. Wer sich festlegt, hört anders zu."""
    st.markdown(f"**{frage}**")
    tipp = st.slider("Dein Tipp", minimum, maximum, start, schritt,
                     key=f"tipp_{key}", format=format_str,
                     label_visibility="collapsed")

    if not st.button("Auflösen", key=f"loesen_{key}"):
        st.caption("Erst tippen, dann auflösen.")
        return tipp, False

    daneben = abs(tipp - echt)
    if toleranz_gut is None:
        toleranz_gut = 0.15 * abs(echt)
    nk = int(format_str[2]) if len(format_str) > 2 and \
        format_str[2].isdigit() else 1

    c1, c2 = st.columns(2)
    c1.metric("Dein Tipp", f"{dez(tipp, nk)} {einheit}".strip())
    c2.metric("Tatsächlich", f"{dez(echt, nk)} {einheit}".strip(),
              delta=f"{'+' if tipp >= echt else '−'}{dez(daneben, nk)} daneben",
              delta_color="off")

    if daneben <= toleranz_gut:
        st.success("Guter Instinkt. Das war nah dran.")
    elif daneben <= 3 * toleranz_gut:
        st.info("Richtige Größenordnung, aber daneben.")
    else:
        st.warning("Deutlich daneben. Genau darum geht es hier.")

    if aufloesung_text:
        st.markdown(aufloesung_text)
    return tipp, True


# ==================================================================
# Codefeld zum Selbstrechnen
# ==================================================================
def codefelder_aktiv():
    """Codefelder lassen sich für den öffentlichen Link abschalten.

    In Streamlit Cloud unter Settings -> Secrets:  CODEFELDER = false
    """
    wert = os.environ.get("CODEFELDER")
    if wert is None:
        try:
            wert = st.secrets.get("CODEFELDER", None)
        except Exception:
            wert = None
    if wert is None:
        return True
    return str(wert).strip().lower() not in ("0", "false", "nein", "off")


def code_feld(key, code, hinweis=None, hoehe=320, extras=None,
              titel="Selbst rechnen"):
    """Editierbares Codefeld mit Ausführen-Knopf und Ausgabe."""
    if not codefelder_aktiv():
        return

    st.markdown(f"##### {titel}")
    if hinweis:
        st.caption(hinweis)

    # Der Zustand des Textfelds liegt unter seinem eigenen Schlüssel. Sobald
    # der gesetzt ist, ignoriert Streamlit ein übergebenes value. Deshalb
    # wird beim Zurücksetzen dieser Schlüssel selbst überschrieben, und zwar
    # vor dem Erzeugen des Widgets. Nachher wäre es ein Fehler.
    #
    # Im Schlüssel steckt zusätzlich eine Prüfsumme der Vorlage. Ändert sich
    # die Vorlage im Quelltext, entsteht ein neuer Schlüssel und die laufende
    # Sitzung zeigt sofort die neue Fassung, statt an der alten zu kleben.
    kennung = hashlib.md5(code.encode("utf-8")).hexdigest()[:8]
    feld = f"area_{key}_{kennung}"
    if st.session_state.pop(f"neuladen_{key}", False) or feld not in st.session_state:
        st.session_state[feld] = code

    eingabe = st.text_area(
        "Python-Code, du darfst alles ändern",
        height=hoehe,
        key=feld,
        label_visibility="collapsed",
    )

    c1, c2, _ = st.columns([1.1, 1.1, 2])
    los = c1.button("▶ Ausführen", key=f"run_{key}", type="primary",
                    use_container_width=True)
    if c2.button("Zurücksetzen", key=f"reset_{key}", use_container_width=True):
        st.session_state[f"neuladen_{key}"] = True
        st.rerun()

    if not los:
        return

    puffer = io.StringIO()
    umgebung = {"np": np, "numpy": np, "plt": plt, "math": math}
    if extras:
        umgebung.update(extras)
    try:
        with contextlib.redirect_stdout(puffer):
            exec(eingabe, umgebung)   # noqa: S102, bewusst, siehe README
        ausgabe = puffer.getvalue()
        if ausgabe.strip():
            st.code(ausgabe, language=None)
        else:
            st.info("Kein `print()` im Code, deshalb keine Ausgabe.")
        fig = plt.gcf()
        if fig.get_axes():
            st.pyplot(fig)
        plt.close("all")
    except Exception:
        zeilen = traceback.format_exc().splitlines()
        st.error("Da ist etwas schiefgegangen. Das ist normal. Einfach "
                 "ändern und nochmal.")
        st.code(zeilen[-1], language=None)
