# FX Relative-Strength Swing Rotation — Regelwerk

> Ziel: Eine Swing-Strategie, bei der **jede** Entscheidung eine Zahl aus dem
> Chart ist. Keine Chartformen, kein Augenmaß, kein "sieht aus wie". Wenn zwei
> Leute dasselbe Regelwerk mit denselben Daten anwenden, kommen sie zu
> **identischen** Trades. Das ist die Definition von idiotensicher.
>
> Diese Datei ist die einzige Wahrheit. Wenn eine Situation hier nicht steht,
> wird **nicht** gehandelt.

---

## 0. Kernidee (in einem Satz)

Währungen bewegen sich gegeneinander in Trends. Wir messen jede Woche rein
rechnerisch, welche der 8 Hauptwährungen am **stärksten** und welche am
**schwächsten** ist, und handeln genau das Paar zwischen diesen beiden — long
die starke, short die schwache. Fertig.

---

## 1. Universum (fest, wird nie geändert)

**8 Währungen:** USD, EUR, GBP, JPY, AUD, NZD, CAD, CHF

**7 Mess-Paare** (das sind die einzigen Charts, die du zum Ranken brauchst):

| # | Paar    | Misst die Stärke von | Vorzeichen der % -Änderung |
|---|---------|----------------------|-----------------------------|
| 1 | EURUSD  | EUR                  | **+** (unverändert)         |
| 2 | GBPUSD  | GBP                  | **+**                       |
| 3 | AUDUSD  | AUD                  | **+**                       |
| 4 | NZDUSD  | NZD                  | **+**                       |
| 5 | USDJPY  | JPY                  | **−** (umkehren)            |
| 6 | USDCHF  | CHF                  | **−**                       |
| 7 | USDCAD  | CAD                  | **−**                       |

> Warum das Vorzeichen? Bei EURUSD bedeutet "+2%", dass EUR **stärker** wurde.
> Bei USDJPY bedeutet "+2%", dass USD stärker und damit JPY **schwächer** wurde
> — deshalb drehen wir das Vorzeichen um, damit "+" immer "diese Währung wird
> stärker" heißt.

Die **8. Währung ist USD** und wird nicht direkt gemessen, sondern berechnet
(siehe 3.2).

---

## 2. Zeitrahmen & Rhythmus (fest)

| Zweck                     | Timeframe | Wann                                             |
|---------------------------|-----------|--------------------------------------------------|
| Stärke messen & ranken    | **Daily** | 1× pro Woche, am **Montag beim Wochenopen**      |
| Trendfilter               | **Daily** | gleicher Moment                                  |
| Einstieg ausführen        | **4H**    | Open der **ersten 4H-Kerze** der Handelswoche    |
| Trade-Management          | —         | wieder am nächsten Montag                        |

- **Entscheidungszeitpunkt = einmal pro Woche, Montag beim Open.** Nicht öfter.
  Kein Reinschauen unter der Woche außer zum Prüfen von Stop/Target.
- Zum Ranken werden immer die **letzten abgeschlossenen** Daily-Kerzen benutzt
  (also der Stand von Freitag-Close).

---

## 3. Der Stärke-Score (das objektive Herzstück)

### 3.1 Roh-Werte ablesen — 7 Zahlen

Lookback = **20 Handelstage** (≈ 1 Monat).

Für jedes der 7 Mess-Paare den **20-Tage-Return** ablesen:

```
Return_20 = (Close_heute − Close_vor_20_Tagen) / Close_vor_20_Tagen × 100
```

In TradingView am einfachsten mit dem Indikator **ROC (Rate of Change),
Länge = 20**, auf dem Daily. Der ROC-Wert auf der letzten abgeschlossenen
Kerze (Freitag) ist die gesuchte Zahl.

### 3.2 In Währungsstärke umrechnen — 8 Zahlen

```
Stärke(EUR) = +ROC20(EURUSD)
Stärke(GBP) = +ROC20(GBPUSD)
Stärke(AUD) = +ROC20(AUDUSD)
Stärke(NZD) = +ROC20(NZDUSD)
Stärke(JPY) = −ROC20(USDJPY)
Stärke(CHF) = −ROC20(USDCHF)
Stärke(CAD) = −ROC20(USDCAD)
Stärke(USD) = − (Mittelwert der 7 Werte oben)
```

> USD ist stark, wenn alle anderen gegen USD schwach sind — deshalb der
> negierte Durchschnitt.

### 3.3 Ranken

Sortiere die 8 Stärke-Werte:

- **Rang 1** = größter Wert = **stärkste** Währung
- **Rang 8** = kleinster Wert = **schwächste** Währung

Das ist die komplette "Confluence". Eine Rangliste aus Zahlen. Nichts zu
interpretieren.

---

## 4. Paar-Auswahl (eindeutig)

1. Nimm die **Rang-1-Währung** (stark) und die **Rang-8-Währung** (schwach).
2. Bilde daraus das Standard-Paar (z. B. Rang-1 = EUR, Rang-8 = JPY → **EURJPY**).
3. Richtung:
   - Ist die **starke** Währung die **Basis** (erste im Symbol) → **BUY**.
   - Ist die **starke** Währung der **Quote** (zweite im Symbol) → **SELL**.

**Beispiel A:** stark = EUR, schwach = JPY → Symbol EURJPY, EUR ist Basis → **BUY EURJPY**.
**Beispiel B:** stark = JPY, schwach = EUR → Symbol EURJPY, JPY ist Quote → **SELL EURJPY**.

> Egal wie du es drehst: Du bist immer **long die starke** und **short die
> schwache** Währung.

---

## 5. Einstiegsfilter (ein einziger, Ja/Nein)

Öffne das ausgewählte Paar im **Daily** mit einer **50-SMA**:

- **BUY** nur erlaubt, wenn Daily-Close **> 50-SMA**.
- **SELL** nur erlaubt, wenn Daily-Close **< 50-SMA**.

Wenn der Filter der Ranking-Richtung **widerspricht** → **kein Trade diese
Woche.** (Die Rangliste sagt "stark", aber der Preis ist noch nicht im Trend —
wir warten.)

**Ausführung:** Filter bestanden → Einstieg zum **Open der ersten 4H-Kerze**
der Handelswoche. Marktorder. Kein Warten auf Pullbacks, keine Muster.

---

## 6. Risiko & Ausstieg (feste Zahlen)

| Größe            | Regel                                                      |
|------------------|------------------------------------------------------------|
| ATR              | **ATR(14)** auf dem **Daily**, abgelesen am Einstiegstag   |
| Stop-Loss        | Einstieg **∓ 1,5 × ATR(14)** (unter Einstieg bei BUY, darüber bei SELL) |
| Risiko pro Trade | **1 %** des Kontos                                          |
| Positionsgröße   | (1 % × Konto) ÷ (Stop-Abstand in Pips × Pip-Wert)          |
| Take-Profit      | **+2R** (fix 1:2 — R = Stop-Abstand)                       |

**Ausstiegs-Reihenfolge (was zuerst passiert, zählt):**

1. **Stop-Loss** getroffen → Trade zu, Ergebnis = **−1R**.
2. **Take-Profit** getroffen → Trade zu, Ergebnis = **+2R**.
3. **Rotations-Exit** (geprüft nur am nächsten Montag): Wenn weder Stop noch TP
   getroffen wurde **und** das Paar nicht mehr Rang-1-gegen-Rang-8 ist —
   konkret: die starke Währung ist aus **Rang 1–2** gefallen **oder** die
   schwache Währung ist aus **Rang 7–8** gestiegen → Ausstieg zum **Open der
   ersten 4H-Kerze**. Ergebnis = aktueller offener Gewinn/Verlust in R.
4. **Zeit-Stop:** Spätestens nach **10 Handelstagen** schließen, egal was ist.

---

## 7. Positions-Regeln

- **Maximal 1 offener Trade** gleichzeitig. Ein Trade-Signal pro Woche.
- **Kein** Nachkaufen, **kein** Pyramidisieren, **kein** Verschieben des Stops
  (außer der Trade wird komplett geschlossen).
- Ist bereits ein Trade offen → diese Woche **nicht** neu einsteigen, nur
  managen (Punkt 6).

---

## 8. Die wöchentliche Checkliste (alles muss JA sein)

```
[ ] 1. Ist es der feste Entscheidungszeitpunkt (Montag-Open)?
[ ] 2. Stärke-Sheet ausgefüllt → eindeutige Rang-1 und Rang-8 (kein Gleichstand)?
[ ] 3. Stimmt die 50-SMA des Paares mit der Richtung überein?
[ ] 4. Ist gerade KEIN Trade offen?

Alle 4 = JA  → Einstieg zum nächsten 4H-Open, Stop 1,5×ATR, Ziel +2R, Risiko 1 %.
Ein NEIN     → kein neuer Trade. (Bei offenem Trade: nur Punkt 6 anwenden.)
```

Bei Gleichstand im Ranking (zwei Währungen exakt gleicher Wert): **kein Trade.**
Kein Losentscheid, keine Interpretation.

---

## 9. Die einzigen einstellbaren Schrauben (zum späteren Testen)

Beim Backtest **zuerst mit genau diesen Defaults** testen. Erst danach EINE
Schraube auf einmal variieren — niemals mehrere gleichzeitig (sonst weißt du
nie, was gewirkt hat = Kurven-Anpassung).

| Schraube            | Default | Alternativen zum Testen |
|---------------------|---------|-------------------------|
| Lookback            | 20 Tage | 10 / 40                 |
| Stop-Multiplikator  | 1,5×ATR | 1,0× / 2,0×             |
| Take-Profit         | +2R     | +3R / nur Rotations-Exit|
| SMA-Filter-Länge    | 50      | 20 / 100 / kein Filter  |

**Alles andere bleibt fix.** Nicht anfassen.

---

## 10. Was diese Strategie NICHT ist

- Kein Signal-Dienst. Niemand sagt dir "kauf jetzt". Du liest die Zahlen ab.
- Keine Intraday-Strategie. Entscheidungen fallen 1× pro Woche.
- Keine diskretionäre Strategie. Wenn du "ein gutes Gefühl" bei einem anderen
  Paar hast — irrelevant. Es zählt nur die Rangliste.

Erst wenn der Backtest (siehe `BACKTEST.md`) über einen langen Zeitraum eine
stabile positive Erwartung zeigt, wird die Strategie mit echtem Geld gehandelt.
