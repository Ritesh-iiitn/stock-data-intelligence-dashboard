# Stock Data Intelligence Dashboard 📈

A production-ready financial data platform that collects, processes, analyzes, and visualizes stock data. Built as a full-stack dashboard demonstrating modern python engineering and dynamic aesthetics.

## ✨ Features

- **Real-Time Data Collection**: Fetches market data dynamically using `yfinance`.
- **Advanced Processing**: Powered by `Pandas` and `NumPy`.
  - Calculates 7-day Moving Averages.
  - Computes 52-week High/Low.
  - Generates Daily Returns margins.
- **Custom Intelligence (Machine Learning)**: 
  - Implementation of **Linear Regression** to calculate a prediction trendline for the current 30-day view window.
  - **Volatility Calculation** via statistical standard deviation.
  - **Stock Comparison Engine** computing Returns, Volatility, and target cross-Correlation between stocks.
- **Async Robust REST API**: Fast, non-blocking asynchronous Python endpoints.
- **High-End UI Dashboard**: High aesthetics, glassmorphism-inspired user interface with robust implementations of `Chart.js`.

## ⚙️ Tech Stack

- **Backend**: Python 3.9+, FastAPI, Uvicorn
- **Data Engineering**: Pandas, NumPy, Scikit-Learn
- **Data Source**: Yahoo Finance API (`yfinance`)
- **Frontend**: HTML5, Vanilla Modern CSS3, JavaScript, Chart.js

## 🚀 Setup & Deployment Instructions

1. **Clone/Navigate to Project**
   ```bash
   cd stock-dashboard
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server Locally**
   ```bash
   uvicorn main:app --reload
   ```

5. **View Dashboard**
   Open your browser to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🐳 Docker Support (Advanced Feature)

You can easily containerize and run the platform without setting up Python locally.

```bash
docker build -t stock-dash .
docker run -p 8000:8000 stock-dash
```

## 📡 API Endpoints Architecture

- `GET /companies`: Returns listing array of supported companies.
- `GET /data/{symbol}?days=30`: Returns detailed stock performance data (`Close`, `Averages`, `Prediction Trend`) in JSON format.
- `GET /summary/{symbol}`: Returns core metrics (52-week high/low, base average view) for given symbol.
- `GET /compare?symbol1={sym1}&symbol2={sym2}`: **(Bonus API)** Exposes statistical correlation, analyzing the paired movement ratio of two individual equities.
