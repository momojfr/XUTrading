"""
XAUUSD Trading Strategy Analysis
==================================
Analyzes a personal trading journal (250+ trades) to evaluate strategy
performance, identify patterns, and quantify risk (drawdowns, win rate,
performance by year).

Author: [Your Name]
Data source: Personal trading journal exported from Notion
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. LOAD & CLEAN DATA
# ---------------------------------------------------------------------------

GERMAN_MONTHS = {
    'Januar': 'January', 'Februar': 'February', 'März': 'March', 'April': 'April',
    'Mai': 'May', 'Juni': 'June', 'Juli': 'July', 'August': 'August',
    'September': 'September', 'Oktober': 'October', 'November': 'November',
    'Dezember': 'December'
}


def load_and_clean(filepath: str) -> pd.DataFrame:
    """Load raw journal export and return a cleaned DataFrame of valid trades."""
    df = pd.read_csv(filepath, encoding='utf-8-sig')

    # Keep only trades with a definitive win/loss outcome
    # (drops empty rows and trades marked as rule violations)
    df = df[df['TP?-2RR'].isin(['Yes', 'No'])].copy()

    # Parse German-language timestamps, e.g. "8. Mai 2025 22:00 (GMT+7)"
    datum = df['Datum'].str.replace(r'\s*\(GMT.*\)', '', regex=True)
    for de, en in GERMAN_MONTHS.items():
        datum = datum.str.replace(de, en, regex=False)
    df['date'] = pd.to_datetime(datum, format='%d. %B %Y %H:%M', errors='coerce')

    # Only keep rows where the parsed year matches the journal's own "Jahr" field
    # (guards against occasional data-entry / parsing mismatches)
    df = df[df['date'].dt.year == df['Jahr']]

    df = df.sort_values('date').reset_index(drop=True)

    # Simple fixed-R outcome model: win = +2R, loss = -1R
    df['pnl_r'] = df['TP?-2RR'].map({'Yes': 2, 'No': -1})
    df['equity'] = df['pnl_r'].cumsum()

    return df


# ---------------------------------------------------------------------------
# 2. METRICS
# ---------------------------------------------------------------------------

def win_rate(df: pd.DataFrame) -> float:
    return (df['TP?-2RR'] == 'Yes').mean() * 100


def win_rate_by_group(df: pd.DataFrame, column: str) -> pd.Series:
    return df.groupby(column)['TP?-2RR'].apply(lambda x: (x == 'Yes').mean() * 100).round(1)


def max_drawdown(df: pd.DataFrame) -> tuple[float, pd.Timestamp]:
    """Returns the largest peak-to-trough drawdown (in R) and when it occurred."""
    running_max = df['equity'].cummax()
    drawdown = df['equity'] - running_max
    worst_idx = drawdown.idxmin()
    return drawdown.min(), df.loc[worst_idx, 'date']


# ---------------------------------------------------------------------------
# 3. PLOTS
# ---------------------------------------------------------------------------

def plot_equity_curve(df: pd.DataFrame, save_path: str = None):
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['equity'])
    plt.axhline(0, color='red', linestyle='--', linewidth=0.8)
    plt.title('Equity Curve (Win = +2R, Loss = -1R)')
    plt.xlabel('Date')
    plt.ylabel('Cumulative R')
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()


def plot_equity_by_year(df: pd.DataFrame, save_path: str = None):
    plt.figure(figsize=(12, 6))
    for year in sorted(df['Jahr'].unique()):
        sub = df[df['Jahr'] == year]
        plt.plot(sub['date'], sub['pnl_r'].cumsum(), label=year)
    plt.title('Equity Curve by Year (each starting at 0)')
    plt.xlabel('Date')
    plt.ylabel('Cumulative R')
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()


# ---------------------------------------------------------------------------
# 4. MAIN
# ---------------------------------------------------------------------------

def main():
    df = load_and_clean('data/trades.csv')

    print(f"Total valid trades: {len(df)}")
    print(f"Overall win rate: {win_rate(df):.1f}%")

    print("\nWin rate by year:")
    print(win_rate_by_group(df, 'Jahr'))

    print("\nWin rate by direction (Long/Short):")
    print(win_rate_by_group(df, 'L/S'))

    dd, dd_date = max_drawdown(df)
    print(f"\nMax drawdown: {dd:.1f}R (on {dd_date.date()})")

    plot_equity_curve(df, save_path='equity_curve.png')
    plot_equity_by_year(df, save_path='equity_by_year.png')


if __name__ == '__main__':
    main()
