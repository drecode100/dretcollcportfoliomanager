import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from collections import defaultdict
import streamlit as st # Import Streamlit

# --- User Portfolio Data (from your provided list) ---
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
today = datetime.date(2025, 6, 27) # Using a fixed date as per the context (June 27, 2025)

performance_periods = {
    "Last 3 Months (Q4)": lambda: today - relativedelta(months=3),
    "Last 6 Months (Q3-Q4)": lambda: today - relativedelta(months=6),
    "Last 9 Months (Q2-Q4)": lambda: today - relativedelta(months=9),
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

    Refer to the previous explanation for how to integrate a real API (e.g., Alpha Vantage, yfinance).
    """
    # st.write(f"Fetching mock data for {symbol} from {start_date} to {end_date}") # Debugging line for Streamlit

    # MOCK DATA: Simulate different prices for different periods
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
        # Find the stock's current price from the portfolio list
        current_p = next(s["current_price"] for s in portfolio if s["symbol"] == symbol)
        if start_date <= datetime.date(2022, 6, 27):
            return {"start_price": current_p * 0.8, "end_price": current_p}
        else:
            return {"start_price": current_p * 0.95, "end_price": current_p}
    else: # Generic mock for other stocks
        current_p = next(s["current_price"] for s in portfolio if s["symbol"] == symbol)
        if start_date <= datetime.date(2022, 6, 27):
            return {"start_price": 0.7 * current_p, "end_price": current_p}
        elif start_date <= datetime.date(2023, 6, 27):
            return {"start_price": 0.85 * current_p, "end_price": current_p}
        elif start_date <= datetime.date(2024, 6, 27):
            return {"start_price": 0.95 * current_p, "end_price": current_p}
        else:
            return {"start_price": 0.98 * current_p, "end_price": current_p}


# --- Generate Recommendations ---
def get_recommendation(performance_data):
    recommendations = []
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
            pass

    if "Last 3 Months (Q4)" in performance_data:
        try:
            perf_3m = float(performance_data["Last 3 Months (Q4)"].replace('%', ''))
            if perf_3m < -10:
                recommendations.append("Recent significant decline. Investigate reasons for the drop.")
            elif perf_3m > 10 and perf_12m < 0:
                 recommendations.append("Recent strong recovery; long-term performance is still negative. Evaluate for potential turnaround or continued volatility.")
        except ValueError:
            pass
            
    if not recommendations:
        recommendations.append("Performance data inconclusive for specific recommendations. Conduct deeper analysis.")

    return " ".join(recommendations)


# --- Streamlit App Layout ---
st.set_page_config(layout="wide")
st.title("Stock Portfolio Performance Analyzer")
st.write(f"Analysis as of: **{today.strftime('%Y-%m-%d')}**")
st.markdown("---")


# --- Analyze Stock Performance ---
individual_stock_performance = []

# Using Streamlit spinner to show loading
with st.spinner("Calculating individual stock performance..."):
    for stock_info in portfolio:
        symbol = stock_info["symbol"]
        stock_name = stock_info["stock"]
        current_price = stock_info["current_price"]
        currency = stock_info.get("currency", "$")

        stock_results = {
            "symbol": symbol,
            "stock_name": stock_name,
            "current_price": f"{current_price} {currency}",
            "performance": {}
        }

        for period_name, get_start_date_func in performance_periods.items():
            start_date = get_start_date_func()
            if start_date > today:
                start_date = today

            historical_data = get_historical_data(symbol, start_date, today)

            if historical_data and "start_price" in historical_data and "end_price" in historical_data:
                start_price_val = historical_data["start_price"]
                end_price_val = historical_data["end_price"]

                if start_price_val is not None and start_price_val > 0:
                    percentage_change = ((end_price_val - start_price_val) / start_price_val) * 100
                    stock_results["performance"][period_name] = f"{percentage_change:.2f}%"
                else:
                    stock_results["performance"][period_name] = "N/A (Start price 0 or None)"
            else:
                stock_results["performance"][period_name] = "N/A (Data not found)"

        individual_stock_performance.append(stock_results)

st.header("Individual Stock Performance")

# Prepare data for a clean DataFrame display
display_data = []
for stock in individual_stock_performance:
    row = {
        "Symbol": stock["symbol"],
        "Stock Name": stock["stock_name"],
        "Current Price": stock["current_price"]
    }
    for period, perf in stock["performance"].items():
        row[period] = perf
    row["Recommendation"] = get_recommendation(stock["performance"])
    display_data.append(row)

# Convert to DataFrame for better display
df_individual = pd.DataFrame(display_data)
st.dataframe(df_individual, use_container_width=True)

st.markdown("---")

# --- Calculate Weighted Average Portfolio Performance (Equal Allocation) ---
portfolio_average_performance = defaultdict(float)
stock_count_per_period = defaultdict(int)

with st.spinner("Calculating portfolio average performance..."):
    for stock_data in individual_stock_performance:
        for period, perf_str in stock_data["performance"].items():
            if "N/A" not in perf_str:
                try:
                    performance_value = float(perf_str.replace('%', ''))
                    portfolio_average_performance[period] += performance_value
                    stock_count_per_period[period] += 1
                except ValueError:
                    pass

    final_portfolio_performance = {}
    for period, total_perf in portfolio_average_performance.items():
        if stock_count_per_period[period] > 0:
            final_portfolio_performance[period] = f"{total_perf / stock_count_per_period[period]:.2f}%"
        else:
            final_portfolio_performance[period] = "N/A (No valid data)"

st.header("Weighted Average Portfolio Performance (Equal Allocation)")

# Prepare data for a DataFrame display for portfolio averages
portfolio_avg_df = pd.DataFrame([
    {"Period": period, "Average Performance": avg_perf}
    for period, avg_perf in final_portfolio_performance.items()
])
st.dataframe(portfolio_avg_df, use_container_width=True)

st.markdown("---")

st.header("General Portfolio Recommendations")
st.info("These recommendations are based on simulated data and general market principles. For personalized financial advice, consult a certified financial advisor.")

if final_portfolio_performance:
    overall_12m_perf = final_portfolio_performance.get("Last 12 Months (Q1-Q4)", "N/A")
    if "N/A" not in overall_12m_perf:
        try:
            overall_12m_value = float(overall_12m_perf.replace('%', ''))
            if overall_12m_value > 15:
                st.success("- Your portfolio shows strong overall growth over the past year. Consider reviewing individual components to maintain momentum.")
            elif overall_12m_value > 0:
                st.info("- Your portfolio has positive overall performance. Continue monitoring and rebalancing as needed.")
            else:
                st.warning("- Your portfolio has experienced a decline over the past year. This may indicate a need to re-evaluate investment strategies, diversify further, or research underperforming assets.")
        except ValueError:
            st.error("- Cannot provide a specific overall recommendation due to data issues.")
    else:
        st.warning("- Not enough valid data to provide a comprehensive overall portfolio recommendation.")

st.markdown("---")
st.caption("Disclaimer: Investment in the stock market involves risks, and past performance is not indicative of future results. This program provides general information and should not be considered financial advice.")
