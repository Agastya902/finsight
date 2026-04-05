# FinSight

**Explainable Fintech Portfolio Intelligence**

FinSight is a streamlined MVP web application designed to demonstrate financial data analysis, strategy backtesting, portfolio optimization, and plain-English insights. It transforms complex quantitative results into explainable summaries, catering to financial analysts, fintech product teams, technical sales, and client-facing demonstrations.

## Key Features

- **Stock Analytics**: Dive deep into standard metrics like annualized return, volatility, max drawdown, and moving averages.
- **Strategy Backtesting**: Compare classical strategies like Moving Average Crossover against Buy and Hold and benchmark indices (e.g., SPY).
- **Portfolio Optimization**: Allocate capital effectively using scipy.optimize algorithms to find the Maximum Sharpe or Minimum Volatility portfolios among user-selected assets.
- **Explainable Summaries**: An intelligent rule-based engine that instantly distills the outcomes of charting and optimization into clean, professional, reading-ready English interpretations.

## Tech Stack

- **Language**: Python
- **Frontend**: Streamlit
- **Data & Computation**: Pandas, NumPy, yfinance
- **Optimization**: SciPy
- **Visualization**: Plotly

## Screenshots

<!-- Note: Add screenshots of Overview, Analytics, Backtesting, and Optimization here -->
*(Screenshots coming soon)*

## Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd finsight
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Deployment Instructions (Streamlit Community Cloud)

1. Push your code to a public GitHub repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io).
3. Click "New app".
4. Select the repository, branch (`main`), and main file path (`app.py`).
5. Click "Deploy". The app will automatically install dependencies from `requirements.txt` and launch.

## Future Improvements
- **Live Data**: Hook up to live websockets for real-time pricing.
- **User Portfolios**: Add backend database integration (e.g., PostgreSQL or Firebase) to save user's custom created portfolios.
- **Advanced Strategies**: Expand to incorporate Mean-Reversion and Machine Learning forecasting based trading algorithms.
