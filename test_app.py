# -*- coding: utf-8 -*-
"""
Selbsttest der App. Klickt jedes Kapitel und die wichtigen Knöpfe durch
und meldet jede Exception. Aufruf:

    python test_app.py
"""
import sys
import time

from streamlit.testing.v1 import AppTest

import block_haber_bosch as hb
import block_quantenwelt as qw

FEHLER = []


def pruefe(name, at):
    if at.exception:
        for e in at.exception:
            FEHLER.append(f"{name}: {e.message}")
        print(f"  FEHLER  {name}")
    else:
        print(f"  ok      {name}")


def seite(block, kapitel=None, timeout=300):
    at = AppTest.from_file("app.py", default_timeout=timeout).run()
    at.sidebar.radio[0].set_value(block).run()
    if kapitel is not None:
        at.sidebar.radio[1].set_value(kapitel).run()
    return at


print("== Alle Kapitel rendern ==")
for blockname, modul in [("Block 1 · Haber-Bosch", hb),
                         ("Block 2 · Quantenwelt", qw)]:
    for kap in modul.KAPITEL:
        t0 = time.time()
        at = seite(blockname, kap)
        pruefe(f"{blockname} / {kap}  ({time.time()-t0:.1f}s)", at)

for einzel in ["Start", "Werkzeugkasten"]:
    pruefe(einzel, seite(einzel))

print("\n== Ratefragen aufloesen ==")
at = seite("Block 1 · Haber-Bosch", hb.KAPITEL[1])
at.button(key="loesen_n2_vs_h2").click().run()
pruefe("K1 Schaetzfrage aufgeloest", at)

at = seite("Block 2 · Quantenwelt", qw.KAPITEL[3])
at.button(key="loesen_kasten_halb").click().run()
pruefe("QM K3 Schaetzfrage aufgeloest", at)

print("\n== Regler bewegen ==")
at = seite("Block 1 · Haber-Bosch", hb.KAPITEL[1])
for temp in [20, 500, 1500, 3000]:
    at.slider(key="t_boltzmann").set_value(temp).run()
    pruefe(f"K1 Boltzmann bei {temp} Grad", at)

at = seite("Block 1 · Haber-Bosch", hb.KAPITEL[2])
for T, P in [(250, 10), (300, 50), (450, 200), (620, 400), (400, 300)]:
    at.slider(key="t_spiel").set_value(T).run()
    at.slider(key="p_spiel").set_value(P).run()
    pruefe(f"K2 Reaktor {T} Grad / {P} bar", at)
at.slider(key="barriere").set_value(100).run()
pruefe("K2 Barriere 100", at)
at.slider(key="barriere").set_value(50).run()
at.slider(key="t_kat").set_value(20).run()
pruefe("K2 Barriere 50 bei 20 Grad", at)

at = seite("Block 2 · Quantenwelt", qw.KAPITEL[4])
at.slider(key="l4").set_value(2.0).run()
pruefe("QM K4 grosser Kasten (Infrarot)", at)
at.slider(key="l4").set_value(0.4).run()
pruefe("QM K4 kleiner Kasten (UV)", at)

print("\n== Quantenchemie wirklich rechnen (dauert) ==")
at = seite("Block 1 · Haber-Bosch", hb.KAPITEL[3], timeout=900)
at.button(key="btn_h2").click().run()
pruefe("K3 H2-Kurve live gerechnet", at)
at.radio(key="vz_tipp").set_value("Die Reaktion setzt Energie frei").run()
pruefe("K3 Vorzeichen-Tipp gesetzt", at)
at.button(key="btn_hb").click().run()
pruefe("K3 Reaktionsenergie live gerechnet (richtiger Tipp)", at)
at.radio(key="vz_tipp").set_value("Die Reaktion braucht Energie").run()
pruefe("K3 Reaktionsenergie mit falschem Tipp", at)
at.button(key="btn_n2").click().run()
pruefe("K3 N2-Kurve angezeigt", at)

print("\n== Codefelder ausfuehren ==")
for blockname, kap, key in [("Block 1 · Haber-Bosch", hb.KAPITEL[0], "luft"),
                            ("Block 1 · Haber-Bosch", hb.KAPITEL[4],
                             "menschen")]:
    at = seite(blockname, kap, timeout=600)
    at.button(key=f"run_{key}").click().run()
    pruefe(f"Codefeld {key} ausgefuehrt", at)

print("\n== Werkzeugkasten-Uebersetzer ==")
at = seite("Werkzeugkasten")
for wert in [945.0, 0.0, 2.4]:
    at.number_input[0].set_value(wert).run()
    pruefe(f"Uebersetzer mit {wert}", at)

print()
if FEHLER:
    print(f"{len(FEHLER)} FEHLER:")
    for f in FEHLER:
        print(" -", f)
    sys.exit(1)
print("Alles sauber.")
