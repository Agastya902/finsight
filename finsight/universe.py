# Pre-defined institutional dictionaries for Autocomplete dropdowns
# Maps Display Name -> Ticker Symbol

BENCHMARK_PRESETS = {
    "S&P 500 (SPY)": "SPY",
    "NASDAQ 100 (QQQ)": "QQQ",
    "Total Market (VTI)": "VTI",
    "Dow Jones Industrial (DIA)": "DIA",
    "Russell 2000 (IWM)": "IWM",
    "Custom (Type your own)": "CUSTOM"
}

# Condensed top-tier equities for autocomplete. 
# Users can still type custom tickers.
EQUITY_UNIVERSE = {
    "Apple Inc. (AAPL)": "AAPL",
    "Microsoft Corp. (MSFT)": "MSFT",
    "Alphabet Inc. Class A (GOOGL)": "GOOGL",
    "Amazon.com Inc. (AMZN)": "AMZN",
    "NVIDIA Corp. (NVDA)": "NVDA",
    "Meta Platforms Inc. (META)": "META",
    "Tesla Inc. (TSLA)": "TSLA",
    "Berkshire Hathaway Inc. (BRK-B)": "BRK-B",
    "JPMorgan Chase & Co. (JPM)": "JPM",
    "Johnson & Johnson (JNJ)": "JNJ",
    "Visa Inc. (V)": "V",
    "UnitedHealth Group (UNH)": "UNH",
    "Procter & Gamble Co. (PG)": "PG",
    "Mastercard Inc. (MA)": "MA",
    "Exxon Mobil Corp. (XOM)": "XOM",
    "Home Depot Inc. (HD)": "HD",
    "Chevron Corp. (CVX)": "CVX",
    "Eli Lilly and Co. (LLY)": "LLY",
    "AbbVie Inc. (ABBV)": "ABBV",
    "Broadcom Inc. (AVGO)": "AVGO",
    "Merck & Co. (MRK)": "MRK",
    "PepsiCo Inc. (PEP)": "PEP",
    "Coca-Cola Co. (KO)": "KO",
    "Pfizer Inc. (PFE)": "PFE",
    "Costco Wholesale Corp. (COST)": "COST",
    "Bank of America Corp. (BAC)": "BAC",
    "McDonald's Corp. (MCD)": "MCD",
    "Salesforce Inc. (CRM)": "CRM",
    "Cisco Systems Inc. (CSCO)": "CSCO",
    "Thermo Fisher Scientific (TMO)": "TMO",
    "Abbott Laboratories (ABT)": "ABT",
    "Walt Disney Co. (DIS)": "DIS",
    "Danaher Corp. (DHR)": "DHR",
    "Accenture plc (ACN)": "ACN",
    "Texas Instruments Inc. (TXN)": "TXN",
    "Comcast Corp. (CMCSA)": "CMCSA",
    "Verizon Communications (VZ)": "VZ",
    "NextEra Energy Inc. (NEE)": "NEE",
    "Nike Inc. (NKE)": "NKE",
    "Custom (Type your own)": "CUSTOM"
}

def extract_ticker(selection: str, mapping: dict) -> str:
    """Helper to convert the dropdown selection back to the raw ticker string."""
    return mapping.get(selection, selection.upper().strip())
