import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from collections import defaultdict
import streamlit as st # Import Streamlit

# --- Streamlit App Layout ---
st.set_page_config(layout="wide")
st.title("📈 Stock Portfolio Performance Analyzer")
st.markdown("---")

# --- User Input Section ---
st.header("Configure Your Portfolio & Analysis")

# Allow user to input/edit portfolio data
st.markdown("### Your Portfolio Holdings (Edit shares as needed)")
st.info("💡 Edit the 'Shares' column directly in the table below. The current price is for reference; historical prices will be *mocked* unless you integrate a real API.")

# Default portfolio data with a placeholder for shares
default_portfolio_data = [
    {"symbol": "CLOV", "stock": "CLOVER HEALTH INVESTMENTS CORP.", "current_price": 2.75, "shares": 100},
    {"symbol": "PFFA", "stock": "VIRTUS INFRACAP US PFD ETF", "current_price": 20.83, "shares": 50},
    {"symbol": "ABNB", "stock": "AIRBNB", "current_price": 133.97, "shares": 10},
    {"symbol": "BABA", "stock": "ALIBABA GROUP", "current_price": 114.05, "shares": 15},
    {"symbol": "FOUR", "stock": "SHIFT4 PAYMENTS", "current_price": 98.73, "shares": 12},
    {"symbol": "CTXR", "stock": "CITIUS PHARMACEUTICALS INC.", "current_price": 1.67, "shares": 500},
    {"symbol": "BIDU", "stock": "BAIDU INC.", "current_price": 85.73, "shares": 20},
    {"symbol": "LGO", "stock": "LARGO RESOURCS LTD.", "current_price": 1.22, "shares": 800},
    {"symbol": "EEMA", "stock": "MSCI EMERGING MARKETS ASIA ISHARES", "current_price": 82.74, "shares": 10},
    {"symbol": "RTX", "stock": "RTX CORP", "current_price": 144.47, "shares": 8},
    {"symbol": "JD", "stock": "JD COM INC", "current_price": 33.16, "shares": 30},
    {"symbol": "NOK", "stock": "NOKIA CORP", "current_price": 5.17, "shares": 200},
    {"symbol": "AMD", "stock": "ADVANCED MICRO DEVICES INC", "current_price": 143.94, "shares": 10},
    {"symbol": "NXPI", "stock": "NXP SEMICONDUCTORS NV", "current_price": 218.06, "shares": 7},
    {"symbol": "MOH", "stock": "MOLINA HELTHCARE INC", "current_price": 296.19, "shares": 5},
    {"symbol": "NVDA", "stock": "NVIDIA CORPORATION", "current_price": 157.49, "shares": 9},
    {"symbol": "PLD", "stock": "PROLOGIS INC", "current_price": 106.37, "shares": 11},
    {"symbol": "QCOM", "stock": "QUALCOMM INC", "current_price": 158.94, "shares": 8},
    {"symbol": "KXIN", "stock": "KAIXIN AUTO HOLDINGS", "current_price": 0.92, "shares": 1000},
    {"symbol": "KEGN", "stock": "KENGEN", "current_price": 6.84, "currency": "KES", "shares": 500},
    {"symbol": "KPLC", "stock": "KPLC", "current_price": 11.40, "currency": "KES", "shares": 400},
    {"symbol": "CABL", "stock": "EAST AFRICA CABLES", "current_price": 1.00, "currency": "KES", "shares": 2000},
    {"symbol": "UCHM", "stock": "UCHUMI", "current_price": 0.3, "currency": "KES", "shares": 5000},
    {"symbol": "UNGA", "stock": "UNGA GROUP LTD", "current_price": 20.40, "currency": "KES", "shares": 100},
    {"symbol": "ORCH", "stock": "KENYA ORCHADS LTD", "current_price": 19.50, "currency": "KES", "shares": 100},
]

# Convert to DataFrame for editing
portfolio_df = pd.DataFrame(default_portfolio_data)

# Editable dataframe in Streamlit
edited_portfolio_df = st.data_editor(
    portfolio_df,
    num_rows="dynamic",
    hide_index=True,
    column_config={
        "symbol": st.column_config.TextColumn("Stock Symbol", help="Enter stock ticker symbol (e.g., NVDA)"),
        "stock": st.column_config.TextColumn("Company Name"),
        "current_price": st.column_config.NumberColumn("Price in $", format="$%.2f"),
        "shares": st.column_config.NumberColumn("Shares", min_value=0, step=1, help="Number of shares you hold for this stock"),
        "currency": st.column_config.TextColumn("Currency")
    },
    key="portfolio_editor"
)

# Convert edited DataFrame back to list of dicts for processing
user_portfolio = edited_portfolio_df.to_dict(orient='records')

# Analysis End Date
analysis_end_date = st.date_input(
    "Select Analysis End Date",
    value=datetime.date(2025, 6, 27), # Default to fixed date as per previous context
    min_value=datetime.date(2000, 1, 1),
    max_value=datetime.date.today() + relativedelta(months=12), # Allow slightly future for testing
    help="This date will be used as the 'today' for performance calculations."
)

# API Key Input (Placeholder)
st.markdown("### API Key for Real-Time Data (Optional)")
st.info("To fetch real historical data, you'll need to integrate a financial data API. Enter your API key here (e.g., Alpha Vantage, Finnhub). **Currently, the app uses mock data.**")
api_key = st.text_input("Enter your API Key (e.g., for Alpha Vantage)", type="password", help="Your API key for real financial data access. Leave blank to use mock data.")


# --- Define Performance Periods ---
# We'll use the selected analysis_end_date as 'today' for calculations
performance_periods = {
    "Last 3 Months (Q4)": lambda end_date: end_date - relativedelta(months=3),
    "Last 6 Months (Q3-Q4)": lambda end_date: end_date - relativedelta(months=6),
    "Last 9 Months (Q2-Q4)": lambda end_date: end_date - relativedelta(months=9),
    "Last 12 Months (Q1-Q4)": lambda end_date: end_date - relativedelta(months=12),
    "Last 18 Months": lambda end_date: end_date - relativedelta(months=18),
    "Last 24 Months": lambda end_date: end_date - relativedelta(months=24),
    "Last 36 Months": lambda end_date: end_date - relativedelta(months=36),
}

# --- Function to fetch historical data (MOCK/PLACEHOLDER) ---
def get_historical_data(symbol, start_date, end_date, api_key=None):
    """
    *** IMPORTANT: This function is a MOCK and does NOT fetch real data. ***
    You need to replace this with actual API calls to a financial data provider.

    If api_key is provided, you would use it here.
    Example (using hypothetical yfinance integration if you uncomment and install yfinance):
    # import yfinance as yf
    # try:
    #     ticker = yf.Ticker(symbol)
    #     hist = ticker.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    #     if not hist.empty:
    #         # Get the closing price on the start_date (or closest available)
    #         # and the closing price on the end_date (or closest available)
    #         # This requires careful indexing, e.g., hist['Close'].iloc[0] and hist['Close'].iloc[-1]
    #         # Or look up specific dates.
    #         # For simplicity, let's assume we take the first and last available dates in the range.
    #         start_price = hist['Close'].iloc[0]
    #         end_price = hist['Close'].iloc[-1]
    #         return {"start_price": start_price, "end_price": end_price}
    # except Exception as e:
    #     st.error(f"Error fetching data for {symbol} using yfinance: {e}")
    #     return None
    """
    # MOCK DATA: Simulate different prices for different periods
    # Get current price from the user_portfolio based on the symbol
    current_stock_info = next((s for s in user_portfolio if s["symbol"] == symbol), None)
    if not current_stock_info:
        return None # Should not happen if data is well-formed

    current_p = current_stock_info["current_price"]

    if symbol == "NVDA":
        if start_date <= datetime.date(2022, 6, 27): # 36 months ago
            return {"start_price": 50.0, "end_price": current_p}
        elif start_date <= datetime.date(2023, 6, 27): # 24 months ago
            return {"start_price": 80.0, "end_price": current_p}
        elif start_date <= datetime.date(2024, 6, 27): # 12 months ago
            return {"start_price": 120.0, "end_price": current_p}
        elif start_date <= datetime.date(2025, 3, 27): # 3 months ago (Q4)
            return {"start_price": 140.0, "end_price": current_p}
        else: # Default for shorter periods if not specified
            return {"start_price": 0.98 * current_p, "end_price": current_p} # Simulate slight gain
    elif symbol == "BABA":
        if start_date <= datetime.date(2022, 6, 27):
            return {"start_price": 90.0, "end_price": current_p}
        elif start_date <= datetime.date(2023, 6, 27):
            return {"start_price": 100.0, "end_price": current_p}
        elif start_date <= datetime.date(2024, 6, 27):
            return {"start_price": 110.0, "end_price": current_p}
        else:
            return {"start_price": 0.99 * current_p, "end_price": current_p} # Simulate slight gain
    elif current_stock_info.get("currency") == "KES": # Kenyan Stocks
        if start_date <= datetime.date(2022, 6, 27):
            return {"start_price": current_p * 0.8, "end_price": current_p}
        else:
            return {"start_price": current_p * 0.95, "end_price": current_p}
    else: # Generic mock for other stocks
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
    perf_12m = None
    if "Last 12 Months (Q1-Q4)" in performance_data and "N/A" not in performance_data["Last 12 Months (Q1-Q4)"]:
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

    if "Last 3 Months (Q4)" in performance_data and "N/A" not in performance_data["Last 3 Months (Q4)"]:
        try:
            perf_3m = float(performance_data["Last 3 Months (Q4)"].replace('%', ''))
            if perf_3m < -10:
                recommendations.append("Recent significant decline. Investigate reasons for the drop.")
            elif perf_3m > 10 and perf_12m is not None and perf_12m < 0: # Recently recovered but bad long term
                 recommendations.append("Recent strong recovery; long-term performance is still negative. Evaluate for potential turnaround or continued volatility.")
        except ValueError:
            pass
            
    if not recommendations:
        recommendations.append("Performance data inconclusive for specific recommendations. Conduct deeper analysis.")

    return " ".join(recommendations)

# --- Analysis Button ---
if st.button("Run Analysis", type="primary"):
    st.markdown("---")
    st.write(f"Running analysis for: **{analysis_end_date.strftime('%Y-%m-%d')}**")

    # --- Analyze Stock Performance ---
    individual_stock_performance = []

    # Using Streamlit spinner to show loading
    with st.spinner("Calculating individual stock performance... (Using mock data)"):
        for stock_info in user_portfolio:
            symbol = stock_info["symbol"]
            stock_name = stock_info["stock"]
            current_price = stock_info["current_price"]
            currency = stock_info.get("currency", "$")
            shares = stock_info.get("shares", 0) # Get shares from user input

            if shares == 0:
                continue # Skip stocks with 0 shares

            stock_results = {
                "symbol": symbol,
                "stock_name": stock_name,
                "current_price": f"{current_price} {currency}",
                "shares": shares, # Include shares in results
                "performance": {},
                "initial_value": {} # To store initial value for weighted avg
            }

            for period_name, get_start_date_func in performance_periods.items():
                start_date = get_start_date_func(analysis_end_date) # Pass end_date to lambda
                if start_date > analysis_end_date:
                    start_date = analysis_end_date

                historical_data = get_historical_data(symbol, start_date, analysis_end_date, api_key)

                if historical_data and "start_price" in historical_data and "end_price" in historical_data:
                    start_price_val = historical_data["start_price"]
                    end_price_val = historical_data["end_price"]

                    if start_price_val is not None and start_price_val > 0:
                        percentage_change = ((end_price_val - start_price_val) / start_price_val) * 100
                        stock_results["performance"][period_name] = f"{percentage_change:.2f}%"
                        # Store initial value based on shares for weighted average calculation
                        stock_results["initial_value"][period_name] = start_price_val * shares
                    else:
                        stock_results["performance"][period_name] = "N/A (Start price 0 or None)"
                        stock_results["initial_value"][period_name] = 0
                else:
                    stock_results["performance"][period_name] = "N/A (Data not found)"
                    stock_results["initial_value"][period_name] = 0

            individual_stock_performance.append(stock_results)

    st.header("Individual Stock Performance")

    # Prepare data for a clean DataFrame display
    display_data = []
    for stock in individual_stock_performance:
        row = {
            "Symbol": stock["symbol"],
            "Stock Name": stock["stock_name"],
            "Current Price": stock["current_price"],
            "Shares Held": stock["shares"]
        }
        for period, perf in stock["performance"].items():
            row[period] = perf
        row["Recommendation"] = get_recommendation(stock["performance"])
        display_data.append(row)

    df_individual = pd.DataFrame(display_data)
    st.dataframe(df_individual, use_container_width=True)

    # --- Visualization ---
    st.header("Visualizing Performance")
    # Filter out N/A values for charting
    chart_data = []
    for stock in individual_stock_performance:
        if "Last 12 Months (Q1-Q4)" in stock["performance"] and "N/A" not in stock["performance"]["Last 12 Months (Q1-Q4)"]:
            try:
                chart_data.append({
                    "Stock": stock["stock_name"],
                    "Performance (%)": float(stock["performance"]["Last 12 Months (Q1-Q4)"].replace('%', ''))
                })
            except ValueError:
                pass # Skip if value cannot be converted

    if chart_data:
        df_chart = pd.DataFrame(chart_data)
        df_chart = df_chart.sort_values(by="Performance (%)", ascending=False)
        st.subheader("Individual Stock Performance (Last 12 Months)")
        st.bar_chart(df_chart.set_index("Stock"))
    else:
        st.info("No valid 12-month performance data to display a chart.")


    st.markdown("---")

    # --- Calculate Weighted Average Portfolio Performance ---
    portfolio_weighted_performance = defaultdict(lambda: {"total_initial_value": 0.0, "total_final_value": 0.0})

    with st.spinner("Calculating weighted average portfolio performance..."):
        for stock_data in individual_stock_performance:
            shares = stock_data["shares"]
            current_price = float(stock_data["current_price"].split(" ")[0]) # Extract numerical part
            
            for period, perf_str in stock_data["performance"].items():
                if "N/A" not in perf_str:
                    try:
                        # Extract start price from initial_value for the current stock and period
                        initial_price_for_period = stock_data["initial_value"].get(period, 0) / shares if shares > 0 else 0
                        
                        if initial_price_for_period > 0:
                            portfolio_weighted_performance[period]["total_initial_value"] += initial_price_for_period * shares
                            portfolio_weighted_performance[period]["total_final_value"] += current_price * shares
                        # If start_price was 0 or None, it means no valid data for this stock for this period,
                        # so we don't include it in the sum for this period.
                    except (ValueError, TypeError):
                        pass

        final_portfolio_performance_weighted = {}
        for period, values in portfolio_weighted_performance.items():
            if values["total_initial_value"] > 0:
                weighted_change = ((values["total_final_value"] - values["total_initial_value"]) / values["total_initial_value"]) * 100
                final_portfolio_performance_weighted[period] = f"{weighted_change:.2f}%"
            else:
                final_portfolio_performance_weighted[period] = "N/A (No valid data for weighted avg)"

    st.header("Weighted Average Portfolio Performance")
    st.info("This calculation uses the number of shares you provided, reflecting your actual portfolio weighting.")

    portfolio_weighted_avg_df = pd.DataFrame([
        {"Period": period, "Weighted Average Performance": avg_perf}
        for period, avg_perf in final_portfolio_performance_weighted.items()
    ])
    st.dataframe(portfolio_weighted_avg_df, use_container_width=True)

    st.markdown("---")

    st.header("General Portfolio Recommendations")
    st.info("These recommendations are based on simulated data and general market principles. For personalized financial advice, consult a certified financial advisor.")

    if final_portfolio_performance_weighted:
        overall_12m_perf = final_portfolio_performance_weighted.get("Last 12 Months (Q1-Q4)", "N/A")
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

    # --- Download Buttons ---
    st.subheader("Download Results")

    # Convert DataFrames to CSV
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_individual = convert_df_to_csv(df_individual)
    st.download_button(
        label="Download Individual Stock Performance CSV",
        data=csv_individual,
        file_name="individual_stock_performance.csv",
        mime="text/csv",
    )

    csv_portfolio_avg = convert_df_to_csv(portfolio_weighted_avg_df)
    st.download_button(
        label="Download Weighted Portfolio Performance CSV",
        data=csv_portfolio_avg,
        file_name="weighted_portfolio_performance.csv",
        mime="text/csv",
    )

else:
    st.info("Click 'Run Analysis' to see your portfolio performance.")


# --- 🧠 30-Year Portfolio Strategy Guide ---
st.markdown("---")
st.header("🧠 30-Year Portfolio Strategy Guide")
st.markdown("""
Inspired by: Warren Buffett (value investing, compounding) and Jim Simons (quantitative, data-driven rebalancing)

### 🔍 1. Core Strategic Foundations

| Principle       | Warren Buffett                          | Jim Simons                                    |
| :-------------- | :-------------------------------------- | :-------------------------------------------- |
| **Investment Philosophy** | Buy wonderful companies at fair prices  | Exploit short-term inefficiencies via data    |
| **Holding Period** | Decades (compound over time)            | Often short-term, but repeatable patterns     |
| **Focus** | Value, fundamentals, moat               | Math, signals, quantitative models            |

### 🏗️ 2. Recommended Structure for a Long-Term Portfolio

| Component             | Suggested Allocation | Strategy                                             |
| :-------------------- | :------------------- | :--------------------------------------------------- |
| **U.S. Blue-Chip Stocks** | 30–40%               | Long-term compounding (NVDA, AMD, MOH, QCOM)         |
| **Dividend-Paying Stocks**| 10–15%               | Steady income (PFFA, PLD, RTX)                       |
| **ETFs (U.S. + Emerging)** | 20–25%               | Broad diversification (EEMA, SPY, QQQ)               |
| **Global Growth Stocks** | 10–15%               | Alibaba, JD for exposure to Asia’s growth            |
| **Speculative or Small Caps** | 5–10%                | CTXR, CLOV, LGO—high-risk, monitor closely           |
| **Kenyan Stocks** | <5% (or watchlist)   | Opportunistic; small allocation unless FX risk managed |

### 📈 3. Return Optimization Tactics

* Rebalance annually to maintain target weights
* Add capital during dips in high-quality names (NVDA, ABNB, MOH)
* Avoid overtrading: Let winners run unless fundamentals deteriorate
* Monitor key metrics: PE ratios, ROE, earnings trends
* Use rolling 5-year performance metrics to evaluate ETF or sector shifts

### ⚠️ 4. Risk Management

* Limit exposure to low-liquidity stocks (e.g. Kenyan microcaps)
* Cap speculative holdings to <10% of total portfolio
* Keep at least 20–25% in ETFs or blue-chips for downside protection
* Consider FX exposure if investing in emerging markets directly

### 🧭 5. Signals to Buy/Sell Based on Simons/Buffett Ideas

**BUY when:**
* Price dips >20% in high-quality stock (and fundamentals are intact)
* Strong earnings revisions or momentum (Simons-style signal)
* Long-term competitive moat remains intact (Buffett-style)

**SELL/REDUCE when:**
* Momentum breaks down + deteriorating earnings (Simons)
* PE ratios extremely overextended vs. sector
* Company loses moat or faces structural disruption (Buffett-style)

### 📅 6. 30-Year Mindset

* Think in 10-year blocks, not quarters
* Focus on compound annual growth rate (CAGR), not absolute returns
* Assume cyclical downturns every 7–10 years; position accordingly
* Build core around high-quality, repeatable business models
""")

st.markdown("---")

# --- Advanced Strategy & Research Insights (Conceptual) ---
st.header("🔬 Advanced Strategy & Research Insights (Conceptual)")
st.info("This section outlines advanced concepts used by professional investors. Implementing these fully requires integrating real-time data, complex models, and significant expertise. It serves as a guide for deeper exploration.")

with st.expander("Quantitative Signals (Requires Real Data)"):
    st.markdown("""
    Quantitative strategies rely on mathematical and statistical models to identify trading opportunities.
    These typically require vast amounts of historical data (price, volume, fundamental, alternative data).

    **Common Indicators (Conceptual - not calculated here):**
    * **Relative Strength Index (RSI):** Measures the speed and change of price movements to identify overbought or oversold conditions.
    * **Moving Average Convergence Divergence (MACD):** Reveals changes in the strength, direction, momentum, and duration of a trend.
    * **Bollinger Bands:** Measures market volatility and identify overbought or oversold levels.
    * **Volume Analysis:** Identifying patterns in trading volume that correlate with price movements.
    * **Factor Investing:** Screening stocks based on factors like Value (low P/E), Growth (high earnings growth), Quality (high ROE), Momentum (recent price trends), and Low Volatility.
    * **Machine Learning Models:** Predicting future price movements, volatility, or sentiment using supervised or unsupervised learning.
    """)
    st.warning("To implement these, you would need to: 1) Fetch full historical daily data for each stock, 2) Calculate these indicators using libraries like `TA-Lib` or `pandas-ta`, and 3) Develop a backtesting framework.")

with st.expander("Fundamental Analysis Factors"):
    st.markdown("""
    Fundamental analysis involves evaluating a company's financial health and intrinsic value.

    **Key Metrics to Monitor:**
    * **P/E Ratio (Price-to-Earnings):** Valuation metric comparing current share price to per-share earnings.
    * **PEG Ratio (Price/Earnings to Growth):** Relates P/E to expected earnings growth.
    * **ROE (Return on Equity):** Measures profitability in relation to shareholder equity.
    * **Debt-to-Equity Ratio:** Indicates a company's leverage.
    * **Revenue and Earnings Growth:** Tracking the rate at which a company's sales and profits are increasing.
    * **Free Cash Flow:** Cash generated after accounting for capital expenditures.
    * **Competitive Moat:** Sustainable competitive advantages (e.g., brand, patents, network effects).
    * **Management Quality:** Experience, track record, and alignment with shareholder interests.
    """)
    st.warning("Integrating these metrics requires financial statement data from APIs (e.g., Yahoo Finance's detailed financials, Alpha Vantage, Finnhub's fundamental data endpoints).")

with st.expander("Sentiment Analysis (Conceptual)"):
    st.markdown("""
    Sentiment analysis attempts to gauge the market's or public's emotional tone towards a stock or sector.

    **Sources of Sentiment Data:**
    * **News Headlines & Articles:** Analyzing financial news for positive, negative, or neutral sentiment.
    * **Social Media (e.g., X/Twitter, Reddit):** Monitoring discussions for mentions and sentiment trends.
    * **Analyst Ratings:** Aggregating buy/sell/hold recommendations from financial analysts.
    * **Earnings Call Transcripts:** Analyzing language for management's tone and forward-looking statements.
    """)
    st.warning("Implementing sentiment analysis requires access to text-based data feeds and natural language processing (NLP) capabilities.")

with st.expander("Global Macro & Event-Driven Analysis"):
    st.markdown("""
    * **Global Macro:** Investing based on broad economic trends, interest rate changes, currency movements, and geopolitical events.
    * **Event-Driven:** Exploiting opportunities arising from specific corporate events like mergers, acquisitions, bankruptcies, or spin-offs.
    """)
    st.warning("These strategies require deep understanding of economics, geopolitics, and corporate finance, often relying on expert analysis rather than purely automated signals.")
