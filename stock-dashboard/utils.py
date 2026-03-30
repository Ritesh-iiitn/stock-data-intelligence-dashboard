import pandas as pd
import numpy as np

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans dataframe by replacing NaNs and infinity values."""
    df = df.replace([np.inf, -np.inf], np.nan)
    return df.dropna()

def format_date_index(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures index is string formatted for JSON serialization."""
    if isinstance(df.index, pd.DatetimeIndex):
        df.index = df.index.strftime('%Y-%m-%d')
    return df
