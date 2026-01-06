import streamlit as st

# -----------------------------
# Import
# -----------------------------
from performance.growth_quality import growth_quality_index
from utils.data_loader import load_financials
from performance.roic_decomposition import roic_decomposition
from analysis.ratios import calculate_ratios
from exports.report_export import generate_full_report
from performance.conviction_score import calculate_conviction_score
from analysis.trends import calculate_trends
from analysis.red_flags import detect_red_flags
from performance.roic import calculate_roic, value_creation_analysis
from valuation.dcf import calculate_fcff, calculate_dcf_value
from valuation.wacc import calculate_wacc
from valuation.sensitivity import dcf_sensitivity_analysis
from valuation.equity_value import calculate_equity_value
from valuation.multiples import (
    calculate_trading_multiples,
    relative_valuation_assessment,
)


# -----------------------------
# App Title
# -----------------------------
st.title("FinSight AI – Analyst Platform")

file_path = "data/raw/company_financials_10_years_full.csv"

try:
    # =========================================================
    # LOAD DATA
    # =========================================================
    df = load_financials(file_path)

    st.subheader("Financial Data (10 Years)")
    st.dataframe(df.style.format("{:,.0f}"))

    latest = df.iloc[-1]

    # =========================================================
    # KPI CARDS
    # =========================================================
    st.subheader("Key Performance Indicators")

    roe = latest["NetIncome"] / latest["TotalEquity"]
    ebitda_margin = latest["EBITDA"] / latest["Revenue"]
    debt_equity = latest["Debt"] / latest["TotalEquity"]

    years = df["Year"].iloc[-1] - df["Year"].iloc[0]
    revenue_cagr = (
        (df["Revenue"].iloc[-1] / df["Revenue"].iloc[0]) ** (1 / years) - 1
        if years > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ROE", f"{roe:.2%}")
    col2.metric("EBITDA Margin", f"{ebitda_margin:.2%}")
    col3.metric("Debt / Equity", f"{debt_equity:.2f}")
    col4.metric("Revenue CAGR", f"{revenue_cagr:.2%}")

    # =========================================================
    # FINANCIAL RATIOS
    # =========================================================
    ratios_df = calculate_ratios(df)

    st.subheader("Key Financial Ratios")

    ratio_columns = [
        "EBITDA_Margin",
        "Net_Margin",
        "ROE",
        "ROA",
        "Debt_to_Equity",
        "Asset_Turnover",
    ]

    st.dataframe(
        ratios_df[["Year"] + ratio_columns].style.format(
            {col: "{:.2%}" for col in ratio_columns}
        )
    )

    # =========================================================
    # TREND ANALYSIS
    # =========================================================
    st.subheader("Trend Analysis")

    trend_columns = ["Revenue", "EBITDA", "NetIncome"]
    trend_df, cagr_df = calculate_trends(df, trend_columns)

    st.markdown("### Year-over-Year Growth")

    yoy_cols = ["Year"] + [f"{c}_YoY_Growth" for c in trend_columns]
    st.dataframe(
        trend_df[yoy_cols].style.format(
            {c: "{:.2%}" for c in yoy_cols if c != "Year"}
        )
    )

    st.markdown("### CAGR Summary")
    st.dataframe(cagr_df.style.format({"CAGR": "{:.2%}"}))

    # =========================================================
    # RED FLAG ANALYSIS
    # =========================================================
    st.subheader("Red Flag Analysis")

    red_flags = detect_red_flags(df)
    for flag in red_flags:
        st.write(flag)

    # =========================================================
    # FCFF – ACTUALS BASED
    # =========================================================
    st.subheader("Free Cash Flow to Firm (FCFF) – Actuals Based")

    fcff_df = calculate_fcff(df)

    st.dataframe(
        fcff_df.style.format(
            {
                "NOPAT": "{:,.0f}",
                "Depreciation": "{:,.0f}",
                "CapEx": "{:,.0f}",
                "Delta_WC": "{:,.0f}",
                "FCFF": "{:,.0f}",
            }
        )
    )

    # =========================================================
    # DCF VALUATION
    # =========================================================
    st.subheader("DCF Valuation (FCFF Based)")

    wacc = st.slider("WACC", 0.08, 0.15, 0.11, 0.01)
    terminal_growth = st.slider("Terminal Growth Rate", 0.02, 0.06, 0.04, 0.005)

    enterprise_value, dcf_table = calculate_dcf_value(
        fcff_df, wacc=wacc, terminal_growth=terminal_growth
    )

    st.metric("Enterprise Value (DCF)", f"{enterprise_value:,.0f}")

    # =========================================================
    # DCF SENSITIVITY ANALYSIS
    # =========================================================
    st.subheader("DCF Sensitivity Analysis")

    wacc_range = [wacc - 0.02, wacc - 0.01, wacc, wacc + 0.01, wacc + 0.02]
    growth_range = [terminal_growth - 0.01, terminal_growth, terminal_growth + 0.01]

    wacc_range = [w for w in wacc_range if w > terminal_growth]
    growth_range = [g for g in growth_range if g > 0]

    sensitivity_df = dcf_sensitivity_analysis(
        fcff_df, wacc_range=wacc_range, growth_range=growth_range
    )

    st.dataframe(sensitivity_df.style.format("{:,.0f}"))

    # =========================================================
    # EQUITY VALUE & TARGET PRICE
    # =========================================================
    st.subheader("Equity Value & Target Price")

    cash = st.number_input("Cash & Cash Equivalents", value=float(latest["Cash"]))
    shares_outstanding = st.number_input(
        "Shares Outstanding (in millions)",
        value=float(latest["SharesOutstanding"]),
    )
    current_price = st.number_input(
        "Current Market Price", value=float(latest["CurrentPrice"])
    )

    equity_result = calculate_equity_value(
        enterprise_value=enterprise_value,
        total_debt=latest["Debt"],
        cash=cash,
        shares_outstanding=shares_outstanding,
        current_price=current_price,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Enterprise Value", f"{equity_result['Enterprise Value']:,.0f}")
    col2.metric("Net Debt", f"{equity_result['Net Debt']:,.0f}")
    col3.metric("Equity Value", f"{equity_result['Equity Value']:,.0f}")
    col4.metric("Target Price", f"{equity_result['Target Price']:,.2f}")

    if "Upside / Downside" in equity_result:
        st.metric(
            "Upside / Downside",
            f"{equity_result['Upside / Downside']:.2%}",
        )
    # =========================================================
    # ROIC & VALUE CREATION ANALYSIS
    # =========================================================
    st.subheader("ROIC & Value Creation Analysis")

    roic_df = calculate_roic(df)

    vc_df = value_creation_analysis(roic_df, wacc=wacc)

    st.dataframe(
        vc_df.style.format(
            {
                "ROIC": "{:.2%}",
                "WACC": "{:.2%}",
                "Value_Creation_Spread": "{:.2%}",
            }
        )
    )

    latest_vc = vc_df.iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("ROIC (Latest)", f"{latest_vc['ROIC']:.2%}")
    col2.metric("WACC", f"{latest_vc['WACC']:.2%}")
    col3.metric(
        "Value Creation Spread",
        f"{latest_vc['Value_Creation_Spread']:.2%}",
    )

    # =========================================================
    # RELATIVE VALUATION (MULTIPLES)
    # =========================================================
    st.subheader("Relative Valuation (Trading Multiples)")

    # Market values
    market_cap = latest["CurrentPrice"] * latest["SharesOutstanding"]

    multiples = calculate_trading_multiples(
        market_cap=market_cap,
        enterprise_value=enterprise_value,
        net_income=latest["NetIncome"],
        ebitda=latest["EBITDA"],
    )

    # Peer benchmarks (user inputs)
    st.markdown("### Peer Benchmark Assumptions")

    peer_pe = st.number_input("Peer Average P/E", value=20.0, step=1.0)
    peer_ev_ebitda = st.number_input("Peer Average EV/EBITDA", value=12.0, step=0.5)

    assessment = relative_valuation_assessment(
        multiples,
        peer_pe=peer_pe,
        peer_ev_ebitda=peer_ev_ebitda,
    )

        # Display multiples
    col1, col2 = st.columns(2)
    col1.metric("P/E", f"{multiples['P/E']:.2f}")
    col2.metric("EV / EBITDA", f"{multiples['EV/EBITDA']:.2f}")

        # Display assessment
    st.markdown("### Relative Valuation Assessment")
    for k, v in assessment.items():
        st.write(f"• **{k}**: {v}")
        # =========================================================
        # ROIC DECOMPOSITION
        # =========================================================
        st.subheader("ROIC Decomposition – McKinsey Framework")

        roic_decomp_df = roic_decomposition(df)

        st.dataframe(
                roic_decomp_df.style.format(
                    {
                    "Operating_Margin": "{:.2%}",
                    "Capital_Turnover": "{:.2f}",
                    "ROIC_Check": "{:.2%}",
                }
            )
        )

        latest_roic = roic_decomp_df.iloc[-1]

        col1, col2, col3 = st.columns(3)
        col1.metric("Operating Margin", f"{latest_roic['Operating_Margin']:.2%}")
        col2.metric("Capital Turnover", f"{latest_roic['Capital_Turnover']:.2f}")
        col3.metric("ROIC", f"{latest_roic['ROIC_Check']:.2%}")
    # =========================================================
    # GROWTH QUALITY INDEX
    # =========================================================
    st.subheader("Growth Quality Index")

    gqi = growth_quality_index(df, roic_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue CAGR", f"{gqi['Revenue CAGR']:.2%}")
    col2.metric("Net Income CAGR", f"{gqi['Net Income CAGR']:.2%}")
    col3.metric("OCF CAGR", f"{gqi['OCF CAGR']:.2%}")

    col4, col5 = st.columns(2)
    col4.metric("ROIC (Avg)", f"{gqi['ROIC (Avg)']:.2%}")
    col5.metric("Growth Volatility", f"{gqi['Growth Volatility']:.2%}")

    st.metric(
        "Growth Quality Score",
        f"{gqi['Growth Quality Score']} / 100"
    )

    st.success(f"Assessment: {gqi['Growth Quality Label']}")
    # =========================================================
    # CONVICTION SCORE
    # =========================================================
    st.subheader("Investment Conviction Score")

    roic_spread = latest_vc["Value_Creation_Spread"]

    conviction_score, conviction_label, breakdown = calculate_conviction_score(
        equity_result=equity_result,
        roic_spread=roic_spread,
        gqi_score=gqi["Growth Quality Score"],
        debt_equity=debt_equity,
        earnings_flags=red_flags,
    )

    st.metric(
        "Conviction Score",
        f"{conviction_score} / 100",
        conviction_label,
    )

    st.markdown("### Score Breakdown")
    for k, v in breakdown.items():
        st.write(f"• **{k}**: {v}")
    # =========================================================
    # INVESTMENT COMMITTEE (IC) SUMMARY
    # =========================================================
    st.subheader("Investment Committee Summary")

    st.markdown("### Business Snapshot")
    st.write(
        f"""
        • Revenue CAGR: {revenue_cagr:.2%}  
        • ROIC vs WACC: {latest_vc['ROIC']:.2%} vs {latest_vc['WACC']:.2%}  
        • Growth Quality: {gqi['Growth Quality Label']}  
        """
    )

    st.markdown("### Valuation Summary")
    st.write(
        f"""
        • Enterprise Value (DCF): {enterprise_value:,.0f}  
        • Target Price: {equity_result['Target Price']:.2f}  
        • Upside / Downside: {equity_result.get('Upside / Downside', 0):.2%}
        """
    )

    st.markdown("### Risk Summary")
    for flag in red_flags:
        st.write(f"• {flag}")

    st.markdown("### Final View")
    st.success(
        f"""
        **Conviction Level:** {conviction_label}  
        **Conviction Score:** {conviction_score}/100  

        The company demonstrates {'strong' if conviction_score > 75 else 'moderate'} fundamentals
        with valuation support and {'sustainable' if roic_spread > 0 else 'questionable'} value creation.
        """
    )

    if st.button("📄 Export Full Financial Report"):
        report_data = {
            "conviction_score": conviction_score,
            "growth_label": gqi["Growth Quality Label"],
            "revenue_cagr": f"{revenue_cagr:.2%}",
            "ebitda_margin": f"{ebitda_margin:.2%}",
            "ebitda_margin_val": ebitda_margin,
            "roic": f"{latest_vc['ROIC']:.2%}",
            "wacc": f"{latest_vc['WACC']:.2%}",
            "roic_spread": latest_vc["Value_Creation_Spread"],
            "enterprise_value": f"{enterprise_value:,.0f}",
            "target_price": f"{equity_result['Target Price']:.2f}",
            "upside": f"{equity_result.get('Upside / Downside', 0):.2%}",
            "pe": f"{multiples['P/E']:.2f}",
            "ev_ebitda": f"{multiples['EV/EBITDA']:.2f}",
            "relative_view": list(assessment.values())[0],
            "red_flags": red_flags,
        }

        pdf_path = generate_full_report(report_data)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download Full Financial Report (PDF)",
                f,
                file_name="FinSight_Full_Analyst_Report.pdf",
                mime="application/pdf",
            )

except Exception as e:
    st.error(str(e))
