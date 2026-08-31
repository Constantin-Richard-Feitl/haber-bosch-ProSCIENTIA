# Vom Dünger zur Quantenwelt

Interaktive Streamlit-App zum Arbeitskreis *„Vom Dünger zur Quantenwelt –
wie Wissenschaft unser Weltbild transformiert"* (Pro Scientia).

Eine App, zwei Blöcke, ein Link. Kein Vorwissen nötig.

---

## Was drin ist

| Seite | Kapitel | Worum es geht |
|---|---|---|
| **Start** | – | Einstieg und Bedienhinweise |
| **Block 1 · Dünger aus Luft** | 4 | Von der Luft über die Bindungsenergie und den Katalysator bis zum selbstgebauten Reaktor |
| **Block 2 · Die Quantenwelt** | 5 | Teilchen im Kasten, von der Gitarrensaite über den QLED-Fernseher bis zur live gerechneten Quantenchemie |
| **Nachschlagen** | – | Fachwörter und Quellen |

Die App ist der Mitmachteil des Arbeitskreises. Die Diskussion findet in der
Runde statt, nicht im Browser – deshalb enthält die App keine Diskussionsfragen.

### Die drei Regeln, nach denen sie gebaut ist

1. **Keine Zahl steht allein.** Neben jeder Zahl steht ein Vergleich, ein Bild
   oder ein Balken. Die nackten Werte, Formeln und Vorbehalte liegen in den
   ausklappbaren 🔬-Kästen.
2. **Ein einziger Maßstab.** Statt kJ/mol zu erklären, wird alles an einer
   Größe gemessen: der Energie, die die Umgebungswärme einem Molekül bei 20 °C
   mitgibt (2,4 kJ/mol). Die Dreifachbindung im Stickstoff ist das 388-fache
   davon – das reicht als Verständnis für das ganze Kapitel.
3. **Erst raten, dann auflösen.** An mehreren Stellen legen sich die
   Teilnehmenden zuerst fest. Wer geschätzt hat, hört bei der Auflösung anders
   zu.

---

## Lokal starten

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Öffnet sich unter <http://localhost:8501>.

---

## Auf Streamlit Community Cloud stellen

Ergebnis ist eine öffentliche Adresse wie `https://euer-name.streamlit.app`.

### 1 · Repository anlegen

Auf <https://github.com> ein **neues, öffentliches** Repository anlegen
(z. B. `duenger-quantenwelt`) und diese Dateien hineinlegen:

```
app.py                 ← Einstiegsdatei, die muss Streamlit Cloud kennen
bausteine.py
chemie.py
block_haber_bosch.py
block_quantenwelt.py
hf_pure.py
requirements.txt
README.md
.gitignore
```

Per Kommandozeile:

```bash
git init
git add .
git commit -m "Arbeitskreis-App"
git branch -M main
git remote add origin https://github.com/<euer-name>/duenger-quantenwelt.git
git push -u origin main
```

### 2 · App verbinden

1. Auf <https://share.streamlit.io> mit dem GitHub-Konto anmelden.
2. **Create app** → **Deploy a public app from GitHub**.
3. Ausfüllen: Repository, Branch `main`, Main file path `app.py`, App URL frei
   wählbar – das wird der Link zum Verschicken.
4. **Deploy.** Der erste Start dauert ein bis zwei Minuten.

### 3 · Ändern

Jeder `git push` auf `main` baut die App automatisch neu.

Wenn die App eine Weile nicht benutzt wurde, schläft sie ein und braucht beim
nächsten Aufruf etwa 30 Sekunden. **Ruft den Link deshalb kurz vor dem
Arbeitskreis einmal selbst auf**, dann ist sie warm, wenn alle gleichzeitig
kommen.

---

## Ein Wort zur Sicherheit

Das Codefeld in Block 2, Kapitel 5 führt echten Python-Code auf dem Server aus
– anders wäre das Mitrechnen nicht möglich. Wer den Link hat, kann dort
beliebigen Code laufen lassen. Streamlit Community Cloud isoliert jede App in
einem eigenen Container, es geht also nicht um euer Notebook. Trotzdem gilt:

* **Keine Zugangsdaten, Tokens oder privaten Daten** ins Repository legen.
* Den Link nur an die Runde geben, nicht öffentlich streuen.

Abschalten lässt sich das Codefeld in Streamlit Cloud unter
**Settings → Secrets**:

```toml
CODEFELDER = false
```

Lokal geht dasselbe über die Umgebungsvariable `CODEFELDER=false`.

---

## Wie die Rechnungen entstehen

**Quantenchemie.** `hf_pure.py` ist eine eigenständige Hartree-Fock-
Implementierung in reinem numpy (STO-3G, Elemente H, C, N, O). Kein Compiler,
keine Chemiebibliothek, läuft überall. Alle Rechnungen in Block 2, Kapitel 5
laufen live im Moment des Knopfdrucks: die H₂-Kurve in unter einer Sekunde,
die Reaktionsenergie in rund drei, die N₂-Bindung in rund zwei.

**Gleichgewicht und Geschwindigkeit.** In `chemie.py`. Das Gleichgewicht ist
gegen die klassische Messtabelle von Larson & Dodge angepasst und trifft sie
zwischen 10 und 600 bar auf etwa einen Prozentpunkt. Die Geschwindigkeit ist
eine reine Arrhenius-Abschätzung, normiert auf den realen Betriebspunkt.

Alle Vereinfachungen und ihre Grenzen stehen in den 🔬-Kästen der jeweiligen
Kapitel – das gehört zum Thema des Arbeitskreises dazu.

---

## Selbsttest

```bash
python test_app.py
```

Klickt jedes Kapitel, jeden wichtigen Regler und jeden Rechenknopf durch und
meldet jede Ausnahme. Läuft in etwa einer Minute durch.

---

## Am Tag des Arbeitskreises

* **Link vorher aufwärmen** (siehe oben).
* **Jede und jeder öffnet den Link selbst** – auf dem Handy klappt die
  Navigation über das »-Symbol oben links auf.
* **Block 1, Kapitel 1** gehört dem Molekülbaukasten: N₂, H₂ und NH₃ von Hand
  nachbauen, bevor die App die Gleichung durchrechnet.
* **Die Ratefragen wirklich raten lassen.** Block 1 / Kapitel 2 („Wie viel mehr
  Aufwand für N≡N?") und Block 2 / Kapitel 5 („Wo liegt das Minimum?") sind die
  beiden Stellen, an denen die Runde aufwacht.
* **Block 1, Kapitel 4 ist der Wettbewerb.** Wer findet zuerst Bedingungen, bei
  denen alle drei Häkchen grün werden? Der Startpunkt (300 °C, 50 bar) liegt
  bewusst daneben.
* **Zeitplan:** Pro Block etwa 30 Minuten. Wer knapp in der Zeit ist, kann
  Block 2 / Kapitel 5 kürzen und nur Schritt 1 rechnen lassen.

---

Arbeitskreis „Vom Dünger zur Quantenwelt" · Constantin Richard Feitl &
Dato Tsomaia
