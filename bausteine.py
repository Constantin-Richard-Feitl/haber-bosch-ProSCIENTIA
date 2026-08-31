# -*- coding: utf-8 -*-
"""
Gemeinsame Bausteine für beide Blöcke.

Hier liegt vor allem das, was das Projekt didaktisch trägt:
Übersetzungen von Fachzahlen in Alltagsgrößen, die Zehnerpotenz-Leiter
und das editierbare Codefeld.

Grundregel für die ganze App:
Keine Fachzahl steht allein. Neben jeder Zahl steht entweder ein
Vergleich, ein Bild oder ein Balken. Die Fachzahl selbst wandert in
einen ausklappbaren Kasten für die, die sie sehen wollen.
"""

import io
import os
import math
import contextlib
import traceback

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ==================================================================
# Farben und Grundstil
# ==================================================================
BLAU = "#1b6ca8"
ORANGE = "#d95f02"
GRUEN = "#2a9d5c"
ROT = "#c0392b"
GRAU = "#c9c9c9"
DUNKELGRAU = "#555555"

# ==================================================================
# Naturkonstanten und Umrechnungen
# ==================================================================
R_GAS = 8.314462618          # J/(mol*K)
N_A = 6.02214076e23          # 1/mol
H_PLANCK = 6.62607015e-34    # J*s
C_LICHT = 299792458.0        # m/s
M_E = 9.1093837015e-31       # kg
EV = 1.602176634e-19         # J
EV_IN_KJ_MOL = 96.48533212   # 1 eV entspricht 96,485 kJ/mol
HARTREE_KJ = 2625.499639     # 1 Hartree in kJ/mol
HARTREE_EV = 27.211386       # 1 Hartree in eV
# Die thermische Energie bei 20 Grad, in eV. Der Bezugspunkt fuer alle
# Einordnungen im Block Quantenwelt.
EV_ZIMMER = 8.314462618 * 293.15 / 1000.0 / 96.48533212

# Alltagsanker, alle in Kilojoule
KJ_WASSER_LITER = 4.182 * 80     # 1 L Wasser von 20 auf 100 Grad erwärmen
KJ_HANDYAKKU = 69.3              # ein voller Handyakku (5000 mAh, 3,85 V)
KJ_KWH = 3600.0
KJ_SCHOKOTAFEL = 2200.0          # 100 g Vollmilchschokolade


# ==================================================================
# Darstellungshelfer
# ==================================================================
HOCH = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def hoch(n):
    """10 hoch n als lesbarer Text, z.B. hoch(168) -> '10¹⁶⁸'."""
    return "10" + str(int(n)).translate(HOCH)


def dez(zahl, stellen=1):
    """Zahl in deutscher Schreibweise: Komma als Dezimaltrenner.

    dez(2.8) -> '2,8'   dez(12345.6, 0) -> '12.346'
    """
    text = f"{zahl:,.{stellen}f}"
    return text.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def stil_setzen():
    """Einheitlicher, ruhiger Matplotlib-Stil für die ganze App."""
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
    """Plot anzeigen und danach aufräumen, damit nichts liegen bleibt."""
    st.pyplot(fig)
    plt.close(fig)


# ==================================================================
# Der Kern der Didaktik: Fachzahl -> Alltag
# ==================================================================
def waermeportion(T_celsius=20.0):
    """Thermische Energie R*T bei gegebener Temperatur, in kJ/mol.

    Das ist der wichtigste Maßstab der ganzen App: die Energieportion,
    die die Umgebungswärme einem Molekül im Schnitt mitgibt. Bei
    Zimmertemperatur sind das rund 2,4 kJ/mol. Jede Bindungsenergie
    wird an dieser Portion gemessen.
    """
    return R_GAS * (T_celsius + 273.15) / 1000.0


def alltag(kJ_pro_mol, stoff_g_pro_mol=None):
    """Übersetzt kJ/mol in Vergleiche, die man sich vorstellen kann.

    Gibt ein dict mit fertig formatierten Textbausteinen zurück.
    """
    E = float(kJ_pro_mol)
    a = {}
    a["portionen"] = E / waermeportion(20.0)
    a["ev"] = E / EV_IN_KJ_MOL
    a["wasser_liter"] = E / KJ_WASSER_LITER
    a["akkus"] = E / KJ_HANDYAKKU
    a["kwh"] = E / KJ_KWH
    a["schokolade"] = E / KJ_SCHOKOTAFEL
    a["hub_meter"] = E * 1000.0 / (75.0 * 9.81)   # 75-kg-Mensch anheben
    if E > 0:
        # Wellenlänge eines Lichtteilchens mit genau dieser Energie
        e_pro_teilchen = E * 1000.0 / N_A
        a["wellenlaenge_nm"] = H_PLANCK * C_LICHT / e_pro_teilchen * 1e9
    else:
        a["wellenlaenge_nm"] = float("inf")
    if stoff_g_pro_mol:
        a["mj_pro_kg"] = E / (stoff_g_pro_mol / 1000.0) / 1000.0
    return a


def energie_karten(kJ_pro_mol, titel="Was diese Energie im Alltag bedeutet"):
    """Drei Alltagsvergleiche als Kacheln. Für 1 mol des Stoffs."""
    a = alltag(kJ_pro_mol)
    st.markdown(f"##### {titel}")
    k1, k2, k3 = st.columns(3)
    k1.metric("Wasser kochen", f"{dez(a['wasser_liter'])} Liter",
              help="So viel Wasser könnte man mit dieser Energie von "
                   "20 auf 100 Grad erhitzen.")
    k2.metric("Handyakkus", f"{dez(a['akkus'], 0)} Stück",
              help="So viele volle Handyakkus stecken in dieser Energie.")
    k3.metric("Einen Menschen anheben", f"{dez(a['hub_meter']/1000)} km",
              help="So hoch könnte man einen 75 kg schweren Menschen "
                   "damit anheben.")
    st.caption(
        "Alle drei Angaben gelten für **ein Mol**, also für rund "
        "600 000 000 000 000 000 000 000 Moleküle. Chemikerinnen und "
        "Chemiker rechnen immer in dieser Packungsgröße."
    )


# ==================================================================
# Zehnerpotenz-Leiter: große Zahlen begreifbar machen
# ==================================================================
LEITER = [
    (2, "so viele Menschen, wie in diesem Raum sitzen"),
    (4, "Zuschauer in einer großen Konzerthalle"),
    (7, "Einwohner Österreichs"),
    (10, "Menschen auf der Erde"),
    (19, "Sandkörner an allen Stränden der Welt"),
    (22, "Moleküle in einem Liter Luft"),
    (25, "Moleküle in einem Glas Wasser"),
    (44, "Moleküle in der gesamten Erdatmosphäre"),
    (50, "Atome, aus denen die Erde besteht"),
    (57, "Atome in der Sonne"),
    (68, "Atome in der Milchstraße"),
    (80, "Atome im gesamten sichtbaren Universum"),
]


def leiter_vergleich(log10_zahl):
    """Findet den nächstgelegenen Alltagsvergleich für eine Zehnerpotenz."""
    n = log10_zahl
    if n > 80:
        return None
    passend = min(LEITER, key=lambda e: abs(e[0] - n))
    return passend


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
            f"**{hoch(round(n))} ist keine Zahl mehr, die irgendwo vorkommt.** "
            f"Im gesamten sichtbaren Universum gibt es etwa {hoch(80)} Atome. "
            "Man müsste dieses Universum vollständig mit Stickstoff füllen und "
            "das Ganze anschließend noch einmal mit sich selbst multiplizieren, "
            "um auch nur auf diese Stückzahl zu kommen.\n\n"
            "Anders gesagt: Es passiert nicht. Nicht selten, sondern nie."
        )
    else:
        stufe = leiter_vergleich(n)
        st.info(
            f"Zum Vergleich: **{hoch(stufe[0])}** ist ungefähr die Anzahl "
            f"{stufe[1]}."
        )


def boltzmann_anteil(Ea_kJ_pro_mol, T_celsius):
    """Anteil der Teilchen, deren Energie über der Schwelle Ea liegt.

    Das ist der Boltzmann-Faktor exp(-Ea/RT). Er ist eine Abschätzung
    der Größenordnung, keine exakte Reaktionsgeschwindigkeit. Für die
    Frage 'passiert das überhaupt' reicht er vollkommen.
    """
    T = T_celsius + 273.15
    exponent = -Ea_kJ_pro_mol * 1000.0 / (R_GAS * T)
    if exponent < -700:
        return 10.0 ** (exponent / math.log(10))   # verhindert Unterlauf
    return math.exp(exponent)


# ==================================================================
# Balkenvergleich für Bindungsenergien
# ==================================================================
def balken_vergleich(paare, einheit="kJ/mol", hervorheben=None,
                     xlabel="Aufwand, um die Bindung zu brechen",
                     zeige_zahlen=True):
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
    if zeige_zahlen:
        spanne = max(werte) if werte else 1
        for yi, w in zip(y, werte):
            ax.text(w + spanne * 0.015, yi, f"{w:.0f}", va="center",
                    fontsize=9, color=DUNKELGRAU)
        ax.set_xlim(0, spanne * 1.16)
    ax.set_xlabel(f"{xlabel}  [{einheit}]")
    fig.tight_layout()
    return fig


# ==================================================================
# Fachkasten: hier und nur hier stehen die nackten Zahlen
# ==================================================================
def fachkasten(titel, inhalt):
    """Ausklappbarer Kasten für Fachzahlen, Formeln und Vorbehalte."""
    with st.expander(f"🔬 {titel}"):
        st.markdown(inhalt)


# ==================================================================
# Codefeld zum Selbstrechnen
# ==================================================================
def codefelder_aktiv():
    """Codefelder lassen sich für den öffentlichen Link abschalten.

    In Streamlit Cloud unter Settings -> Secrets eintragen:
        CODEFELDER = false
    Siehe README, Abschnitt 'Ein Wort zur Sicherheit'.
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


def code_feld(key, code, hinweis=None, hoehe=260, extras=None,
              titel="Selbst ausprobieren"):
    """Editierbares Codefeld mit Ausführen-Knopf und Ausgabe."""
    if not codefelder_aktiv():
        return

    st.markdown(f"##### {titel}")
    if hinweis:
        st.caption(hinweis)

    speicher = f"code_{key}"
    if speicher not in st.session_state:
        st.session_state[speicher] = code

    eingabe = st.text_area(
        "Python-Code – du darfst alles ändern",
        value=st.session_state[speicher],
        height=hoehe,
        key=f"area_{key}",
        label_visibility="collapsed",
    )

    c1, c2, _ = st.columns([1.1, 1.1, 2])
    los = c1.button("▶ Ausführen", key=f"run_{key}", type="primary",
                    use_container_width=True)
    if c2.button("Zurücksetzen", key=f"reset_{key}", use_container_width=True):
        st.session_state[speicher] = code
        st.rerun()

    if not los:
        return

    puffer = io.StringIO()
    umgebung = {"np": np, "numpy": np, "plt": plt, "math": math}
    if extras:
        umgebung.update(extras)
    try:
        with contextlib.redirect_stdout(puffer):
            exec(eingabe, umgebung)   # noqa: S102 – bewusst, siehe README
        ausgabe = puffer.getvalue()
        if ausgabe.strip():
            st.code(ausgabe, language=None)
        else:
            st.info("Kein `print()` im Code – deshalb keine Ausgabe.")
        fig = plt.gcf()
        if fig.get_axes():
            st.pyplot(fig)
        plt.close("all")
    except Exception:
        zeilen = traceback.format_exc().splitlines()
        st.error("Da ist etwas schiefgegangen. Das ist normal, "
                 "einfach ändern und nochmal.")
        st.code(zeilen[-1], language=None)


# ==================================================================
# Kleine Wiederholungselemente
# ==================================================================
def schaetzfrage(key, frage, minimum, maximum, start, schritt, echt,
                 einheit="", format_str="%.1f", aufloesung_text=None,
                 toleranz_gut=None):
    """Erst raten lassen, dann auflösen. Gibt den geratenen Wert zurück.

    Das ist der wichtigste Interaktionsbaustein der App: Wer vorher rät,
    hört beim Auflösen anders zu.
    """
    st.markdown(f"**{frage}**")
    tipp = st.slider("Dein Tipp", minimum, maximum, start, schritt,
                     key=f"tipp_{key}", format=format_str,
                     label_visibility="collapsed")

    if not st.button("Auflösen", key=f"loesen_{key}"):
        st.caption("Erst tippen, dann auflösen. Ohne Tipp ist die Antwort "
                   "nur eine Zahl mehr.")
        return tipp, False

    abweichung = abs(tipp - echt)
    if toleranz_gut is None:
        toleranz_gut = 0.15 * abs(echt)

    nk = int(format_str[2]) if len(format_str) > 2 and \
        format_str[2].isdigit() else 1
    c1, c2 = st.columns(2)
    c1.metric("Dein Tipp", f"{dez(tipp, nk)} {einheit}".strip())
    c2.metric("Tatsächlich", f"{dez(echt, nk)} {einheit}".strip(),
              delta=f"{'+' if tipp >= echt else '−'}{dez(abs(tipp-echt), nk)} "
                    f"daneben", delta_color="off")

    if abweichung <= toleranz_gut:
        st.success("Guter Instinkt. Das war nah dran.")
    elif abweichung <= 3 * toleranz_gut:
        st.info("Richtige Größenordnung, aber daneben.")
    else:
        st.warning("Deutlich daneben – und genau darum geht es hier.")

    if aufloesung_text:
        st.markdown(aufloesung_text)
    return tipp, True


# Wofür ein Elektronenvolt im Alltag steht. Der Block Quantenwelt rechnet
# in eV; ohne diese Leiter ist die Einheit für die meisten nur ein Kürzel.
# Bänder statt Einzelwerte, damit die Einordnung nie danebengreift.
EV_BAENDER = [
    (0.05, "weniger als die Wärme, die in diesem Raum ohnehin herumfliegt"),
    (0.5, "Wärmestrahlung, wie sie ein Heizkörper abgibt – Infrarot"),
    (1.6, "nahes Infrarot, knapp unterhalb dessen, was dein Auge noch sieht"),
    (2.0, "rotes Licht"),
    (2.6, "grünes bis gelbes Licht"),
    (3.1, "blaues bis violettes Licht"),
    (5.0, "Ultraviolett – die Strahlung, die Sonnenbrand macht"),
    (10.0, "energiereiches Ultraviolett; in dieser Gegend liegt auch die "
           "Dreifachbindung im Stickstoff mit 9,8 eV"),
    (float("inf"),
     "genug, um Atome auseinanderzureißen – ein Wasserstoffatom "
     "braucht dafür 13,6 eV"),
]


def ev_einordnung(E_eV):
    """Ordnet eine Energie in eV in etwas Anschauliches ein."""
    if E_eV <= 0:
        return "Keine Energie, also auch nichts zu vergleichen."
    band = next(t for grenze, t in EV_BAENDER if E_eV < grenze)
    verhaeltnis = E_eV / EV_ZIMMER
    if 0.75 < verhaeltnis < 1.35:
        rel = "**ungefähr genau so viel**"
    elif verhaeltnis >= 1:
        rel = f"das **{dez(verhaeltnis, 0)}-fache**"
    else:
        rel = f"**{dez(1 / verhaeltnis, 1)}-mal weniger**"
    return (f"Das ist {band}. Gegenüber der Wärme bei Zimmertemperatur "
            f"ist es {rel}.")


def ev_karten(E_eV, titel="Wie viel ist das?"):
    """Zeigt eine eV-Energie zusammen mit Vergleichen."""
    st.markdown(f"##### {titel}")
    a = E_eV * EV_IN_KJ_MOL
    lam = H_PLANCK * C_LICHT / (E_eV * EV) * 1e9 if E_eV > 0 else float("inf")
    k1, k2, k3 = st.columns(3)
    k1.metric("Energie", f"{dez(E_eV, 3)} eV")
    k2.metric("In Chemikersprache", f"{dez(a, 0)} kJ/mol")
    k3.metric("Als Licht wäre das", f"{dez(lam, 0)} nm")
    st.caption(ev_einordnung(E_eV))


def merksatz(text):
    """Ein Satz, der hängen bleiben soll."""
    st.markdown(
        f"<div style='border-left:4px solid {ORANGE};background:#fff8f2;"
        f"padding:0.85rem 1.1rem;margin:1.1rem 0;border-radius:4px;"
        f"font-size:1.02rem'>{text}</div>",
        unsafe_allow_html=True,
    )


def kapitel_kopf(nummer, gesamt, titel, unterzeile=None):
    st.caption(f"Kapitel {nummer} von {gesamt}")
    st.title(titel)
    if unterzeile:
        st.markdown(
            f"<div style='color:#666;font-size:1.06rem;margin-top:-0.6rem;"
            f"margin-bottom:1.2rem'>{unterzeile}</div>",
            unsafe_allow_html=True,
        )
