# Gold Fib-OB Swing Continuation — Regelwerk

> Ziel: Eine Swing-Strategie, bei der **jede** Entscheidung eine Zahl aus dem
> Chart ist. Kein Augenmaß, kein "sieht aus wie", kein diskretionäres Fib.
> Zwei Leute mit denselben Daten kommen zu **identischen** Trades.
>
> Diese Datei ist die einzige Wahrheit. Steht eine Situation hier nicht drin,
> wird **nicht** gehandelt.

---

## 0. Kernidee (in einem Satz)

Nach einer starken Impulsbewegung zieht sich der Kurs zurück. Wenn das
**50 %-Retracement (Fib 0.5)** genau in einem **frischen Order Block** liegt,
steigen wir **in Richtung des Impulses** ein (Continuation) und lassen einen
Teil als **Runner** bis zur nächsten Liquidität laufen.

---

## 1. Markt & Zeitrahmen (fest)

| Punkt              | Festlegung                                              |
|--------------------|---------------------------------------------------------|
| Instrument         | **XAUUSD / Gold** (Basis-Test). Danach übertragbar.     |
| Arbeits-Timeframe  | **4H** — Impuls, Fib, OB, Entry, EQH/EQL alles auf 4H   |
| Stil               | **Swing** — Trades laufen typischerweise Tage           |
| Entscheidungstakt  | bei jedem **abgeschlossenen 4H-Close**                   |

Kein zusätzlicher Trendfilter, kein EMA. Bewusst minimal.

---

## 2. Bausteine — alle objektiv definiert

### 2.1 Swing-Punkt (5-Kerzen-Fraktal)

- **Swing-Hoch (SH):** eine Kerze, deren **Hoch** höher ist als die Hochs der
  **2 Kerzen links und 2 Kerzen rechts** davon.
- **Swing-Tief (ST):** Spiegelbild (Tief tiefer als die 2 links und 2 rechts).

> Ein Fraktal ist erst **bestätigt**, wenn die 2 Kerzen rechts geschlossen sind.
> Vorher zählt es nicht. (Kein Vorgriff.)

### 2.2 Impuls (das Fib-Fundament)

Eine Bewegung zählt als **gültiger Impuls**, wenn **alle 3** Bedingungen erfüllt
sind (Beispiel: Abwärts-Impuls von SH zu ST):

1. **Größe:** Distanz `SH_Hoch − ST_Tief` ≥ **2,0 × ATR(14)** (ATR auf 4H).
2. **Tempo:** vom SH bis zum ST liegen **≤ 10 Kerzen**.
3. **Struktur-Bruch (BOS):** das ST bricht **unter** das vorherige bestätigte
   Swing-Tief (macht ein neues tieferes Tief).

Aufwärts-Impuls = Spiegelbild (ST → SH, ≥ 2 ATR, ≤ 10 Kerzen, bricht das
vorherige Swing-Hoch).

> Gibt es mehrere gültige Impulse gleichzeitig → nimm den **jüngsten**
> (zuletzt abgeschlossenen). Nie einen älteren "nachträglich" auswählen.

### 2.3 Fibonacci

Direkt über den gültigen Impuls gelegt:

- Abwärts-Impuls: **0 = SH_Hoch**, **1 = ST_Tief**.
- Aufwärts-Impuls: **0 = ST_Tief**, **1 = SH_Hoch**.
- **0.5 = genau die Mitte:** `(0-Level + 1-Level) / 2`.

### 2.4 Order Block (OB)

- **Bearisher OB** (für Shorts, Abwärts-Impuls): die **letzte Kerze mit
  bullischem Close** (Close > Open) **direkt vor** dem Start des Abwärts-Impuls.
- **Bullischer OB** (für Longs): die **letzte Kerze mit bärischem Close**
  (Close < Open) direkt vor dem Start des Aufwärts-Impuls.
- **Zone = die ganze Kerze: von ihrem Hoch bis zu ihrem Tief** (High–Low).

### 2.5 "Frisch" (unmitigiert)

Der OB ist **frisch**, wenn seit seiner Entstehung **keine** Kerze in die Zone
(High–Low) hineingelaufen ist — der aktuelle Retracement ist der **erste** Tap.
War die Zone vorher schon einmal berührt → **verbraucht → kein Trade.**

### 2.6 EQH/EQL (Liquidität)

Die Level des Indikators **"EQH/EQL D.A.T"** (feste Einstellungen, damit
reproduzierbar) definieren die Liquiditäts-Pools. Rolle hier: **Ziel für den
Runner** (siehe §4).

---

## 3. Einstieg (Trigger + Ausführung)

### 3.1 Die Confluence-Bedingung (Ja/Nein)

**Der Trade ist nur gültig, wenn die 0.5 innerhalb der frischen OB-Zone liegt:**

```
OB_Tief ≤ Fib-0.5-Preis ≤ OB_Hoch     UND     OB ist frisch (§2.5)
```

Ist das nicht der Fall → **kein Trade.**

### 3.2 Entry, Stop, R

- **Entry = Limit-Order an der näheren OB-Kante (proximal):**
  - Short (Abwärts-Impuls, Kurs läuft von unten hoch): Limit am **OB-Tief**.
  - Long (Aufwärts-Impuls, Kurs läuft von oben runter): Limit am **OB-Hoch**.
- **Stop = hinter der fernen OB-Kante (distal) + Puffer 0,1 × ATR(14):**
  - Short: Stop = **OB-Hoch + 0,1 × ATR**.
  - Long: Stop = **OB-Tief − 0,1 × ATR**.
- **R (Risiko-Einheit) = | Entry − Stop |.**
- **Positionsgröße:** so, dass der Verlust bei Stop = **1 % des Kontos** ist.

### 3.3 Gültigkeit der Limit-Order

Die Order verfällt (nicht gehandelt), wenn **vor** dem Fill eines eintritt:

1. Der Kurs macht ein **neues Extrem jenseits Fib 1.0** (Impuls verlängert sich,
   Setup veraltet), **oder**
2. **20 Kerzen** vergehen ohne Fill.

---

## 4. Ausstieg — Teilgewinn + Runner (2-teilig, objektiv)

Position wird **50 / 50** geteilt.

| Teil        | Regel                                                                 |
|-------------|-----------------------------------------------------------------------|
| **TP1 (50 %)** | bei **+2R** schließen. Gleichzeitig Stop des Rests auf **Break-Even** (Entry). |
| **Runner (50 %)** | Ziel = **nächster gegenüberliegender EQH/EQL-Pool in Impuls-Richtung** (Short → nächster EQL darunter; Long → nächster EQH darüber). |

**Runner-Fallback:** existiert kein solcher EQH/EQL-Pool → Runner-Ziel =
**Fib-Extension −1.0** (Impuls um 100 % über sein Ende hinaus projiziert).

**Gültigkeits-Check fürs Ziel:** das Runner-Ziel muss **≥ 3R** vom Entry
entfernt sein. Ist die nächste Liquidität **< 3R** entfernt → **kein Runner**:
dann wird die **volle** Position bei **+2R** geschlossen (degeneriert zu fix 2R).

**Weitere feste Exit-Regeln:**
- Wird der **Stop** vor TP1 getroffen → ganze Position −1R. Fertig.
- Nach TP1 kann der Runner nur noch **+Runner-Gewinn** oder **Break-Even (0)**
  ergeben — nie wieder Verlust.
- **Zeit-Stop:** spätestens nach **10 Handelstagen** alles schließen.

### 4.1 Ergebnis in R (fürs Journal)

- Stop vor TP1: **−1R**
- TP1 + Runner-BE: `0,5 × 2R + 0,5 × 0 =` **+1R**
- TP1 + Runner-Ziel: `0,5 × 2R + 0,5 × (Runner-Distanz / R)`
  - Beispiel Runner bei 4R: `1R + 0,5 × 4R =` **+3R**

---

## 5. Positions-Regeln

- **Maximal 1 offener Trade** gleichzeitig. Erst wenn der geschlossen ist, zählt
  das nächste Setup.
- Kein Nachlegen, kein Pyramidisieren, kein Stop-Verschieben außer den
  vorgeschriebenen BE-Move nach TP1.

---

## 6. Wöchentliche/tägliche Checkliste (alles muss JA sein)

```
[ ] 1. Gültiger Impuls? (≥ 2×ATR  UND  ≤ 10 Kerzen  UND  BOS)          §2.2
[ ] 2. Fib über den jüngsten Impuls gezogen, 0.5 berechnet?            §2.3
[ ] 3. Frischer OB vorhanden (noch nie angetappt)?                     §2.4/2.5
[ ] 4. Liegt die 0.5 INNERHALB der OB-Zone?                            §3.1
[ ] 5. Runner-Ziel (EQH/EQL oder Fib-Ext) ≥ 3R entfernt?              §4
[ ] 6. Gerade KEIN Trade offen?                                        §5

Alle JA → Limit an OB-Kante, Stop hinter OB, 1 % Risiko, TP1 +2R (→BE), Runner.
Ein NEIN → kein Trade. Punkt 5 NEIN → nur fix +2R (kein Runner).
```

---

## 7. Die einzigen einstellbaren Schrauben (später, einzeln testen)

Zuerst **immer** mit diesen Defaults backtesten. Erst danach **eine** Schraube
auf einmal ändern — nie mehrere gleichzeitig (sonst Kurven-Anpassung).

| Schraube            | Default   | Alternativen        |
|---------------------|-----------|---------------------|
| Impuls-Größe        | 2,0 × ATR | 1,5× / 2,5×         |
| Impuls-Tempo        | ≤ 10 Kerzen | ≤ 6 / ≤ 15        |
| Fib-Entry-Level     | 0.5       | 0.618 / 0.705       |
| Stop-Puffer         | 0,1 × ATR | 0,05× / 0,2×        |
| TP1                 | 2R        | 1,5R / 3R           |
| Teilgewinn-Anteil   | 50 %      | 33 % / 66 %         |
| Runner-Mindestziel  | 3R        | 2,5R / 4R           |

Alles andere bleibt fix.

---

## 8. Was diese Strategie NICHT ist

- Kein Signal-Dienst. Du liest die Zahlen selbst ab.
- Kein diskretionäres Fib: der Impuls ist über §2.2 **eindeutig** bestimmt —
  du "suchst" dir keinen Swing aus.
- Kein "gutes Gefühl". Nur die Checkliste zählt.

Erst wenn der Backtest (`BACKTEST.md`) über einen langen Zeitraum eine stabile,
positive Erwartung mit erträglichem Drawdown zeigt → Demo-Forward-Test → danach
echtes Geld.
