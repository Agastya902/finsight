# FinSight Platform

**Institutional Explainable Portfolio Intelligence**

FinSight is a premium analytical SaaS MVP designed for wealth managers, fintech operators, and quantitative product teams. It bridges the gap between mathematically rigorous modeling (MPT, Backtesting) and beautifully rendered, client-ready plain English explainability.

![FinSight Architecture](https://img.shields.io/badge/Architecture-Modular-blue) ![Fintech](https://img.shields.io/badge/Domain-Fintech-green) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit_Dark_Mode-red)

## Live Demo
> **[Place link to Streamlit Community Cloud demo here]**

## Platform Capabilities

- **Institutional Micro-Analytics**: Extract and normalize critical financial vectors (Sharpe, Drawdown, Volatility Profiles) with robust fallback handling against Yahoo Finance endpoints.
- **Algorithmic Strategy Backtesting**: Effortlessly run performance comparisons between traditional buy-and-hold methodologies and dynamic Moving Average cross strategies.
- **MPT Constraint Solving**: Dynamically optimize highly-concentrated portfolios utilizing SciPy SLSQP optimization against Max Sharpe or Min Volatility manifolds.
- **Automated Explainability Engine**: Translates highly complex multidimensional market data and volatility metrics into reading-ready analyst commentary suitable for immediate presentation to C-Suite or high-net-worth clients.
- **Research Report Export**: Generate and download professional PDF, HTML, and CSV research reports with automated executive summaries and key performance indicators.
- **Premium Design System**: Injected CSS and heavily modified Plotly interfaces creating a sleek, dark-mode 'Bloomberg Terminal meets modern web' aesthetic.

## Tech Stack
- **Compute Layer**: `Python 3`, `NumPy`, `SciPy`
- **Analytics & Tensors**: `Pandas`, `yfinance`
- **Visualization**: `Plotly` (Extensively Customized Template)
- **Frontend Container**: `Streamlit` (with explicit CSS injection for premium product design styling)

---

## Technical Preview

*(Take screenshots of the glassmorphic cards and dark mode charts and place them here)*
- `docs/landing.jpg`
- `docs/analytics.jpg`
- `docs/optimizer.jpg`

## Local Setup & Deployment

1. **Clone & Virtualize**
```bash
git clone <repo-url> finsight
cd finsight
python3 -m venv .venv
source .venv/bin/activate
```

2. **Hydrate Dependencies**
```bash
pip install -r requirements.txt
```

3. **Ignite the Application**
```bash
streamlit run app.py
```

## Streamlit Cloud Deployment
This product is completely ready for one-click deployment via Streamlit Community Cloud. 
1. Link your public GitHub repository containing this exact folder structure to Streamlit.
2. Select target main path `app.py`.
3. Launch! The engine intrinsically loads dependencies defined in `requirements.txt`.

## Future Roadmap
- Implementation of Kelly Criterion sizing tools.
- PostgreSQL connector for saving user configuration states.
- Addition of Mean Reversion ML predictions utilizing Scikit-learn regressors on recent price horizons.
