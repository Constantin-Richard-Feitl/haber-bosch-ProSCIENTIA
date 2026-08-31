# -*- coding: utf-8 -*-
"""
Vom Dünger zur Quantenwelt
Arbeitskreis Pro Scientia – wie Wissenschaft unser Weltbild transformiert

Eine App, zwei Blöcke, ein Link.

Start lokal:
    python -m streamlit run app.py

Braucht streamlit, numpy und matplotlib (siehe requirements.txt). Die
Quantenchemie in hf_pure.py läuft mit reinem numpy – kein Compiler, keine
Chemiebibliothek.
"""

import streamlit as st

import bausteine as b
import block_haber_bosch as hb
import block_quantenwelt as qw

st.set_page_config(page_title="Vom Dünger zur Quantenwelt", page_icon="🌱",
                   layout="centered")
b.stil_setzen()

BLOECKE = {
    "Start": None,
    "Block 1 · Dünger aus Luft": hb,
    "Block 2 · Die Quantenwelt": qw,
    "Nachschlagen": None,
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

st.sidebar.caption("Kein Vorwissen nötig. Alle Fachwörter stehen unter "
                   "*Nachschlagen*.")


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
Zwei Umbrüche der Naturwissenschaft, die auf ganz verschiedene Weise
transformativ waren – und beide zum Anfassen.

**Haber-Bosch** veränderte die Welt, bevor irgendjemand verstanden hatte,
warum es funktioniert: vier Jahre vom Labor in die Fabrik, die Erklärung kam
fast hundert Jahre später hinterher.

**Die Quantenmechanik** veränderte zuerst nur, wie wir denken. Sie brauchte
Jahrzehnte, bis daraus Technik wurde – und heute rechnet sie auf einem
Laptop Moleküle durch, die niemand gemessen hat.
"""
    )

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
#### Block 1 · Dünger aus Luft
**Warum die Luft voller Dünger ist und trotzdem niemand herankommt.**

Du schätzt, wie fest eine chemische Bindung hält, findest heraus, warum Hitze
allein nicht reicht, und baust am Ende deinen eigenen Ammoniakreaktor.

*Vier Kapitel.*
"""
        )
    with c2:
        st.markdown(
            """
#### Block 2 · Die Quantenwelt
**Ein Teilchen in einem Kasten, und warum daran alles hängt.**

Von der Gitarrensaite zur Energieleiter, von der Energieleiter zur Farbe
deines Fernsehers – und zum Schluss rechnest du selbst ein Molekül durch.

*Fünf Kapitel.*
"""
        )

    st.divider()
    st.markdown(
        """
### Wie das hier funktioniert

**Links in der Leiste** wählst du Block und Kapitel. Auf dem Handy ist sie
eingeklappt – tipp oben links auf das Pfeil-Symbol **»**.

**Erst raten, dann auflösen.** An einigen Stellen wirst du gebeten zu tippen,
bevor etwas aufgelöst wird. Das ist kein Test, und niemand sieht dein
Ergebnis. Es funktioniert nur besser so.

**Keine Zahl steht allein.** Neben jeder Zahl steht ein Vergleich, ein Bild
oder ein Balken. Wer die nackten Werte, Formeln und Vorbehalte sehen will,
findet sie in den Kästen mit dem 🔬-Symbol.

**Nichts geht kaputt.** Alle Regler lassen sich beliebig verstellen, ein
Neuladen der Seite setzt alles zurück.
"""
    )

    st.caption(
        "Arbeitskreis „Vom Dünger zur Quantenwelt – wie Wissenschaft unser "
        "Weltbild transformiert“ · Constantin Richard Feitl & Dato Tsomaia"
    )


# ==================================================================
# Nachschlagen
# ==================================================================
GLOSSAR = [
    ("Mol",
     "Eine Stückzahl, so wie Dutzend – nur größer. Ein Mol sind rund "
     "600 000 000 000 000 000 000 000 Teilchen. In der Chemie wird in dieser "
     "Packungsgröße gerechnet, weil einzelne Moleküle zu klein zum Wiegen "
     "sind."),
    ("kJ/mol",
     "Energie pro Mol, also pro Standardpackung Moleküle. Der einzige "
     "Vergleichswert, den man dazu braucht: Die Umgebungswärme liefert bei "
     "20 °C rund 2,4 kJ/mol. Alles darüber ist viel."),
    ("eV (Elektronenvolt)",
     "Dieselbe Idee, aber pro einzelnem Teilchen statt pro Mol. Praktisch, "
     "wenn man über Elektronen und Licht spricht. 1 eV = 96,5 kJ/mol; "
     "sichtbares Licht liegt bei 1,8 bis 3,1 eV."),
    ("Bindungsenergie",
     "Der Aufwand, um eine chemische Bindung zu zerreißen. Je größer, desto "
     "stabiler das Molekül. N≡N liegt mit 945 kJ/mol ganz oben."),
    ("Aktivierungsenergie",
     "Die Hürde auf dem Weg zur Reaktion – nicht das Ziel, sondern der Berg "
     "davor. Auch eine Reaktion, die insgesamt Energie freisetzt, kommt ohne "
     "genug Anlauf nicht in Gang."),
    ("Katalysator",
     "Ein Stoff, der eine Reaktion beschleunigt, ohne selbst verbraucht zu "
     "werden. Er liefert keine Energie, sondern bietet einen Weg an, auf dem "
     "die Hürde niedriger ist."),
    ("Chemisches Gleichgewicht",
     "Der Zustand, in dem Hin- und Rückreaktion gleich schnell laufen und "
     "sich die Mengen nicht mehr ändern. Er sagt, wie viel am Ende "
     "herauskommt – nicht, wie lange es dauert."),
    ("Wellenfunktion ψ",
     "Kein Stoff, der wackelt, sondern eine Rechengröße. Wo ihr Quadrat groß "
     "ist, findet man das Teilchen wahrscheinlich; wo es null ist, nie."),
    ("Quantenzahl n",
     "Eine Hausnummer, keine Messgröße. Sie zählt durch, welcher der "
     "erlaubten Zustände gemeint ist. Immer eine ganze Zahl."),
    ("Nullpunktsenergie",
     "Die Mindestenergie eines eingesperrten Teilchens. Ein Elektron kann "
     "nicht stillstehen – deshalb stürzt es nicht in den Atomkern."),
    ("Ångström",
     "Ein Zehnmilliardstel Meter, also 0,1 Nanometer. Ungefähr die Größe "
     "eines Atoms; Bindungslängen liegen bei ein bis zwei Ångström."),
    ("Hartree-Fock",
     "Ein Rechenverfahren, das jedes Elektron nur den Durchschnitt aller "
     "anderen spüren lässt. Schnell und ehrlich grob – man weiß genau, was "
     "weggelassen wurde."),
]

QUELLEN = """
**Chemie und Verfahren**

* Larson, A. T. & Dodge, R. L. (1923/24): Gleichgewichtsmessungen zur
  Ammoniaksynthese. Das Modell dieser App ist gegen diese klassische Tabelle
  angepasst.
* *Green ammonia synthesis*, Editorial, **Nature Synthesis** 2 (2023).
  Quelle für 1–2 % des Weltenergiebedarfs und für die 48 % der
  Weltbevölkerung, die von synthetisch gedüngter Nahrung leben.
  <https://www.nature.com/articles/s44160-023-00362-y>
* Ertl, G.: Nobelpreis für Chemie 2007 für die Aufklärung chemischer Vorgänge
  auf Oberflächen, am Beispiel der Ammoniaksynthese.

**Quantenmechanik und Quantenchemie**

* Schrödinger, E. (1926): *Quantisierung als Eigenwertproblem.* Annalen der
  Physik 79.
* `hf_pure.py` ist eine eigenständige Hartree-Fock-Implementierung in reinem
  numpy: STO-3G-Basissatz nach Hehre, Stewart & Pople (1969),
  Gauß-Integrale über das McMurchie-Davidson-Schema.
* Spektroskopische Vergleichswerte (Bindungslängen und Taltiefen
  *D*<sub>e</sub>) nach Huber & Herzberg, *Constants of Diatomic Molecules*.

Alle Rechenergebnisse dieser App entstehen im Moment des Knopfdrucks.
"""


def nachschlagen():
    st.title("Nachschlagen")
    tab1, tab2 = st.tabs(["Fachwörter", "Quellen"])
    with tab1:
        st.caption("Jedes Fachwort der App in einem Satz. Anklicken zum "
                   "Aufklappen.")
        for wort, erklaerung in GLOSSAR:
            with st.expander(wort):
                st.write(erklaerung)
    with tab2:
        st.markdown(QUELLEN, unsafe_allow_html=True)
        st.caption(
            "Die App rechnet mit vereinfachten Modellen. Wo eine "
            "Vereinfachung das Ergebnis merklich verschiebt, steht das im "
            "🔬-Kasten des jeweiligen Kapitels."
        )


# ==================================================================
# Seite ausliefern
# ==================================================================
if block == "Start":
    startseite()
elif block == "Nachschlagen":
    nachschlagen()
else:
    modul.zeichne(kapitel)

st.sidebar.caption("Constantin Richard Feitl & Dato Tsomaia · Pro Scientia")
