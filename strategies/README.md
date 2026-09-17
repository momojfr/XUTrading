# Trading-Strategien

Zwei getrennte, vollständig objektive Strategien. Jede Regel ist ein Ja/Nein aus
Kursdaten — kein Augenmaß, kein diskretionäres Fib. Beide werden **manuell im
TradingView-Replay** backtestet (kein Code, keine Live-Signale).

| Ordner | Strategie | Markt | Stil | Timeframe |
|--------|-----------|-------|------|-----------|
| [`swing_fx_relative_strength/`](swing_fx_relative_strength/) | Relative-Strength Rotation | FX (8 Majors / 28 Paare) | Swing (Tage) | Daily-Ranking, 4H-Entry |
| [`scalping_gold_fib_ob/`](scalping_gold_fib_ob/) | Fib-0.5-in-frischem-Order-Block Continuation | Gold (XAUUSD) | Scalping (intraday) | 15m |

Jeder Ordner enthält:

- **`STRATEGY.md`** — das komplette Regelwerk (die einzige Wahrheit).
- **`BACKTEST.md`** — Schritt-für-Schritt manueller Backtest-Plan.
- **`journal_*.csv`** — Journal-Vorlage (in Google Sheets / Excel importieren,
  Formeln laut `BACKTEST.md` einfügen).

## Vorgehen für beide

1. Erst mit den **Default-Parametern** backtesten — nichts anfassen.
2. Ab **≥ 50 Trades** auswerten (Winrate, Ø R, Profit-Faktor, Max-Drawdown).
3. Danach **eine** Schraube auf einmal testen (Out-of-Sample bestätigen).
4. Backtest + Out-of-Sample + Demo-Forward-Test → erst dann echtes Geld.
