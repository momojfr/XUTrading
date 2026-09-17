# Gold Fib-OB Scalping Continuation — Regelwerk

> Ziel: Ein Scalping-Setup, bei dem **jede** Entscheidung eine Zahl aus dem
> Chart ist. Kein Augenmaß, kein diskretionäres Fib. Zwei Leute mit denselben
> Daten kommen zu **identischen** Trades.
>
> Diese Datei ist die einzige Wahrheit. Steht eine Situation hier nicht drin,
> wird **nicht** gehandelt.

---

## 0. Kernidee (in einem Satz)

Nach einem starken Intraday-Impuls zieht sich der Kurs zurück. Liegt das
**50 %-Retracement (Fib 0.5)** genau in einem **frischen Order Block**, steigen
wir **in Richtung des Impulses** ein und lassen einen Teil als **Runner** bis zur
nächsten Liquidität laufen — alles innerhalb der Session, ohne Übernacht-Risiko.

---

## 1. Markt & Zeitrahmen (fest)

| Punkt              | Festlegung                                                    |
|--------------------|---------------------------------------------------------------|
| Instrument         | **XAUUSD / Gold**                                             |
| Arbeits-Timeframe  | **15m** — Impuls, Fib, OB, Entry, EQH/EQL alles auf 15m       |
| Verfeinerung       | **5m** optional nur für den exakten Fill (Tunable, §7)        |
| Stil               | **Scalping / intraday** — Trades werden am selben Tag geschlossen |
| Entscheidungstakt  | bei jedem abgeschlossenen **15m-Close** innerhalb der Session |

Kein EMA, kein zusätzlicher Trendfilter. Bewusst minimal.

### 1.1 Session-Filter (Uhrzeit = reines Ja/Nein)

Einstiege **nur** im aktiven Handelsfenster (Gold-Volatilität konzentriert sich
dort). Zeiten in **deiner Chart-Zeitzone einmal fixieren** und notieren:

- **London:** 08:00–11:00
- **New York:** 13:30–16:30

Außerhalb dieser Fenster → **kein neuer Entry.** (Verwaltung offener Trades
läuft weiter, siehe §4.)

> Trage deine tatsächlichen lokalen Zeiten in `BACKTEST.md` Teil A ein, damit
> jeder Durchlauf identisch ist.

---

## 2. Bausteine — alle objektiv definiert

### 2.1 Swing-Punkt (5-Kerzen-Fraktal)

- **Swing-Hoch (SH):** Kerze, deren **Hoch** höher ist als die Hochs der
  **2 Kerzen links und 2 rechts**.
- **Swing-Tief (ST):** Spiegelbild.

> Erst **bestätigt**, wenn die 2 Kerzen rechts geschlossen sind. Kein Vorgriff.

### 2.2 Impuls (das Fib-Fundament)

Gültiger Impuls, wenn **alle 3** erfüllt sind (Beispiel Abwärts, SH→ST):

1. **Größe:** `SH_Hoch − ST_Tief` ≥ **2,0 × ATR(14)** (ATR auf 15m).
2. **Tempo:** vom SH bis zum ST **≤ 10 Kerzen** (≤ 2,5 h auf 15m).
3. **Struktur-Bruch (BOS):** das ST bricht **unter** das vorherige bestätigte ST.

Aufwärts-Impuls = Spiegelbild (ST→SH, ≥ 2 ATR, ≤ 10 Kerzen, bricht vorheriges SH).

> Mehrere gültige Impulse gleichzeitig → nimm den **jüngsten**.

### 2.3 Fibonacci

- Abwärts: **0 = SH_Hoch**, **1 = ST_Tief**.
- Aufwärts: **0 = ST_Tief**, **1 = SH_Hoch**.
- **0.5 = Mitte:** `(0-Level + 1-Level) / 2`.

### 2.4 Order Block (OB)

- **Bearisher OB** (Shorts): letzte Kerze mit **bullischem Close** (Close > Open)
  **direkt vor** dem Abwärts-Impuls.
- **Bullischer OB** (Longs): letzte Kerze mit **bärischem Close** direkt vor dem
  Aufwärts-Impuls.
- **Zone = ganze Kerze High–Low.**

### 2.5 "Frisch" (unmitigiert)

Frisch = seit Entstehung ist **keine** Kerze in die Zone (High–Low) gelaufen —
dieser Retracement ist der **erste** Tap. Vorher berührt → **verbraucht → kein Trade.**

### 2.6 EQH/EQL (Liquidität)

Level des Indikators **"EQH/EQL D.A.T"** mit **festen** Einstellungen. Rolle:
**Ziel für den Runner** (§4).

---

## 3. Einstieg (Trigger + Ausführung)

### 3.1 Confluence-Bedingung (Ja/Nein)

```
OB_Tief ≤ Fib-0.5-Preis ≤ OB_Hoch     UND     OB ist frisch (§2.5)
UND innerhalb des Session-Fensters (§1.1)
```

Nicht erfüllt → **kein Trade.**

### 3.2 Entry, Stop, R

- **Entry = Limit an der proximalen OB-Kante:**
  - Short: Limit am **OB-Tief**. Long: Limit am **OB-Hoch**.
- **Stop = hinter der distalen OB-Kante + 0,1 × ATR(14):**
  - Short: **OB-Hoch + 0,1×ATR**. Long: **OB-Tief − 0,1×ATR**.
- **R = | Entry − Stop |.**
- **Positionsgröße:** Verlust bei Stop = **1 % des Kontos** (fürs Scalping ggf.
  auch niedriger, aber im Backtest konstant halten).

### 3.3 Gültigkeit der Limit-Order

Order verfällt vor dem Fill, wenn eines eintritt:

1. neues Extrem **jenseits Fib 1.0**, **oder**
2. **10 Kerzen** ohne Fill (Scalp: schneller als beim Swing), **oder**
3. das **Session-Fenster endet** (§1.1) — dann Order streichen.

---

## 4. Ausstieg — Teilgewinn + Runner (2-teilig, objektiv)

Position **50 / 50** geteilt.

| Teil            | Regel                                                                 |
|-----------------|-----------------------------------------------------------------------|
| **TP1 (50 %)**  | bei **+2R** schließen. Stop des Rests auf **Break-Even (Entry)**.      |
| **Runner (50 %)** | Ziel = **nächster gegenüberliegender EQH/EQL-Pool in Impuls-Richtung** (Short → nächster EQL darunter; Long → nächster EQH darüber). |

**Runner-Fallback:** kein passender EQH/EQL-Pool → Runner-Ziel = **Fib-Extension −1.0**.

**Gültigkeits-Check:** Runner-Ziel muss **≥ 3R** vom Entry entfernt sein.
Ist die nächste Liquidität **< 3R** → **kein Runner**, volle Position bei **+2R** (fix 2R).

**Feste Exit-Regeln:**
- Stop vor TP1 → ganze Position **−1R**.
- Nach TP1 nur noch **+Runner** oder **Break-Even (0)** möglich — nie wieder Verlust.
- **Intraday-Zeit-Stop:** alles **spätestens zum Ende der New-York-Session
  (16:30)** schließen — **kein Übernacht-Halten.** Läuft ein Trade am Session-Ende
  noch, wird er zum Marktpreis geschlossen (Ergebnis in R eintragen).

### 4.1 Ergebnis in R (fürs Journal)

- Stop vor TP1: **−1R**
- TP1 + Runner-BE: **+1R**
- TP1 + Runner-Ziel: `1R + 0,5 × (Runner-Distanz / R)`  (z.B. Runner 4R → **+3R**)
- FIX2R: **+2R**
- Zeit-Stop: offener Stand in R

---

## 5. Positions-Regeln

- **Maximal 1 offener Trade** gleichzeitig.
- Kein Nachlegen, kein Pyramidisieren, kein Stop-Verschieben außer dem
  vorgeschriebenen BE-Move nach TP1.
- Maximal **wenige** Trades pro Session — Qualität vor Quantität (das Setup ist
  selten; erzwinge keine Trades außerhalb der Checkliste).

---

## 6. Session-Checkliste (alles muss JA sein)

```
[ ] 1. Innerhalb London/NY-Fenster?                                   §1.1
[ ] 2. Gültiger Impuls? (≥ 2×ATR  UND  ≤ 10 Kerzen  UND  BOS)          §2.2
[ ] 3. Fib über jüngsten Impuls, 0.5 berechnet?                       §2.3
[ ] 4. Frischer OB (noch nie angetappt)?                              §2.4/2.5
[ ] 5. Liegt die 0.5 INNERHALB der OB-Zone?                           §3.1
[ ] 6. Runner-Ziel (EQH/EQL oder Fib-Ext) ≥ 3R entfernt?             §4
[ ] 7. Gerade KEIN Trade offen?                                       §5

Alle JA → Limit an OB-Kante, Stop hinter OB, 1 % Risiko, TP1 +2R (→BE), Runner.
Ein NEIN → kein Trade. Punkt 6 NEIN → nur fix +2R (kein Runner).
```

---

## 7. Die einzigen einstellbaren Schrauben (später, einzeln testen)

Zuerst **immer** mit diesen Defaults. Dann **eine** Schraube auf einmal.

| Schraube            | Default        | Alternativen              |
|---------------------|----------------|---------------------------|
| Arbeits-Timeframe   | 15m            | 5m / 30m                  |
| Impuls-Größe        | 2,0 × ATR      | 1,5× / 2,5×               |
| Impuls-Tempo        | ≤ 10 Kerzen    | ≤ 6 / ≤ 15                |
| Fib-Entry-Level     | 0.5            | 0.618 / 0.705             |
| Stop-Puffer         | 0,1 × ATR      | 0,05× / 0,2×              |
| TP1                 | 2R             | 1,5R / 3R                 |
| Teilgewinn-Anteil   | 50 %           | 33 % / 66 %               |
| Runner-Mindestziel  | 3R             | 2,5R / 4R                 |
| Session-Fenster     | London + NY    | nur NY / nur London       |

Alles andere bleibt fix.

---

## 8. Unterschiede zur Swing-Version (FX)

Die **Logik ist identisch** zur Swing-Fib-OB-Idee — nur:

- Timeframe **15m** statt 4H (mehr, kleinere Setups).
- **Session-Filter** (London/NY) statt rund um die Uhr.
- **Intraday-Zeit-Stop** (kein Übernacht) statt 10-Tage-Halten.
- Limit-Gültigkeit **10 Kerzen** statt 20.

Erst wenn der Backtest (`BACKTEST.md`) über einen langen Zeitraum stabil positiv
ist (bei erträglichem Drawdown) → Demo-Forward → danach echtes Geld.
