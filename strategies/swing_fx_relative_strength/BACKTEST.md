# Manueller Backtest-Plan — FX Relative-Strength Swing Rotation

> Ziel: Die Strategie aus `STRATEGY.md` **selbst** an historischen Daten
> durchklicken (TradingView Bar-Replay) und jeden Trade in einem Journal-Sheet
> erfassen — bis du **selbst** aus den Zahlen siehst, ob sie funktioniert.
> Kein Code, kein Signal von außen. Nur du, der Replay und dein Sheet.

---

## Teil A — Einmaliges Setup in TradingView

### A.1 Mess-Layout (zum Ranken)

Erstelle ein Chart-Layout mit **7 Charts** nebeneinander (TradingView:
"Select Layout" → 8-Chart-Grid, 7 davon nutzen), alle auf **Daily**:

```
EURUSD   GBPUSD   AUDUSD   NZDUSD
USDJPY   USDCHF   USDCAD   (8. frei)
```

Auf **jedem** dieser 7 Charts:
- Indikator **ROC (Rate of Change)** hinzufügen, **Länge = 20**.

Speichere das Layout als **"STRENGTH"**.

### A.2 Trade-Layout (zum Ausführen/Managen)

Zweites Layout mit **2 Charts** desselben Paares:
- Links: **Daily** mit **SMA(50)** und **ATR(14)**.
- Rechts: **4H** (für den Einstiegs-Open).

Speichere als **"TRADE"**.

### A.3 Replay aktivieren

- Öffne Bar-Replay (Button oben in der Toolbar).
- Setze den Startpunkt auf den Beginn deines Testzeitraums (Empfehlung: mind.
  **3 Jahre zurück** → ergibt ~100–150 Trades bei max. 1 Trade/Woche).

---

## Teil B — Das Journal-Sheet

Importiere die zwei mitgelieferten CSV-Vorlagen in Google Sheets oder Excel:

- `backtest_strength_log.csv` → Tab **"Stärke"**
- `backtest_trades_log.csv`  → Tab **"Trades"**

### B.1 Tab "Stärke" — Formeln (nach dem Import einfügen)

Du tippst pro Woche nur die **7 ROC-Werte** (Spalten C–I). Der Rest rechnet sich
selbst. Trage in Zeile 2 folgende Formeln ein und zieh sie nach unten:

| Spalte | Kopf        | Formel (Zeile 2)                                            |
|--------|-------------|------------------------------------------------------------|
| C      | EURUSD_ROC  | *(manuell ablesen)*                                        |
| D      | GBPUSD_ROC  | *(manuell)*                                                |
| E      | AUDUSD_ROC  | *(manuell)*                                                |
| F      | NZDUSD_ROC  | *(manuell)*                                                |
| G      | USDJPY_ROC  | *(manuell)*                                                |
| H      | USDCHF_ROC  | *(manuell)*                                                |
| I      | USDCAD_ROC  | *(manuell)*                                                |
| J      | EUR         | `=C2`                                                       |
| K      | GBP         | `=D2`                                                       |
| L      | AUD         | `=E2`                                                       |
| M      | NZD         | `=F2`                                                       |
| N      | JPY         | `=-G2`                                                      |
| O      | CHF         | `=-H2`                                                      |
| P      | CAD         | `=-I2`                                                      |
| Q      | USD         | `=-AVERAGE(C2:I2)`                                          |
| R      | Stärkste    | `=INDEX($J$1:$Q$1;MATCH(MAX(J2:Q2);J2:Q2;0))`              |
| S      | Schwächste  | `=INDEX($J$1:$Q$1;MATCH(MIN(J2:Q2);J2:Q2;0))`             |
| T      | Spread      | `=MAX(J2:Q2)-MIN(J2:Q2)`                                    |

> Zeile 1 (J1:Q1) enthält die Kürzel EUR,GBP,AUD,NZD,JPY,CHF,CAD,USD — die
> INDEX/MATCH-Formeln lesen daraus den Namen der stärksten/schwächsten Währung.
> `Spread` (T) ist optional: je größer, desto klarer der Trend — später ein
> möglicher Zusatzfilter.

### B.2 Tab "Trades" — Formeln

Pro Trade Einstiegspreis, ATR und Richtung eintragen; Stop/Ziel/Ergebnis
rechnen sich:

| Spalte | Kopf         | Formel / Inhalt                                                        |
|--------|--------------|------------------------------------------------------------------------|
| A      | Trade#       | fortlaufend                                                            |
| B      | Einstiegdatum| *(manuell)*                                                           |
| C      | Paar         | *(manuell, aus Tab Stärke)*                                           |
| D      | Richtung     | BUY / SELL                                                             |
| E      | Einstieg     | *(4H-Open, manuell)*                                                  |
| F      | ATR14_Daily  | *(manuell ablesen)*                                                   |
| G      | Stop         | BUY: `=E2-1.5*F2`  /  SELL: `=E2+1.5*F2`                              |
| H      | Ziel (+2R)   | BUY: `=E2+3*F2`   /  SELL: `=E2-3*F2`   *(2R = 2×1,5ATR = 3ATR)*      |
| I      | SMA-Filter?  | JA / NEIN *(nur JA-Trades werden gehandelt)*                          |
| J      | Ausstiegdatum| *(manuell)*                                                          |
| K      | Ausstieggrund| TP / SL / ROTATION / ZEIT                                             |
| L      | Ergebnis (R) | TP→`2`, SL→`-1`, sonst manuell in R                                   |
| M      | Notizen      | frei                                                                   |

---

## Teil C — Der wöchentliche Ablauf (die Schleife)

Wiederhole das für **jede Woche** deines Testzeitraums:

1. **Replay auf Montag-Open** der Woche stellen (im "STRENGTH"-Layout).
2. **7 ROC-Werte ablesen** (letzte abgeschlossene = Freitags-Kerze) und in Tab
   "Stärke" eintragen. → Sheet zeigt automatisch **Stärkste** und **Schwächste**.
3. **Paar & Richtung** bestimmen (Regelwerk §4). Kein Gleichstand? Sonst: keine
   Zeile in "Trades", weiter zu Woche N+1.
4. Ist gerade **ein Trade offen**? → Wenn ja, **nicht** neu einsteigen, springe
   zu Schritt 7 (Management). Wenn nein, weiter.
5. Ins **"TRADE"-Layout** wechseln, Paar laden:
   - **50-SMA-Filter** prüfen (§5). NEIN → keine neue Position, weiter zu Woche N+1.
   - JA → **ATR(14)** ablesen, **4H-Open** als Einstieg notieren. Zeile in Tab
     "Trades" anlegen. Stop/Ziel rechnet das Sheet.
6. **Replay Tag für Tag vorspulen** und beobachten, was zuerst passiert:
   - Stop getroffen → Ausstieg SL, Ergebnis −1R.
   - Ziel getroffen → Ausstieg TP, Ergebnis +2R.
   - Beides nicht bis nächsten Montag → offen lassen, weiter zu Schritt 7.
7. **Am nächsten Montag (Management-Check):**
   - Neues Ranking ziehen (Schritt 2).
   - **Rotations-Exit** (§6.3): starke Währung aus Rang 1–2 gefallen **oder**
     schwache aus Rang 7–8 gestiegen → Ausstieg zum 4H-Open, Grund ROTATION.
   - Sonst: Trade läuft weiter (max. 10 Handelstage, §6.4).
8. Zurück zu Schritt 1 für die nächste Woche.

> **Disziplin-Regel:** Immer streng von links nach rechts durch den Replay.
> Niemals "vorspulen und schauen wie's ausgeht" bevor du den Einstieg gesetzt
> hast. Das verfälscht das Ergebnis (Hindsight-Bias).

---

## Teil D — Auswertung (das machst du selbst)

Wenn du genug Trades hast (**Ziel: mind. 50, besser 100+**), rechne unten im
Tab "Trades" aus:

| Kennzahl            | Formel (Bereich L2:L... = R-Ergebnisse)                          |
|---------------------|------------------------------------------------------------------|
| Anzahl Trades       | `=COUNT(L2:L200)`                                                 |
| Winrate             | `=COUNTIF(L2:L200;">0")/COUNT(L2:L200)`                          |
| Ø R pro Trade       | `=AVERAGE(L2:L200)`                                               |
| Summe R             | `=SUM(L2:L200)`                                                   |
| Profit-Faktor       | `=SUMIF(L2:L200;">0")/-SUMIF(L2:L200;"<0")`                       |
| Erwartungswert      | = Ø R pro Trade (bei fixem 1:2: `Winrate×2 − (1−Winrate)×1`)      |
| Max. Drawdown (R)   | über die kumulierte R-Kurve (min. von kumuliert − laufendem Hoch) |

**Referenzpunkt (zum Einordnen, nicht als Ziel):** Deine bisherige
diskretionäre Gold-Strategie hatte laut Journal ~48 % Winrate bei 1:2 → ≈ +0,44R
Erwartung pro Trade. Alles, was **stabil deutlich positiv** ist und dabei einen
erträglichen Drawdown hat, ist es wert, danach **forward** getestet zu werden.

---

## Teil E — Anti-Curve-Fitting-Regeln (nicht verhandelbar)

1. **Zuerst mit den Defaults** aus `STRATEGY.md §9` testen. Kein Anfassen.
2. Erst danach **eine** Schraube auf einmal ändern und einen **separaten**
   Durchlauf machen. Nie mehrere gleichzeitig.
3. Teile den Zeitraum: optimiere (falls überhaupt) nur auf der **ersten Hälfte**,
   bestätige auf der **zweiten Hälfte** (Out-of-Sample). Wenn es nur auf der
   ersten Hälfte gut ist → verworfen.
4. **Jeden** Trade erfassen, den die Regeln erzeugen — auch die hässlichen.
   Kein Cherry-Picking von Wochen.
5. Erst wenn Backtest **und** Out-of-Sample **und** danach ein Demo-Forward-Test
   überzeugen → echtes Geld.

---

## Teil F — Nächste Schritte

- [ ] Layouts "STRENGTH" und "TRADE" in TradingView anlegen (Teil A).
- [ ] Beide CSV-Vorlagen importieren und Formeln einfügen (Teil B).
- [ ] Testzeitraum festlegen (Empfehlung: letzte 3 Jahre).
- [ ] Die Schleife (Teil C) durchziehen, bis ≥ 50 Trades im Sheet stehen.
- [ ] Auswerten (Teil D) und selbst entscheiden.

Wenn du beim Durchklicken merkst, dass irgendeine Regel doch noch
Interpretationsspielraum lässt: sag Bescheid, dann schärfen wir genau diese
eine Regel nach, bis sie wieder ein reines Ja/Nein ist.
