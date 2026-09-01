# Vom Dünger zur Quantenwelt

Interaktive Streamlit-App zum Arbeitskreis *„Vom Dünger zur Quantenwelt. Wie
Wissenschaft unser Weltbild transformiert"* (Pro Scientia).

Eine App, zwei Blöcke, ein Link. Kein Vorwissen nötig.

---

## Was drin ist

| Seite | Kapitel | Worum es geht |
|---|---|---|
| **Start** | | Einstieg und Bedienhinweise |
| **Block 1 · Dünger aus Luft** | 4 | Von der Luft über die Bindungsenergie und den Katalysator bis zu Haber und Bosch |
| **Block 2 · Die Quantenwelt** | 5 | Teilchen im Kasten, von der Gitarrensaite über den QLED-Fernseher bis zur live gerechneten Quantenchemie |
| **Nachschlagen** | | Fachwörter und Quellen |

Die App ist nur ein Teil des Nachmittags. Der Geigerzähler und die Diskussion
passieren im Raum. Wie alles zusammenspielt und was man wo dazu
sagt, steht in **[manuskript.md](manuskript.md)**.

Deshalb enthält die App selbst keine Diskussionsfragen. Sie erklärt, die Runde
diskutiert.

### Die drei Regeln, nach denen sie gebaut ist

1. **Keine Zahl steht allein.** Neben jeder Zahl steht ein Vergleich, ein Bild
   oder ein Balken. Die nackten Werte, Formeln und Vorbehalte liegen in den
   ausklappbaren 🔬-Kästen.
2. **Ein einziger Maßstab.** Statt kJ/mol zu erklären, wird alles an einer
   Größe gemessen: der Energie, die die Umgebungswärme einem Molekül bei 20 °C
   mitgibt, also rund 2,4 kJ/mol. Die Dreifachbindung im Stickstoff ist das
   388-fache davon. Das reicht als Verständnis für das ganze Kapitel.
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
block_haber_bosch.py
block_quantenwelt.py
hf_pure.py
requirements.txt
manuskript.md
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
2. **Create app**, dann **Deploy a public app from GitHub**.
3. Ausfüllen: Repository, Branch `main`, Main file path `app.py`. Die App URL
   ist frei wählbar und wird der Link zum Verschicken.
4. **Deploy.** Der erste Start dauert ein bis zwei Minuten.

### 3 · Ändern

Jeder `git push` auf `main` baut die App automatisch neu.

Wenn die App eine Weile nicht benutzt wurde, schläft sie ein und braucht beim
nächsten Aufruf etwa 30 Sekunden. **Ruft den Link deshalb kurz vor dem
Arbeitskreis einmal selbst auf**, dann ist sie warm, wenn alle gleichzeitig
kommen.

---

## Ein Wort zur Sicherheit

Das Codefeld in Block 2, Kapitel 5 führt echten Python-Code auf dem Server
aus. Anders wäre das Mitrechnen nicht möglich. Wer den Link hat, kann dort
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

`hf_pure.py` ist eine eigenständige Hartree-Fock-Implementierung in reinem
numpy (STO-3G, Elemente H, C, N, O). Kein Compiler, keine Chemiebibliothek,
läuft überall. Alle Rechnungen in Block 2, Kapitel 5 laufen live im Moment des
Knopfdrucks: die H₂-Kurve in unter einer Sekunde, die Reaktionsenergie in rund
drei Sekunden, die N₂-Bindung in rund zwei.

Verglichen wird gegen spektroskopische Taltiefen *D*<sub>e</sub> und nicht
gegen die geläufigen Tabellenwerte, weil die Rechnung die Kerne festhält und
die Nullpunktsschwingung nicht kennt. Alle Vereinfachungen und ihre Grenzen
stehen in den 🔬-Kästen der jeweiligen Kapitel. Das gehört zum Thema des
Arbeitskreises dazu.

---

## Selbsttest

```bash
python test_app.py
```

Klickt jedes Kapitel, jeden wichtigen Regler und jeden Rechenknopf durch und
meldet jede Ausnahme. Läuft in etwa einer Minute durch.

---

Arbeitskreis „Vom Dünger zur Quantenwelt" · Constantin Richard Feitl &
Dato Tsomaia
