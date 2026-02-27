"""Realweb Camp Analytics: Python analysis of e-commerce data."""

import pandas as pd
from scipy import stats


def load_data(path: str = 'data.csv') -> pd.DataFrame:
    """Load CSV dataset."""
    df = pd.read_csv(path)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df


def top_channel_revenue(df: pd.DataFrame) -> str:
    """a) Channel with max revenue."""
    if 'revenue' not in df.columns or 'medium' not in df.columns:
        return 'N/A'
    return df.groupby('medium')['revenue'].sum().idxmax()


def avg_check_by_promo(df: pd.DataFrame) -> dict:
    """b) Avg check before/after covid, with/without promo."""
    if 'transaction_value' not in df.columns:
        return {}
    covid_date = pd.Timestamp('2020-03-01')
    df = df.copy()
    df['period'] = df['date'].apply(lambda x: 'after' if x >= covid_date else 'before')
    if 'promo_activated' not in df.columns:
        df['promo_activated'] = 0
    result = df.groupby(['period', 'promo_activated'])['transaction_value'].mean()
    return result.to_dict()


def cr_weekend_vs_weekday(df: pd.DataFrame) -> tuple:
    """c) CR weekend vs weekday, 95% confidence."""
    if 'date' not in df.columns or 'conversion' not in df.columns:
        return (None, None)
    df = df.copy()
    df['weekend'] = df['date'].dt.dayofweek >= 5
    w = df[df['weekend']]['conversion']
    b = df[~df['weekend']]['conversion']
    if len(w) < 2 or len(b) < 2:
        return (None, None)
    _, pval = stats.ttest_ind(w, b)
    return (pval < 0.05, float(pval))


def main():
    """Run analysis."""
    try:
        df = load_data()
    except FileNotFoundError:
        print('data.csv not found. Create sample data or download from Realweb.')
        return
    print('a) Top channel by revenue:', top_channel_revenue(df))
    print('b) Avg check by period/promo:', avg_check_by_promo(df))
    sig, p = cr_weekend_vs_weekday(df)
    print('c) CR weekend vs weekday significant (95%):', sig, 'p-value:', p)
    print('d) CPC forecast: ARIMA/Prophet + seasonality, need historical CPC data')
    print('e) Additional: cohort retention, LTV by channel')


if __name__ == '__main__':
    main()
