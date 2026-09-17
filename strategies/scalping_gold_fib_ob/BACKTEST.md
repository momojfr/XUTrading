# Manueller Backtest-Plan — Gold Fib-OB Scalping

> Die Strategie aus `STRATEGY.md` **selbst** an historischen Daten durchklicken
> (TradingView Bar-Replay) und jeden Trade im Journal-Sheet erfassen — bis du
> **selbst** aus den Zahlen siehst, ob sie funktioniert. Kein Code, kein Signal.

---

## Teil A — Einmaliges Setup in TradingView

1. **Chart:** XAUUSD / Gold, Timeframe **15m**.
2. **Indikatoren:**
   - **ATR, Länge 14** (Impuls-Prüfung, Stop-Puffer, R).
   - **"EQH/EQL D.A.T"** mit **festen** Einstellungen — Settings hier notieren,
     damit jeder Durchlauf identisch ist: `______________________`.
   - *Kein EMA.*
   - Optional Williams-Fractal (Standard) für die 5-Kerzen-Swings.
3. **Session-Fenster in DEINER Chart-Zeitzone fixieren** (einmal ausrechnen und
   hier eintragen — danach nie mehr ändern):
   - London: `08:00–11:00` → lokal: `__________`
   - New York: `13:30–16:30` → lokal: `__________`
4. **Zeichentools:** Fib-Retracement + Rechteck (OB).
5. **Bar-Replay** aktivieren. Scalping erzeugt viele Setups → schon **2–3 Monate**
   reichen oft für ≥ 50 Trades. Lieber mehrere kurze, verschiedene Zeitfenster
   (ruhiger Markt + volatiler Markt) als ein einziger Block.

---

## Teil B — Das Journal-Sheet

Importiere `journal_trades_log.csv`. Du trägst die **Rohwerte** ein; Stop, R,
TP1, Ergebnis rechnet das Sheet.

### Formeln (Zeile 2, nach unten ziehen)

| Sp. | Kopf              | Inhalt / Formel                                                        |
|-----|-------------------|------------------------------------------------------------------------|
| A   | Trade#            | fortlaufend                                                            |
| B   | Datum_Zeit        | 15m-Close, an dem das Setup gültig wurde                               |
| C   | Session           | LONDON / NY                                                            |
| D   | Richtung          | LONG / SHORT                                                           |
| E   | ATR14             | ATR am Setup-Zeitpunkt (manuell)                                       |
| F   | Fib0              | Impuls-Ursprung (manuell)                                              |
| G   | Fib1              | Impuls-Ende (manuell)                                                  |
| H   | Fib05             | `=(F2+G2)/2`                                                           |
| I   | OB_High           | manuell                                                                |
| J   | OB_Low            | manuell                                                                |
| K   | Impuls_ok?        | JA nur wenn `ABS(F2-G2) >= 2*E2` **und** ≤10 Kerzen **und** BOS        |
| L   | 05_in_OB?         | `=IF(AND(H2>=J2;H2<=I2);"JA";"NEIN")`                                  |
| M   | Fresh?            | JA / NEIN (Zone vorher nie angetappt?)                                 |
| N   | InSession?        | JA / NEIN (§1.1)                                                       |
| O   | Entry             | SHORT: `=J2`  /  LONG: `=I2`                                           |
| P   | Stop              | SHORT: `=I2+0.1*E2`  /  LONG: `=J2-0.1*E2`                             |
| Q   | R_$               | `=ABS(O2-P2)`                                                          |
| R   | TP1 (2R)          | SHORT: `=O2-2*Q2`  /  LONG: `=O2+2*Q2`                                 |
| S   | Runner_Ziel       | nächster EQH/EQL-Pool (manuell) oder Fib-Ext −1.0                     |
| T   | Runner_R          | `=ABS(S2-O2)/Q2`                                                       |
| U   | Runner_ok? (≥3R)  | `=IF(T2>=3;"JA";"NEIN")`                                               |
| V   | Ausgang           | SL / TP1+BE / TP1+RUNNER / FIX2R / ZEIT                                |
| W   | Ergebnis_R        | siehe unten                                                           |
| X   | Notizen           | frei                                                                   |

**Ergebnis_R (Spalte W):**

```
SL              →  -1
TP1+BE          →   1
TP1+RUNNER      →  =1 + 0.5*T2
FIX2R           →   2
ZEIT            →   manuell (Stand in R beim Session-Ende-Close)
```

> Echter Trade nur, wenn `Impuls_ok?` **und** `05_in_OB?` **und** `Fresh?`
> **und** `InSession?` alle JA sind. Der Rest ist "kein Setup" → nicht auswerten.

---

## Teil C — Der Ablauf (die Schleife)

Für **jeden** 15m-Close, streng von links nach rechts im Replay:

1. **Im Session-Fenster?** (§1.1) Nein → keine neuen Entries, nur offene Trades
   managen (Schritt 10). 
2. **Neuer bestätigter Swing?** Fraktale prüfen (§2.1).
3. **Gültiger Impuls?** ≥ 2×ATR **und** ≤ 10 Kerzen **und** BOS (§2.2). Nein → weiter.
4. **Fib** über jüngsten Impuls → 0.5 ablesen (§2.3).
5. **OB finden** (letzte Gegenkerze vor Impuls, High–Low) (§2.4).
6. **Frisch?** (§2.5) Nein → kein Trade.
7. **0.5 in OB?** (§3.1) Nein → kein Trade.
8. **Runner-Ziel** bestimmen und ≥ 3R prüfen (§4).
9. Trade offen? Ja → nicht neu einsteigen. Nein → **Limit** an OB-Kante, Stop
   hinter OB, Zeile anlegen. Limit-Gültigkeit (§3.3): neues Extrem jenseits
   Fib 1.0, 10 Kerzen ohne Fill, oder Session-Ende → Order streichen.
10. **Replay vorspulen**, mitschreiben was zuerst passiert:
    - Stop vor TP1 → `SL`, −1R.
    - TP1 (+2R) → 50 % raus, Rest-Stop auf Break-Even.
    - Runner erreicht EQH/EQL → `TP1+RUNNER`; BE-Stop → `TP1+BE`.
    - Runner ungültig (<3R) → volle Position bei 2R → `FIX2R`.
    - **New-York-Session-Ende (16:30) erreicht** → alles schließen → `ZEIT`.
11. Nächste Kerze / nächstes Setup.

> **Disziplin:** Nie vorspulen "um zu sehen wie's ausgeht", bevor der Entry im
> Sheet steht. Kein Übernacht-Halten — Scalp endet mit der Session.

---

## Teil D — Auswertung (machst du selbst)

Ab **≥ 50 Trades** (besser 100+) unten im Sheet (W = Ergebnis_R):

| Kennzahl          | Formel                                                    |
|-------------------|-----------------------------------------------------------|
| Anzahl Trades     | `=COUNT(W2:W400)`                                          |
| Winrate           | `=COUNTIF(W2:W400;">0")/COUNT(W2:W400)`                    |
| Ø R pro Trade     | `=AVERAGE(W2:W400)`                                        |
| Summe R           | `=SUM(W2:W400)`                                            |
| Profit-Faktor     | `=SUMIF(W2:W400;">0")/-SUMIF(W2:W400;"<0")`                |
| Max. Drawdown (R) | über die kumulierte R-Kurve (min. von kumuliert − Hoch)   |
| Runner-Hit-Quote  | `=COUNTIF(V2:V400;"TP1+RUNNER")/COUNT(W2:W400)`            |
| London vs NY      | Winrate/Ø R je Session getrennt (welche Session trägt?)   |

> Extra fürs Scalping: werte **London und NY getrennt** aus. Oft trägt nur eine
> Session — dann kannst du die andere später streichen (das ist der Session-Filter
> als Tunable, §7).

---

## Teil E — Anti-Curve-Fitting (nicht verhandelbar)

1. Zuerst mit den **Defaults** (`STRATEGY.md §7`). Nichts anfassen.
2. Danach **eine** Schraube auf einmal, separater Durchlauf.
3. Zeitraum splitten: auf einem Teil einstellen, auf einem **anderen** bestätigen
   (Out-of-Sample). Nur-ein-Teil-gut → verworfen.
4. **Jeden** Trade erfassen. Kein Cherry-Picking von Setups oder Tagen.
5. Backtest **+** Out-of-Sample **+** Demo-Forward → erst dann echtes Geld.

---

## Teil F — Nächste Schritte

- [ ] TradingView einrichten (Teil A), Session-Zeiten + EQH/EQL-Settings fixieren.
- [ ] `journal_trades_log.csv` importieren, Formeln einfügen (Teil B).
- [ ] Ein paar Monate im Replay durchziehen bis ≥ 50 Trades.
- [ ] Auswerten (Teil D), London vs NY vergleichen, selbst entscheiden.

Wenn eine Regel beim Durchklicken doch Interpretationsspielraum lässt (z.B.
"welcher EQH/EQL-Pool ist der nächste?"), sag genau welche — dann härten wir
sie nach, bis sie wieder reines Ja/Nein ist.
