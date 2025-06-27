import datetime
from dateutil.relativedelta import relativedelta # For easier date calculations
import pandas as pd # Optional, but good for data handling
from collections import defaultdict

# --- User Portfolio Data (from your provided list) ---
# Note: For real calculations, you'd ideally also have the number of shares
# or the initial investment amount per stock.
# Assuming 'current_price' for calculation, though for historical performance
# you'd use the closing price on the *start* date of the period.
portfolio = [
    {"symbol": "CLOV", "stock": "CLOVER HEALTH INVESTMENTS CORP.", "current_price": 2.75},
    {"symbol": "PFFA", "stock": "VIRTUS INFRACAP US PFD ETF", "current_price": 20.83},
    {"symbol": "ABNB", "stock": "AIRBNB", "current_price": 133.97},
    {"symbol": "BABA", "stock": "ALIBABA GROUP", "current_price": 114.05},
    {"symbol": "FOUR", "stock": "SHIFT4 PAYMENTS", "current_price": 98.73},
    {"symbol": "CTXR", "stock": "CITIUS PHARMACEUTICALS INC.", "current_price": 1.67},
    {"symbol": "BIDU", "stock": "BAIDU INC.", "current_price": 85.73},
    {"symbol": "LGO", "stock": "LARGO RESOURCS LTD.", "current_price": 1.22},
    {"symbol": "EEMA", "stock": "MSCI EMERGING MARKETS ASIA ISHARES", "current_price": 82.74},
    {"symbol": "RTX", "stock": "RTX CORP", "current_price": 144.47},
    {"symbol": "JD", "stock": "JD COM INC", "current_price": 33.16},
    {"symbol": "NOK", "stock": "NOKIA CORP", "current_price": 5.17},
    {"symbol": "AMD", "stock": "ADVANCED MICRO DEVICES INC", "current_price": 143.94},
    {"symbol": "NXPI", "stock": "NXP SEMICONDUCTORS NV", "current_price": 218.06},
    {"symbol": "MOH", "stock": "MOLINA HELTHCARE INC", "current_price": 296.19},
    {"symbol": "NVDA", "stock": "NVIDIA CORPORATION", "current_price": 157.49},
    {"symbol": "PLD", "stock": "PROLOGIS INC", "current_price": 106.37},
    {"symbol": "QCOM", "stock": "QUALCOMM INC", "current_price": 158.94},
    {"symbol": "KXIN", "stock": "KAIXIN AUTO HOLDINGS", "current_price": 0.92},
    # Kenyan stocks - Note: Most US-based APIs won't have KES data.
    # You might need a specific Kenyan stock exchange API or manually adjust.
    {"symbol": "KEGN", "stock": "KENGEN", "current_price": 6.84, "currency": "KES"},
    {"symbol": "KPLC", "stock": "KPLC", "current_price": 11.40, "currency": "KES"},
    {"symbol": "CABL", "stock": "EAST AFRICA CABLES", "current_price": 1.00, "currency": "KES"},
    {"symbol": "UCHM", "stock": "UCHUMI", "current_price": 0.3, "currency": "KES"},
    {"symbol": "UNGA", "stock": "UNGA GROUP LTD", "current_price": 20.40, "currency": "KES"},
    {"symbol": "ORCH", "stock": "KENYA ORCHADS LTD", "current_price": 19.50, "currency": "KES"},
]

# --- Define Performance Periods ---
# This dictionary maps a period name to a function that calculates the start date.
# We'll use today's date as the "end date" for calculations.
today = datetime.date(2025, 6, 27) # Using a fixed date as per the context (June 27, 2025)

# Define periods in months for simpler calculation. Quarters will be approximated.
performance_periods = {
    "Last 3 Months (Q4)": lambda: today - relativedelta(months=3),
    "Last 6 Months (Q3-Q4)": lambda: today - relativedelta(months=6), # Approx 2 quarters
    "Last 9 Months (Q2-Q4)": lambda: today - relativedelta(months=9), # Approx 3 quarters
    "Last 12 Months (Q1-Q4)": lambda: today - relativedelta(months=12),
    "Last 18 Months": lambda: today - relativedelta(months=18),
    "Last 24 Months": lambda: today - relativedelta(months=24),
    "Last 36 Months": lambda: today - relativedelta(months=36),
}

# --- Function to fetch historical data (MOCK/PLACEHOLDER) ---
def get_historical_data(symbol, start_date, end_date):
    """
    *** IMPORTANT: This function is a MOCK and does NOT fetch real data. ***
    You need to replace this with actual API calls to a financial data provider.

    How to integrate a real API:
    1. Choose a financial data API (e.g., Alpha Vantage, Finnhub, Twelve Data, Yahoo Finance API).
    2. Sign up for an API key.
    3. Install their Python client library or make HTTP requests directly.
    4. Replace the 'return {}' block with actual API call logic.

    Example (using a hypothetical API structure):
    import requests
    API_KEY = "YOUR_API_KEY" # Replace with your actual API key
    URL_BASE = "https://www.alphavantage.co/query?" # Example for Alpha Vantage

    params = {
        "function": "TIME_SERIES_DAILY", # Or TIME_SERIES_DAILY_ADJUSTED for dividends
        "symbol": symbol,
        "outputsize": "full", # or "compact"
        "apikey": API_KEY
    }
    response = requests.get(URL_BASE, params=params)
    data = response.json()

    # Parse 'data' to extract relevant prices for start_date and end_date.
    # Data structure varies by API, but usually it's a dictionary of dates.
    # You'll need to find the closing price for the specific start_date and end_date.

    # For this mock, we'll return a fixed set of prices for demonstration.
    # In reality, you'd get daily prices and pick the one closest to your start/end date.
    """
    print(f"Fetching mock data for {symbol} from {start_date} to {end_date}")

    # MOCK DATA: Simulate different prices for different periods
    # In a real scenario, you'd get this from the API response
    if symbol == "NVDA":
        if start_date <= datetime.date(2022, 6, 27): # 36 months ago
            return {"start_price": 50.0, "end_price": 157.49}
        elif start_date <= datetime.date(2023, 6, 27): # 24 months ago
            return {"start_price": 80.0, "end_price": 157.49}
        elif start_date <= datetime.date(2024, 6, 27): # 12 months ago
            return {"start_price": 120.0, "end_price": 157.49}
        elif start_date <= datetime.date(2025, 3, 27): # 3 months ago (Q4)
            return {"start_price": 140.0, "end_price": 157.49}
        else: # Default for shorter periods if not specified
            return {"start_price": 150.0, "end_price": 157.49}
    elif symbol == "BABA":
        if start_date <= datetime.date(2022, 6, 27):
            return {"start_price": 90.0, "end_price": 114.05}
        elif start_date <= datetime.date(2023, 6, 27):
            return {"start_price": 100.0, "end_price": 114.05}
        elif start_date <= datetime.date(2024, 6, 27):
            return {"start_price": 110.0, "end_price": 114.05}
        else:
            return {"start_price": 112.0, "end_price": 114.05}
    elif symbol in ["KEGN", "KPLC", "CABL", "UCHM", "UNGA", "ORCH"]:
        # Mock for KES stocks - assume less volatility for demonstration
        if start_date <= datetime.date(2022, 6, 27):
            return {"start_price": portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"] * 0.8, "end_price": portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"]}
        else:
            return {"start_price": portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"] * 0.95, "end_price": portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"]}
    else: # Generic mock for other stocks
        if start_date <= datetime.date(2022, 6, 27):
            return {"start_price": 0.7 * portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"], "end_price": portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"]}
        elif start_date <= datetime.date(2023, 6, 27):
            return {"start_price": 0.85 * portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"], "end_price": portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"]}
        elif start_date <= datetime.date(2024, 6, 27):
            return {"start_price": 0.95 * portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"], "end_price": portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"]}
        else:
            return {"start_price": 0.98 * portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"], "end_price": portfolio[portfolio.index(next(s for s in portfolio if s["symbol"] == symbol))]["current_price"]}


# --- Analyze Stock Performance ---
individual_stock_performance = []

print(f"--- Analyzing Stock Performance (as of {today}) ---")

for stock_info in portfolio:
    symbol = stock_info["symbol"]
    stock_name = stock_info["stock"]
    current_price = stock_info["current_price"]
    currency = stock_info.get("currency", "$") # Default to $ if not specified

    stock_results = {
        "symbol": symbol,
        "stock_name": stock_name,
        "current_price": f"{current_price} {currency}",
        "performance": {}
    }

    for period_name, get_start_date_func in performance_periods.items():
        start_date = get_start_date_func()
        
        # Ensure start_date is not in the future for current mock
        if start_date > today:
            start_date = today

        # Fetch historical data (calls the MOCK function above)
        historical_data = get_historical_data(symbol, start_date, today)

        if historical_data and "start_price" in historical_data and "end_price" in historical_data:
            start_price = historical_data["start_price"]
            end_price = historical_data["end_price"] # This should ideally be today's price or closest close

            if start_price is not None and start_price > 0:
                percentage_change = ((end_price - start_price) / start_price) * 100
                stock_results["performance"][period_name] = f"{percentage_change:.2f}%"
            else:
                stock_results["performance"][period_name] = "N/A (Start price 0 or None)"
        else:
            stock_results["performance"][period_name] = "N/A (Data not found)"

    individual_stock_performance.append(stock_results)

# --- Calculate Weighted Average Portfolio Performance (Equal Allocation) ---
# Assuming "equal allocation" means each stock contributes equally to the average return.
# This is a simple average of the *percentage returns* of each stock.
portfolio_average_performance = defaultdict(float)
stock_count_per_period = defaultdict(int)

for stock_data in individual_stock_performance:
    for period, perf_str in stock_data["performance"].items():
        if "N/A" not in perf_str:
            try:
                # Remove '%' and convert to float
                performance_value = float(perf_str.replace('%', ''))
                portfolio_average_performance[period] += performance_value
                stock_count_per_period[period] += 1
            except ValueError:
                # Handle cases where conversion fails if string is unexpected
                pass

final_portfolio_performance = {}
for period, total_perf in portfolio_average_performance.items():
    if stock_count_per_period[period] > 0:
        final_portfolio_performance[period] = f"{total_perf / stock_count_per_period[period]:.2f}%"
    else:
        final_portfolio_performance[period] = "N/A (No valid data)"

# --- Generate Recommendations ---
def get_recommendation(performance_data):
    recommendations = []
    # Basic rule-based recommendations
    if "Last 12 Months (Q1-Q4)" in performance_data:
        try:
            perf_12m = float(performance_data["Last 12 Months (Q1-Q4)"].replace('%', ''))
            if perf_12m > 20:
                recommendations.append("Strong performer over 12 months. Consider holding or further research.")
            elif perf_12m > 0:
                recommendations.append("Positive performance over 12 months. Monitor closely.")
            else:
                recommendations.append("Negative performance over 12 months. Review fundamentals and market conditions.")
        except ValueError:
            pass # N/A case already handled

    # More specific recommendations based on very recent performance (e.g., last 3 months)
    if "Last 3 Months (Q4)" in performance_data:
        try:
            perf_3m = float(performance_data["Last 3 Months (Q4)"].replace('%', ''))
            if perf_3m < -10:
                recommendations.append("Recent significant decline. Investigate reasons for the drop.")
            elif perf_3m > 10 and perf_12m < 0: # Recently recovered but bad long term
                 recommendations.append("Recent strong recovery; long-term performance is still negative. Evaluate for potential turnaround or continued volatility.")
        except ValueError:
            pass
            
    if not recommendations:
        recommendations.append("Performance data inconclusive for specific recommendations. Conduct deeper analysis.")

    return " ".join(recommendations)

# --- Output Results ---
print("\n--- Individual Stock Performance ---")
for stock in individual_stock_performance:
    print(f"\n{stock['stock_name']} ({stock['symbol']}) - Current Price: {stock['current_price']}")
    for period, perf in stock["performance"].items():
        print(f"  {period}: {perf}")
    # Add recommendations for each stock
    print(f"  Recommendation: {get_recommendation(stock['performance'])}")

print("\n--- Weighted Average Portfolio Performance (Equal Allocation) ---")
for period, avg_perf in final_portfolio_performance.items():
    print(f"  {period}: {avg_perf}")

print("\n--- General Portfolio Recommendations ---")
print("These recommendations are based on simulated data and general market principles.")
print("For personalized financial advice, consult a certified financial advisor.")
if final_portfolio_performance:
    overall_12m_perf = final_portfolio_performance.get("Last 12 Months (Q1-Q4)", "N/A")
    if "N/A" not in overall_12m_perf:
        try:
            overall_12m_value = float(overall_12m_perf.replace('%', ''))
            if overall_12m_value > 15:
                print("- Your portfolio shows strong overall growth over the past year. Consider reviewing individual components to maintain momentum.")
            elif overall_12m_value > 0:
                print("- Your portfolio has positive overall performance. Continue monitoring and rebalancing as needed.")
            else:
                print("- Your portfolio has experienced a decline over the past year. This may indicate a need to re-evaluate investment strategies, diversify further, or research underperforming assets.")
        except ValueError:
            print("- Cannot provide a specific overall recommendation due to data issues.")
    else:
        print("- Not enough valid data to provide a comprehensive overall portfolio recommendation.")

print("\nDisclaimer: Investment in the stock market involves risks, and past performance is not indicative of future results. This program provides general information and should not be considered financial advice.")
