# -*- coding: utf-8 -*-
"""
Erzeugt vorberechnet.json neu.

Die N2-Bindungskurve braucht rund eine Minute, weil jeder einzelne Punkt
eine vollständige Hartree-Fock-Rechnung ist. Deshalb liegt sie fertig
neben der App, statt live gerechnet zu werden.

    python vorberechnen.py
"""

import json
import os
import time

import numpy as np

import hf_pure

HARTREE_KJ = 2625.499639

NH3_GEOMETRIE = [
    ("N", (0.000000, 0.000000, 0.116489)),
    ("H", (0.000000, 0.939731, -0.271808)),
    ("H", (0.813831, -0.469865, -0.271808)),
    ("H", (-0.813831, -0.469865, -0.271808)),
]


def main():
    t0 = time.time()

    rs_h2 = [round(float(x), 3) for x in np.arange(0.40, 2.61, 0.06)]
    es_h2 = [hf_pure.energie([("H", (0, 0, 0)), ("H", (0, 0, r))])
             for r in rs_h2]
    print(f"H2-Kurve fertig ({time.time()-t0:.1f} s)")

    rs_n2 = [round(float(x), 3) for x in np.arange(0.85, 2.31, 0.05)]
    es_n2 = [hf_pure.energie([("N", (0, 0, 0)), ("N", (0, 0, r))])
             for r in rs_n2]
    print(f"N2-Kurve fertig ({time.time()-t0:.1f} s)")

    d = dict(
        rs_h2=rs_h2, es_h2=es_h2, rs_n2=rs_n2, es_n2=es_n2,
        E_H_atom=hf_pure.energie([("H", (0, 0, 0))], spin=1),
        E_N_atom=hf_pure.energie([("N", (0, 0, 0))], spin=3),
        E_H2=hf_pure.energie([("H", (0, 0, 0)), ("H", (0, 0, 0.74))]),
        E_N2=hf_pure.energie([("N", (0, 0, 0)), ("N", (0, 0, 1.10))]),
        E_NH3=hf_pure.energie(NH3_GEOMETRIE),
    )

    i, j = int(np.argmin(es_h2)), int(np.argmin(es_n2))
    d["r_min_h2"] = rs_h2[i]
    d["r_min_n2"] = rs_n2[j]
    d["D_HH"] = (2 * d["E_H_atom"] - es_h2[i]) * HARTREE_KJ
    d["D_NN"] = (2 * d["E_N_atom"] - es_n2[j]) * HARTREE_KJ
    d["dE_reaktion"] = (2 * d["E_NH3"]
                        - (d["E_N2"] + 3 * d["E_H2"])) * HARTREE_KJ

    ziel = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "vorberechnet.json")
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1)

    print()
    print(f"H2: Minimum {d['r_min_h2']} A (gemessen 0,741), "
          f"Bindung {d['D_HH']:.0f} kJ/mol (gemessen 436)")
    print(f"N2: Minimum {d['r_min_n2']} A (gemessen 1,098), "
          f"Bindung {d['D_NN']:.0f} kJ/mol (gemessen 945)")
    print(f"Reaktionsenergie {d['dE_reaktion']:+.0f} kJ/mol (gemessen -92)")
    print(f"\nGeschrieben nach {ziel} ({time.time()-t0:.1f} s)")


if __name__ == "__main__":
    main()
