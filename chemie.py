# -*- coding: utf-8 -*-
"""
Das Rechenmodell hinter dem Reaktor-Kapitel.

Zwei Fragen, die im Haber-Bosch-Verfahren gegeneinander arbeiten:

  1. Wie viel Ammoniak wäre am Ende drin, wenn man ewig wartet?
     -> Gleichgewicht, hängt an Temperatur und Druck.
  2. Wie lange dauert dieses "ewig"?
     -> Geschwindigkeit, hängt an Temperatur und Katalysator.

Kalte Bedingungen gewinnen Frage 1 und verlieren Frage 2. Genau dieser
Konflikt ist der Grund, warum die Anlage bei 450 °C und 200 bar läuft
und nicht bei Zimmertemperatur. Das Kapitel lässt die Teilnehmenden
diesen Konflikt selbst finden.
"""

import math

R_GAS = 8.314462618

# Standardwerte für N2 + 3 H2 -> 2 NH3, bezogen auf 298,15 K
DELTA_H_0 = -91800.0     # J/mol Formelumsatz
DELTA_S_0 = -198.1       # J/(mol*K)
DELTA_CP = -45.3         # J/(mol*K), grobe Temperaturkorrektur

# Empirischer Realgas-Zuschlag. Ohne ihn liegt das ideale Modell bei
# hohen Drücken systematisch etwa 15 % zu niedrig. Der Wert 0.00199
# wurde gegen die klassische Gleichgewichtstabelle von Larson & Dodge
# (1923/24) angepasst und trifft sie über den ganzen Bereich von
# 10 bis 600 bar und 200 bis 600 °C auf etwa einen Prozentpunkt genau.
FUGAZITAET_A = 0.00199

# Der reale Betriebspunkt heutiger Anlagen
BETRIEB_T = 450.0     # °C
BETRIEB_P = 200.0     # bar

# Aktivierungsbarrieren in kJ/mol
BARRIERE_OHNE = 945.0     # blanke Gasphase: die Dreifachbindung selbst
BARRIERE_EISEN = 100.0    # Eisenkatalysator, gemessene Größenordnung


def gleichgewichtskonstante(T_celsius):
    """Kp in bar^-2 für N2 + 3 H2 -> 2 NH3."""
    T = T_celsius + 273.15
    dH = DELTA_H_0 + DELTA_CP * (T - 298.15)
    dS = DELTA_S_0 + DELTA_CP * math.log(T / 298.15)
    dG = dH - T * dS
    return math.exp(-dG / (R_GAS * T))


def nh3_ausbeute(T_celsius, P_bar):
    """Ammoniakgehalt im Gleichgewicht in Molprozent.

    Ausgangsgemisch stöchiometrisch, also ein Teil N2 auf drei Teile H2.
    """
    K = gleichgewichtskonstante(T_celsius) * math.exp(FUGAZITAET_A * P_bar)
    ziel = K * P_bar ** 2

    def ueberschuss(x):
        gesamt = 4 - 2 * x
        x_n2 = (1 - x) / gesamt
        x_h2 = 3 * (1 - x) / gesamt
        x_nh3 = 2 * x / gesamt
        return x_nh3 ** 2 / (x_n2 * x_h2 ** 3) - ziel

    lo, hi = 1e-12, 1 - 1e-12
    for _ in range(120):
        mitte = 0.5 * (lo + hi)
        if ueberschuss(mitte) < 0:
            lo = mitte
        else:
            hi = mitte
    x = 0.5 * (lo + hi)
    return 2 * x / (4 - 2 * x) * 100.0


def relative_geschwindigkeit(T_celsius, Ea_kJ=BARRIERE_EISEN,
                             bezug_celsius=BETRIEB_T):
    """Reaktionsgeschwindigkeit relativ zum Betriebspunkt (dort = 1).

    Reine Arrhenius-Abschätzung. Sie sagt nichts über absolute
    Durchsätze, aber sie zeigt richtig, wie brutal die Temperatur
    auf die Geschwindigkeit durchschlägt.
    """
    T = T_celsius + 273.15
    T0 = bezug_celsius + 273.15
    exponent = -Ea_kJ * 1000.0 / R_GAS * (1.0 / T - 1.0 / T0)
    exponent = max(min(exponent, 700.0), -700.0)
    return math.exp(exponent)


_HOCH = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def _lesbar(zahl):
    """Große Zahl mit Punkt als Tausendertrennung, wie im Deutschen."""
    return f"{zahl:,.0f}".replace(",", ".")


def _komma(zahl, stellen=1):
    """Deutsche Schreibweise mit Komma als Dezimaltrenner."""
    return f"{zahl:.{stellen}f}".replace(".", ",")


def _potenz(zahl):
    """Sehr große Zahl als lesbare Zehnerpotenz, z.B. '2 · 10¹⁰'."""
    e = int(math.floor(math.log10(zahl)))
    m = zahl / 10 ** e
    return f"{m:.0f} · 10{str(e).translate(_HOCH)}"


def reaktor_check(T_celsius, P_bar):
    """Was in einer echten Anlage bei diesen Bedingungen schiefginge.

    Gibt eine Liste (art, text) zurück; art ist 'fehler', 'warnung'
    oder 'ok'.
    """
    meldungen = []

    if T_celsius < 350:
        faktor = 1.0 / max(relative_geschwindigkeit(T_celsius), 1e-300)
        if faktor > 1e6:
            meldungen.append((
                "fehler",
                f"**Zu kalt.** Die Ausbeute wäre traumhaft, nur arbeitet der "
                f"Katalysator rund {_potenz(faktor)}-mal langsamer als im "
                f"Betriebspunkt. Auf dein Ammoniak würdest du länger warten, "
                f"als es die Menschheit gibt."))
        else:
            meldungen.append((
                "warnung",
                f"**Kalt.** Die Ausbeute stimmt. Die Anlage ist dafür rund "
                f"{_lesbar(faktor)}-mal langsamer als üblich – rechne in "
                f"Monaten statt in Minuten."))
    elif T_celsius > 550:
        meldungen.append((
            "fehler",
            "**Zu heiß.** Schnell ist die Reaktion hier, nur bleibt kaum "
            "Ammoniak übrig – und der Eisenkatalysator versintert, seine "
            "Oberfläche verklumpt und er verliert dauerhaft an Wirkung."))
    elif T_celsius > 500:
        meldungen.append((
            "warnung",
            "**Grenzwertig heiß.** Läuft, kostet aber Ausbeute und "
            "Katalysatorlebensdauer."))

    if P_bar > 350:
        meldungen.append((
            "fehler",
            "**Zu viel Druck.** Für die Ausbeute wunderbar. Nur muss ein "
            "Stahlrohr das aushalten, und heißer Wasserstoff greift Stahl "
            "von innen an. Genau daran ist Bosch fast gescheitert."))
    elif P_bar > 250:
        meldungen.append((
            "warnung",
            "**Sehr hoher Druck.** Technisch machbar, aber teuer: dickere "
            "Wände, mehr Kompressorarbeit, größeres Risiko."))
    elif P_bar < 20:
        meldungen.append((
            "warnung",
            "**Kaum Druck.** Ohne Druck verschiebt sich das Gleichgewicht "
            "nicht auf die Ammoniakseite. Da kommt fast nichts heraus."))

    if not meldungen:
        meldungen.append((
            "ok",
            "**Das läuft.** Deine Bedingungen liegen in dem Fenster, in dem "
            "echte Anlagen arbeiten."))
    return meldungen


# Die drei Bedingungen, die eine Anlage gleichzeitig erfüllen muss.
# Das Fenster, das dabei herauskommt, ist ungefähr das, in dem echte
# Anlagen tatsächlich stehen: rund 400 bis 550 °C und 100 bis 350 bar.
MIN_AUSBEUTE = 15.0      # Molprozent NH3 im Gleichgewicht
MIN_TEMPO = 0.2          # relativ zum Betriebspunkt


def bewertung(T_celsius, P_bar):
    """Prüft die drei Bedingungen einer funktionierenden Anlage.

    Gibt (geschafft, [(name, erfuellt, text), ...]) zurück.
    """
    a = nh3_ausbeute(T_celsius, P_bar)
    v = relative_geschwindigkeit(T_celsius)
    hart = any(art == "fehler" for art, _ in reaktor_check(T_celsius, P_bar))

    pruefungen = [
        ("Genug Ausbeute", a >= MIN_AUSBEUTE,
         f"{_komma(a)} % Ammoniak im Gleichgewicht "
         f"(nötig: mindestens {MIN_AUSBEUTE:.0f} %)"),
        ("Schnell genug", v >= MIN_TEMPO,
         f"{_komma(v, 2)}-fache Geschwindigkeit des Betriebspunkts "
         f"(nötig: mindestens {_komma(MIN_TEMPO, 1)})"),
        ("Anlage hält das aus", not hart,
         "Material, Katalysator und Druckbehälter machen mit"
         if not hart else "Etwas in der Anlage geht kaputt"),
    ]
    return all(p[1] for p in pruefungen), pruefungen
