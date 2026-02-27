"""Generate sample data for Realweb Camp Analytics."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n = 500
start = datetime(2019, 1, 1)
dates = [start + timedelta(days=i % 365) for i in range(n)]

df = pd.DataFrame({
    'date': dates,
    'medium': np.random.choice(['cpc', 'organic', 'referral', 'email'], n),
    'revenue': np.random.exponential(100, n),
    'transaction_value': np.random.uniform(50, 500, n),
    'promo_activated': np.random.choice([0, 1], n, p=[0.7, 0.3]),
    'conversion': np.random.binomial(1, 0.02, n),
})

df.to_csv('data.csv', index=False)
print('Created data.csv with', len(df), 'rows')
