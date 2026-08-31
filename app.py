# -*- coding: utf-8 -*-
"""
Vom Dünger zur Quantenwelt
Arbeitskreis Pro Scientia – wie Wissenschaft unser Weltbild transformiert

Eine App, zwei Blöcke, ein Link.

Start lokal:
    python -m streamlit run app.py

Braucht: streamlit, numpy, matplotlib (siehe requirements.txt).
Die Quantenchemie in hf_pure.py läuft mit reinem numpy, es ist also
kein Compiler und keine Chemiebibliothek nötig.
"""

import streamlit as st

import bausteine as b
import block_haber_bosch as hb
import block_quantenwelt as qw

st.set_page_config(
    page_title="Vom Dünger zur Quantenwelt",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="auto",
)
b.stil_setzen()

BLOECKE = {
    "Start": None,
    "Block 1 · Haber-Bosch": hb,
    "Block 2 · Quantenwelt": qw,
    "Werkzeugkasten": None,
}


# ==================================================================
# Navigation
# ==================================================================
st.sidebar.title("Vom Dünger zur Quantenwelt")
st.sidebar.caption("Arbeitskreis Pro Scientia")

block = st.sidebar.radio("Block", list(BLOECKE.keys()),
                         label_visibility="collapsed")
st.sidebar.divider()

modul = BLOECKE[block]
kapitel = None
if modul is not None:
    kapitel = st.sidebar.radio("Kapitel", modul.KAPITEL,
                               label_visibility="collapsed")
    st.sidebar.divider()

if b.codefelder_aktiv():
    st.sidebar.markdown(
        "**Zum Mitrechnen:** In manchen Kapiteln steht ein Codefeld. "
        "Du darfst Zahlen ändern und auf *Ausführen* drücken. "
        "Kaputtmachen kannst du nichts, *Zurücksetzen* holt jederzeit das "
        "Original zurück."
    )
st.sidebar.caption(
    "Kein Vorwissen nötig. Alle Fachwörter stehen im Werkzeugkasten."
)


# ==================================================================
# Startseite
# ==================================================================
def startseite():
    st.title("Vom Dünger zur Quantenwelt")
    st.markdown(
        "<div style='font-size:1.2rem;color:#555;margin-top:-0.7rem;"
        "margin-bottom:1.4rem'>Wie Wissenschaft unser Weltbild "
        "transformiert</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
Was passiert, wenn wissenschaftliche Entdeckungen nicht nur unser Wissen
erweitern, sondern unser gesamtes Weltbild verändern?

Diese App ist der Mitmachteil des Arbeitskreises. Sie ersetzt keinen Vortrag
und verlangt kein Vorwissen – **kein Chemieunterricht, keine Formeln, keine
Programmierkenntnisse.** Alles, was du brauchst, sind Regler, Knöpfe und
Neugier.
"""
    )

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
#### Block 1 · Haber-Bosch
**Warum die Luft voller Dünger ist und trotzdem niemand herankommt.**

Du schätzt, wie fest eine chemische Bindung hält, findest heraus, warum Hitze
allein nicht reicht, baust deinen eigenen Ammoniakreaktor und rechnest zum
Schluss ein Molekül durch, ohne es je zu messen.

*Sechs Kapitel, etwa 30 Minuten.*
"""
        )
    with c2:
        st.markdown(
            """
#### Block 2 · Quantenwelt
**Ein Teilchen in einem Kasten, und warum daran alles hängt.**

Von der Gitarrensaite zur Energieleiter, von der Energieleiter zur Farbe
deines Fernsehers – und zu der Frage, ob ein Elektron überhaupt irgendwo ist.

*Acht Kapitel, etwa 30 Minuten.*
"""
        )

    st.divider()
    st.markdown(
        """
### Wie das hier funktioniert

**Links in der Leiste** wählst du den Block und das Kapitel. Auf dem Handy
ist sie eingeklappt – tipp oben links auf das Pfeil-Symbol **»**, dann
klappt sie auf.

**Ratefragen zuerst.** An mehreren Stellen wirst du gebeten zu tippen, bevor
etwas aufgelöst wird. Das ist kein Test, und niemand sieht dein Ergebnis. Es
funktioniert nur besser so: Wer sich vorher festlegt, merkt sich die Auflösung.

**Fachzahlen sind weggeräumt.** Neben jeder Zahl steht ein Vergleich, ein Bild
oder ein Balken. Wer die nackten Werte, Formeln und Quellen sehen will, findet
sie in den Kästen mit dem 🔬-Symbol.

**Nichts geht kaputt.** Alle Regler und Codefelder lassen sich beliebig
verstellen. Ein Neuladen der Seite setzt alles zurück.
"""
    )

    st.divider()
    st.markdown(
        """
### Der rote Faden

Zwei Umbrüche, die auf ganz verschiedene Weise transformativ waren.

**Haber-Bosch** veränderte die Welt, bevor irgendjemand verstanden hatte,
warum es funktioniert. Vier Jahre vom Labor in die Fabrik, und die Erklärung
kam fast hundert Jahre später hinterher.

**Die Quantenmechanik** veränderte zuerst nur, wie wir denken. Sie nahm dem
Weltbild eine Selbstverständlichkeit weg, die niemand für verhandelbar
gehalten hatte, und brauchte Jahrzehnte, bis daraus Technik wurde.

Beide Blöcke enden in einer Diskussionsrunde. Die Fragen dort sind das
eigentliche Ziel des Nachmittags – der Rest ist Anlauf.
"""
    )

    st.caption(
        "Arbeitskreis „Vom Dünger zur Quantenwelt – wie Wissenschaft unser "
        "Weltbild transformiert“ · Constantin Richard Feitl & Dato Tsomaia"
    )


# ==================================================================
# Werkzeugkasten
# ==================================================================
GLOSSAR = [
    ("Mol",
     "Eine Stückzahl, so wie Dutzend – nur größer. Ein Mol sind rund "
     "600 000 000 000 000 000 000 000 Teilchen. Chemikerinnen rechnen "
     "in dieser Packungsgröße, weil einzelne Moleküle zu klein zum Wiegen "
     "sind."),
    ("kJ/mol",
     "Energie pro Mol, also pro Standardpackung Moleküle. Der einzige "
     "Vergleichswert, den man dazu braucht: Die Wärme in einem Zimmer "
     "liefert rund 2,4 kJ/mol. Alles darüber ist viel."),
    ("eV (Elektronenvolt)",
     "Dieselbe Idee, aber pro einzelnem Teilchen statt pro Mol. Praktisch, "
     "wenn man über Elektronen und Licht spricht. 1 eV = 96,5 kJ/mol. "
     "Sichtbares Licht liegt bei 1,8 bis 3,1 eV."),
    ("Hartree",
     "Die Hausnummer-Einheit der Quantenchemie, die Energie, die im "
     "Wasserstoffatom natürlich vorkommt. 1 Hartree = 2625,5 kJ/mol. "
     "Taucht in dieser App nur in den Rohausgaben auf."),
    ("Bindungsenergie",
     "Der Aufwand, um eine chemische Bindung zu zerreißen. Je größer, desto "
     "stabiler das Molekül. N≡N liegt mit 945 kJ/mol ganz oben."),
    ("Aktivierungsenergie",
     "Die Hürde auf dem Weg zur Reaktion – nicht das Ziel, sondern der Berg "
     "davor. Auch eine Reaktion, die insgesamt Energie freisetzt, kommt ohne "
     "genug Anlauf nicht in Gang."),
    ("Katalysator",
     "Ein Stoff, der eine Reaktion beschleunigt, ohne selbst verbraucht zu "
     "werden. Er liefert keine Energie. Er bietet einen Weg an, auf dem die "
     "Hürde niedriger ist."),
    ("Chemisches Gleichgewicht",
     "Der Zustand, in dem Hin- und Rückreaktion gleich schnell laufen und "
     "sich die Mengen nicht mehr ändern. Er sagt, wie viel am Ende "
     "herauskommt – nicht, wie lange es dauert."),
    ("Bar",
     "Eine Druckeinheit. Ein bar ist ungefähr der normale Luftdruck; ein "
     "Autoreifen hat gut zwei. Im Ammoniakreaktor sind es 200."),
    ("Hartree-Fock",
     "Ein Rechenverfahren, das jedes Elektron nur den Durchschnitt aller "
     "anderen spüren lässt. Schnell und ehrlich grob – man weiß genau, was "
     "weggelassen wurde."),
    ("Basissatz (STO-3G)",
     "Der Baukasten aus mathematischen Grundformen, aus dem das Programm "
     "Elektronenwolken zusammensetzt. STO-3G ist der kleinste gebräuchliche "
     "und entsprechend grob."),
    ("Wellenfunktion ψ",
     "Kein Stoff, der wackelt, sondern eine Rechengröße. Wo sie groß ist, "
     "findet man das Teilchen wahrscheinlich; wo sie null ist, nie."),
    ("Quantenzahl n",
     "Eine Hausnummer, keine Messgröße. Sie zählt durch, welcher der "
     "erlaubten Zustände gemeint ist. Immer eine ganze Zahl."),
    ("Nullpunktsenergie",
     "Die Mindestenergie eines eingesperrten Teilchens. Ein Elektron kann "
     "nicht stillstehen. Deshalb stürzt es nicht in den Atomkern."),
    ("Ångström",
     "Ein Zehnmilliardstel Meter, also 0,1 Nanometer. Ungefähr die Größe "
     "eines Atoms. Bindungslängen liegen bei ein bis zwei Ångström."),
]

QUELLEN = """
**Chemie und Verfahren**

* Larson, A. T. & Dodge, R. L. (1923/24): Gleichgewichtsmessungen zur
  Ammoniaksynthese. Das Modell in dieser App ist gegen diese klassische
  Tabelle angepasst.
* *Green ammonia synthesis*, Editorial, **Nature Synthesis** 2 (2023).
  Quelle für 170 Mio. t Jahresproduktion, 1–2 % des Weltenergiebedarfs,
  3–5 % des Erdgasverbrauchs und 48 % der Weltbevölkerung, die von
  synthetisch gedüngter Nahrung lebt.
  <https://www.nature.com/articles/s44160-023-00362-y>
* Ertl, G.: Nobelpreis für Chemie 2007 für die Aufklärung chemischer
  Vorgänge auf Oberflächen, am Beispiel der Ammoniaksynthese.
* Scheinbare Aktivierungsenergien technischer Eisenkatalysatoren werden
  in der Literatur mit 80 bis über 200 kJ/mol angegeben, je nach
  Katalysator und Bedingungen. Die App rechnet mit 100 kJ/mol als
  rundem Mittelwert.

**Geschichte und Ethik**

* Szöllösi-Janze, M. (1998): *Fritz Haber 1868–1934. Eine Biographie.*
  München: Beck. Belegstellen im Text.
* Smil, V. (2001): *Enriching the Earth.* MIT Press. Standardwerk zur
  Wirkung des Verfahrens auf die Weltbevölkerung.
* Jonas, H. (1979): *Das Prinzip Verantwortung.*

**Quantenchemie**

* Die Datei `hf_pure.py` ist eine eigenständige Hartree-Fock-Implementierung
  in reinem numpy: STO-3G-Basissatz nach Hehre, Stewart & Pople (1969),
  Gauß-Integrale über das McMurchie-Davidson-Schema.
* Alle in der App gezeigten Rechenergebnisse entstehen im Moment des
  Knopfdrucks. Nur die N₂-Kurve liegt vorberechnet in `vorberechnet.json`,
  weil sie live etwa eine Minute bräuchte.
"""


def werkzeugkasten():
    st.title("Werkzeugkasten")
    st.caption("Zum Nachschlagen, Übersetzen und Weiterlesen.")

    tab1, tab2, tab3 = st.tabs(["Einheiten-Übersetzer", "Glossar", "Quellen"])

    with tab1:
        st.markdown(
            """
Hier kannst du jede Energie, die in der App vorkommt, in etwas übersetzen,
das man sich vorstellen kann. Trag einen Wert ein und wähle, in welcher
Einheit er gemeint ist.
"""
        )
        c1, c2 = st.columns([2, 1])
        with c1:
            wert = st.number_input("Wert", value=945.0, step=1.0,
                                   format="%g")
        with c2:
            einheit = st.selectbox(
                "Einheit", ["kJ/mol", "eV", "kcal/mol", "Hartree"])

        umrechnung = {
            "kJ/mol": 1.0,
            "eV": b.EV_IN_KJ_MOL,
            "kcal/mol": 4.184,
            "Hartree": b.HARTREE_KJ,
        }
        kJ = wert * umrechnung[einheit]

        st.divider()
        u1, u2, u3, u4 = st.columns(4)
        u1.metric("kJ/mol", b.dez(kJ, 1))
        u2.metric("eV", b.dez(kJ / b.EV_IN_KJ_MOL, 4))
        u3.metric("kcal/mol", b.dez(kJ / 4.184, 1))
        u4.metric("Hartree", b.dez(kJ / b.HARTREE_KJ, 5))

        if kJ > 0:
            st.divider()
            b.energie_karten(kJ, "Und im Alltag heißt das")
            a = b.alltag(kJ)
            st.divider()
            st.markdown("##### Zwei Einordnungen, die weiterhelfen")
            v1, v2 = st.columns(2)
            v1.metric("Verglichen mit der Zimmerwärme",
                      f"{b.dez(a['portionen'], 0)} ×",
                      help="Wie oft die thermische Energie bei 20 °C "
                           "(2,4 kJ/mol) in diesen Wert passt.")
            v2.metric("Als Licht wäre das",
                      f"{b.dez(a['wellenlaenge_nm'], 0)} nm",
                      help="Wellenlänge eines Lichtteilchens mit genau "
                           "dieser Energie. Sichtbar ist 380–750 nm.")
            st.caption(b.ev_einordnung(kJ / b.EV_IN_KJ_MOL))

        st.info(
            "**Ein paar Werte zum Ausprobieren:** 945 (Dreifachbindung im "
            "Stickstoff) · 436 (Wasserstoff) · 2,4 (Wärme in diesem Raum) · "
            "92 (was die Haber-Bosch-Reaktion freisetzt) · "
            "0,376 in eV (Elektron im Nanometer-Kasten)."
        )

    with tab2:
        st.markdown(
            "Jedes Fachwort, das in der App vorkommt, in einem Satz erklärt. "
            "Anklicken zum Aufklappen."
        )
        for wort, erklaerung in GLOSSAR:
            with st.expander(wort):
                st.write(erklaerung)

    with tab3:
        st.markdown(QUELLEN, unsafe_allow_html=True)
        st.divider()
        st.caption(
            "Die App rechnet mit vereinfachten Modellen. Wo eine Vereinfachung "
            "das Ergebnis merklich verschiebt, steht das im jeweiligen "
            "🔬-Kasten des Kapitels."
        )


# ==================================================================
# Seite ausliefern
# ==================================================================
if block == "Start":
    startseite()
elif block == "Werkzeugkasten":
    werkzeugkasten()
else:
    modul.zeichne(kapitel)

st.sidebar.caption(
    "Constantin Richard Feitl & Dato Tsomaia · Pro Scientia"
)
