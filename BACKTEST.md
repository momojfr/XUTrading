# Manueller Backtest-Plan — Gold Fib-OB Swing Continuation

> Die Strategie aus `STRATEGY.md` **selbst** an historischen Daten durchklicken
> (TradingView Bar-Replay) und jeden Trade im Journal-Sheet erfassen — bis du
> **selbst** aus den Zahlen siehst, ob sie funktioniert. Kein Code, kein Signal
> von außen.

---

## Teil A — Einmaliges Setup in TradingView

1. **Chart:** XAUUSD / Gold, Timeframe **4H**.
2. **Indikatoren:**
   - **ATR, Länge 14** (für Impuls-Prüfung, Stop-Puffer, R).
   - **"EQH/EQL D.A.T"** mit **festen** Einstellungen (notiere die Settings, damit
     jeder Durchlauf identisch ist — die Liquiditäts-Level müssen reproduzierbar sein).
   - *Kein EMA.* (Bewusst raus.)
3. **Zeichentools bereitlegen:** Fib-Retracement-Tool und Rechteck (für den OB).
4. **Bar-Replay** aktivieren, Start **mind. 2–3 Jahre zurück**.

> Fraktale (5-Kerzen-Swings) kannst du per Auge erkennen oder einen
> Williams-Fractal-Indikator (Standard) einblenden — er markiert genau die
> 2-links-2-rechts-Swings aus `STRATEGY.md §2.1`.

---

## Teil B — Das Journal-Sheet

Importiere `backtest_trades_log.csv` in Google Sheets / Excel. Du trägst die
**Rohwerte** ein (Preise, ATR); Stop, R, TP1, Ergebnis rechnet das Sheet.

### Formeln (Zeile 2, nach unten ziehen)

Spalten-Layout des CSV (A…):

| Sp. | Kopf              | Inhalt / Formel                                                        |
|-----|-------------------|------------------------------------------------------------------------|
| A   | Trade#            | fortlaufend                                                            |
| B   | Datum_Setup       | Datum des 4H-Closes, an dem das Setup gültig wurde                     |
| C   | Richtung          | LONG / SHORT                                                           |
| D   | ATR14             | ATR-Wert am Setup-Tag (manuell ablesen)                                |
| E   | Fib0              | Impuls-Ursprung (manuell)                                              |
| F   | Fib1              | Impuls-Ende (manuell)                                                  |
| G   | Fib05             | `=(E2+F2)/2`                                                           |
| H   | OB_High           | manuell                                                                |
| I   | OB_Low            | manuell                                                                |
| J   | Impuls_ok?        | JA nur wenn `ABS(E2-F2) >= 2*D2` **und** ≤10 Kerzen **und** BOS (Auge) |
| K   | 05_in_OB?         | `=IF(AND(G2>=I2;G2<=H2);"JA";"NEIN")`                                  |
| L   | Fresh?            | JA / NEIN (manuell: Zone vorher nie angetappt?)                        |
| M   | Entry             | SHORT: `=I2`  /  LONG: `=H2`  (proximale OB-Kante)                     |
| N   | Stop              | SHORT: `=H2+0.1*D2`  /  LONG: `=I2-0.1*D2`                             |
| O   | R_$               | `=ABS(M2-N2)`                                                          |
| P   | TP1 (2R)          | SHORT: `=M2-2*O2`  /  LONG: `=M2+2*O2`                                 |
| Q   | Runner_Ziel       | nächster EQH/EQL-Pool (manuell ablesen) oder Fib-Ext −1.0             |
| R   | Runner_R          | `=ABS(Q2-M2)/O2`                                                       |
| S   | Runner_ok? (≥3R)  | `=IF(R2>=3;"JA";"NEIN")`                                               |
| T   | Ausgang           | SL / TP1+BE / TP1+RUNNER / FIX2R / ZEIT                                |
| U   | Ergebnis_R        | siehe Formel unten                                                     |
| V   | Notizen           | frei                                                                   |

**Ergebnis_R (Spalte U) — je nach Ausgang eintragen:**

```
SL              →  -1
TP1+BE          →   1        (0,5×2 + 0,5×0)
TP1+RUNNER      →  =1 + 0.5*R2     (0,5×2R + 0,5×Runner_R)
FIX2R           →   2        (kein Runner, volle Position bei 2R)
ZEIT            →   manuell (offener Gewinn/Verlust in R beim Schließen)
```

> Nur Zeilen mit `Impuls_ok?=JA` **und** `05_in_OB?=JA` **und** `Fresh?=JA`
> sind echte Trades. Der Rest ist "kein Setup" und fließt **nicht** in die
> Auswertung.

---

## Teil C — Der Ablauf (die Schleife)

Für **jeden** 4H-Close im Testzeitraum, streng von links nach rechts im Replay:

1. **Neuer bestätigter Swing?** Fraktale prüfen (§2.1).
2. **Gültiger Impuls?** Distanz ≥ 2×ATR **und** ≤ 10 Kerzen **und** BOS (§2.2).
   Nein → nächste Kerze.
3. **Fib** über den jüngsten Impuls ziehen → 0.5 ablesen (§2.3).
4. **OB finden:** letzte Gegenkerze vor dem Impuls, Zone High–Low (§2.4).
5. **Frisch?** Zone seit Entstehung nie angetappt? (§2.5) Nein → kein Trade.
6. **0.5 in OB?** (§3.1) Nein → kein Trade.
7. **Runner-Ziel** bestimmen (nächster EQH/EQL bzw. Fib-Ext) und ≥ 3R prüfen (§4).
8. Ist gerade **ein Trade offen**? Ja → nicht neu einsteigen, nur managen (Schritt 10).
9. **Limit setzen** an OB-Kante, Stop hinter OB. Zeile im Sheet anlegen —
   Entry/Stop/R/TP1 rechnen sich. Limit-Gültigkeit beachten (§3.3): neues Extrem
   jenseits Fib 1.0 **oder** 20 Kerzen ohne Fill → Order streichen, keine Zeile.
10. **Replay vorspulen** und mitschreiben, was zuerst passiert:
    - Stop vor TP1 → `SL`, −1R.
    - TP1 (+2R) erreicht → 50 % raus, Stop des Rests auf Break-Even.
    - Runner erreicht EQH/EQL-Ziel → `TP1+RUNNER`. BE-Stop getroffen → `TP1+BE`.
    - War Runner ungültig (<3R) → volle Position bei 2R → `FIX2R`.
    - Nichts nach 10 Handelstagen → `ZEIT`, in R schließen.
11. Nächste Kerze / nächstes Setup.

> **Disziplin:** Niemals vorspulen "um zu sehen wie's ausgeht", bevor der Entry
> im Sheet steht. Sonst verfälscht Hindsight-Bias das Ergebnis.

---

## Teil D — Auswertung (machst du selbst)

Ab **≥ 50 Trades** (besser 100+) unten im Sheet ausrechnen (U = Ergebnis_R):

| Kennzahl          | Formel                                                    |
|-------------------|-----------------------------------------------------------|
| Anzahl Trades     | `=COUNT(U2:U300)`                                          |
| Winrate           | `=COUNTIF(U2:U300;">0")/COUNT(U2:U300)`                    |
| Ø R pro Trade     | `=AVERAGE(U2:U300)`                                        |
| Summe R           | `=SUM(U2:U300)`                                            |
| Profit-Faktor     | `=SUMIF(U2:U300;">0")/-SUMIF(U2:U300;"<0")`                |
| Max. Drawdown (R) | über die kumulierte R-Kurve (min. von kumuliert − Hoch)   |
| Anteil Runner-Hits| `=COUNTIF(T2:T300;"TP1+RUNNER")/COUNT(U2:U300)`            |

**Referenz (nur zur Einordnung, kein Ziel):** deine bisherige diskretionäre
Gold-Strategie lag bei ~48 % Winrate / 1:2 → ≈ +0,44R pro Trade. Alles, was
**stabil deutlich positiv** ist bei erträglichem Drawdown, ist es wert,
forward getestet zu werden.

---

## Teil E — Anti-Curve-Fitting (nicht verhandelbar)

1. Zuerst mit den **Defaults** aus `STRATEGY.md §7`. Nichts anfassen.
2. Danach **eine** Schraube auf einmal, in einem **separaten** Durchlauf.
3. Zeitraum splitten: (falls überhaupt) auf der **ersten Hälfte** einstellen,
   auf der **zweiten Hälfte** bestätigen (Out-of-Sample). Nur-erste-Hälfte-gut → verworfen.
4. **Jeden** Trade erfassen, den die Regeln erzeugen. Kein Cherry-Picking.
5. Backtest **+** Out-of-Sample **+** Demo-Forward → erst dann echtes Geld.

---

## Teil F — Nächste Schritte

- [ ] TradingView einrichten (Teil A), EQH/EQL-Settings notieren.
- [ ] `backtest_trades_log.csv` importieren, Formeln einfügen (Teil B).
- [ ] Testzeitraum festlegen (Empfehlung: letzte 2–3 Jahre).
- [ ] Schleife (Teil C) durchziehen bis ≥ 50 Trades.
- [ ] Auswerten (Teil D) und selbst entscheiden.

Wenn beim Durchklicken **irgendeine** Regel doch Interpretationsspielraum lässt
(z.B. "welcher EQH/EQL-Pool ist der nächste?"), sag genau welche — dann schärfen
wir diese eine Regel nach, bis sie wieder ein reines Ja/Nein ist.
