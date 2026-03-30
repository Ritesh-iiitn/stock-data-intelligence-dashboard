import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from utils import clean_dataframe, format_date_index

COMPANIES = {
    "INFY.NS": "Infosys Limited",
    "TCS.NS": "Tata Consultancy Services",
    "RELIANCE.NS": "Reliance Industries Limited",
    "HDFCBANK.NS": "HDFC Bank Limited",
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation"
}

def get_company_list():
    """Returns available companies for selection"""
    return [{"symbol": k, "name": v} for k, v in COMPANIES.items()]

def fetch_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """Fetches historical stock data via yfinance"""
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)
    if df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")
    
    # Standardize index timezone behavior
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df

def process_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates necessary business logic and metrics"""
    df = clean_dataframe(df)
    
    # Standard metrics
    df['Daily_Return'] = (df['Close'] - df['Open']) / df['Open']
    df['7_Day_MA'] = df['Close'].rolling(window=7).mean()
    df['52_Week_High'] = df['High'].rolling(window=252, min_periods=1).max()
    df['52_Week_Low'] = df['Low'].rolling(window=252, min_periods=1).min()
    
    # Custom Feature: Volatility
    df['Volatility_30d'] = df['Daily_Return'].rolling(window=30).std()
    
    # Backfill missing rolling values for subset preview
    df = df.bfill()
    return df

def get_recent_data(symbol: str, days: int = 30):
    """Get processed historical data for rendering"""
    df = fetch_stock_data(symbol, period="1y")
    df = process_stock_data(df)
    df_recent = df.tail(days).copy()
    
    # Custom Feature / Advanced Feature: ML Trend Prediction (Linear Regression)
    X = np.arange(len(df_recent)).reshape(-1, 1)
    y = df_recent['Close'].values
    model = LinearRegression()
    model.fit(X, y)
    df_recent['Prediction_Trend'] = model.predict(X)
    
    df_recent = format_date_index(df_recent)
    df_recent = df_recent.rename_axis('Date').reset_index()
    
    return df_recent.to_dict(orient='records')

def get_stock_summary(symbol: str):
    """Provides key high-level summaries for a specific stock"""
    df = fetch_stock_data(symbol, period="1y")
    high_52 = float(df['High'].max())
    low_52 = float(df['Low'].min())
    avg_close = float(df['Close'].mean())
    last_close = float(df['Close'].iloc[-1])
    
    return {
        "symbol": symbol,
        "52_week_high": round(high_52, 2),
        "52_week_low": round(low_52, 2),
        "average_close_price": round(avg_close, 2),
        "last_close_price": round(last_close, 2)
    }

def compare_stocks(symbol1: str, symbol2: str, period: str = "3mo"):
    """Bonus feature: Compares the performance of two stocks"""
    df1 = fetch_stock_data(symbol1, period=period)
    df2 = fetch_stock_data(symbol2, period=period)
    
    ret1 = (df1['Close'].iloc[-1] - df1['Close'].iloc[0]) / df1['Close'].iloc[0] * 100
    ret2 = (df2['Close'].iloc[-1] - df2['Close'].iloc[0]) / df2['Close'].iloc[0] * 100
    
    # Annualized volatility calculation
    vol1 = df1['Close'].pct_change().std() * np.sqrt(252) * 100
    vol2 = df2['Close'].pct_change().std() * np.sqrt(252) * 100
    
    # Correlation processing
    combined = pd.DataFrame({'s1': df1['Close'], 's2': df2['Close']}).dropna()
    correlation = combined['s1'].pct_change().corr(combined['s2'].pct_change())
    
    return {
        "symbol1": symbol1,
        "symbol2": symbol2,
        "period": period,
        "details": {
            symbol1: {
                "return_percent": round(float(ret1), 2),
                "annualized_volatility_percent": round(float(vol1), 2)
            },
            symbol2: {
                "return_percent": round(float(ret2), 2),
                "annualized_volatility_percent": round(float(vol2), 2)
            },
            "correlation": round(float(correlation), 2)
        }
    }

def get_top_movers():
    """Calculates top gainer and loser for the day among the tracked companies."""
    movers = []
    for symbol, name in COMPANIES.items():
        try:
            # fetch last 5 days to ensure we get at least 2 trading days
            df = fetch_stock_data(symbol, period="5d")
            if len(df) >= 2:
                last_close = df['Close'].iloc[-1]
                prev_close = df['Close'].iloc[-2]
                pct_change = ((last_close - prev_close) / prev_close) * 100
                movers.append({
                    "symbol": symbol,
                    "name": name,
                    "change_pct": round(pct_change, 2),
                    "last_price": round(last_close, 2)
                })
        except Exception:
            continue
            
    if not movers:
        return {"top_gainer": None, "top_loser": None}
        
    movers.sort(key=lambda x: x['change_pct'], reverse=True)
    return {
        "top_gainer": movers[0],
        "top_loser": movers[-1]
    }
