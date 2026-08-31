# Vom Dünger zur Quantenwelt

Interaktive Streamlit-App zum Arbeitskreis *„Vom Dünger zur Quantenwelt –
wie Wissenschaft unser Weltbild transformiert“* (Pro Scientia).

Eine App, zwei Blöcke, ein Link. Kein Vorwissen nötig.

---

## Was drin ist

| Block | Kapitel | Worum es geht |
|---|---|---|
| **Start** | – | Einstieg, Bedienhinweise, roter Faden |
| **1 · Haber-Bosch** | 6 | Von der Luft über die Bindungsenergie und den Reaktor bis zur Quantenchemie und der Ethik |
| **2 · Quantenwelt** | 8 | Teilchen im Kasten, von der Gitarrensaite bis zum QLED-Fernseher |
| **Werkzeugkasten** | – | Einheiten-Übersetzer, Glossar, Quellen |

### Die drei Regeln, nach denen die App gebaut ist

1. **Keine Fachzahl steht allein.** Neben jeder Zahl steht ein Vergleich, ein
   Bild oder ein Balken. Die nackten Werte, Formeln und Vorbehalte liegen in
   den ausklappbaren 🔬-Kästen.
2. **Ein einziger Maßstab.** Statt kJ/mol zu erklären, wird alles an einer
   Größe gemessen: der Wärme, die ein Molekül bei Zimmertemperatur zur
   Verfügung hat (2,4 kJ/mol). Die Dreifachbindung im Stickstoff ist das
   388-fache davon – das reicht als Verständnis für das ganze Kapitel.
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

Ergebnis ist eine öffentliche Adresse wie
`https://euer-name.streamlit.app`, die ihr einfach weitergeben könnt.

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
vorberechnet.json      ← nicht vergessen, sonst fehlt Kapitel 3 die N₂-Kurve
requirements.txt
.streamlit/config.toml
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

Wer lieber klickt: Auf GitHub „Add file → Upload files“, alle Dateien
hineinziehen. Wichtig ist nur, dass der Ordner `.streamlit` mitkommt – über
die Weboberfläche muss man ihn ggf. anlegen, indem man beim Dateinamen
`.streamlit/config.toml` eingibt.

### 2 · App verbinden

1. Auf <https://share.streamlit.io> mit dem GitHub-Konto anmelden.
2. **Create app** → **Deploy a public app from GitHub**.
3. Ausfüllen:
   - **Repository:** `<euer-name>/duenger-quantenwelt`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** frei wählbar, das wird der Link zum Verschicken.
4. **Deploy.** Der erste Start dauert ein bis zwei Minuten, weil numpy und
   matplotlib installiert werden.

### 3 · Ändern

Jeder `git push` auf `main` baut die App automatisch neu. Für kleine
Textänderungen reicht das Bearbeiten direkt auf GitHub.

Wenn die App eine Weile nicht benutzt wurde, schläft sie ein und braucht beim
nächsten Aufruf etwa 30 Sekunden. **Ruft den Link deshalb kurz vor dem
Arbeitskreis einmal selbst auf**, dann ist sie warm, wenn alle gleichzeitig
kommen.

---

## Ein Wort zur Sicherheit

Die Codefelder führen echten Python-Code auf dem Server aus – anders wäre das
Mitrechnen nicht möglich. Wer den Link hat, kann dort beliebigen Code laufen
lassen. Streamlit Community Cloud isoliert jede App in einem eigenen
Container, es geht also nicht um euer Notebook. Trotzdem gilt:

* **Keine Zugangsdaten, Tokens oder privaten Daten** ins Repository legen.
* Den Link nur an die Runde geben, nicht öffentlich streuen.

Wenn ihr die Codefelder für den öffentlichen Link lieber abschalten wollt:
in Streamlit Cloud unter **Settings → Secrets** eintragen

```toml
CODEFELDER = false
```

Alles andere – Regler, Grafiken, Rechnungen auf Knopfdruck – bleibt
unverändert. Lokal geht dasselbe über die Umgebungsvariable
`CODEFELDER=false`.

---

## Wie die Rechnungen entstehen

**Quantenchemie.** `hf_pure.py` ist eine eigenständige Hartree-Fock-
Implementierung in reinem numpy (STO-3G, Elemente H, C, N, O). Kein Compiler,
keine Chemiebibliothek, läuft überall. Die Rechnungen in Kapitel 3 laufen
live im Moment des Knopfdrucks: H₂ braucht Sekundenbruchteile, die
Reaktionsenergie rund vier Sekunden. Nur die N₂-Kurve liegt vorberechnet in
`vorberechnet.json`, weil sie live etwa eine Minute bräuchte.

Neu erzeugen lässt sie sich mit:

```bash
python vorberechnen.py
```

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
meldet jede Ausnahme. Läuft in rund einer Minute durch.

---

## Am Tag des Arbeitskreises

* **Link vorher aufwärmen** (siehe oben).
* **Jede und jeder öffnet den Link selbst** – auf dem Handy klappt die
  Navigation über das »-Symbol oben links auf. Am Beamer die eigene Instanz
  führen und die Runde nebenher mitspielen lassen.
* **Die Ratefragen wirklich raten lassen.** Kapitel 1 („Wie viel mehr Aufwand
  für N≡N?“) und Kapitel 3 („Wo liegt das Minimum?“) sind die beiden Stellen,
  an denen die Runde aufwacht. Ein paar Tipps laut abfragen, bevor jemand auf
  *Auflösen* drückt.
* **Kapitel 2 ist der Wettbewerb.** Wer findet zuerst Bedingungen, bei denen
  alle drei Häkchen grün werden? Der Startpunkt (300 °C, 50 bar) liegt
  bewusst daneben.
* **Zeitplan:** Pro Block etwa 30 Minuten Klicken, dann die Diskussionsfragen.
  Wer knapp in der Zeit ist, kann Kapitel 3 (Quantenchemie) überspringen und
  nach dem Reaktor direkt zu „Brot und Sprengstoff“.

---

Arbeitskreis „Vom Dünger zur Quantenwelt“ · Constantin Richard Feitl &
Dato Tsomaia
