import pandas as pd
import numpy as np

def growth_quality_index(df: pd.DataFrame, roic_df: pd.DataFrame):
    """
    Calculate Growth Quality Index (0–100)
    """

    # CAGR calculations
    years = df["Year"].iloc[-1] - df["Year"].iloc[0]

    revenue_cagr = (df["Revenue"].iloc[-1] / df["Revenue"].iloc[0]) ** (1 / years) - 1
    ni_cagr = (df["NetIncome"].iloc[-1] / df["NetIncome"].iloc[0]) ** (1 / years) - 1
    ocf_cagr = (df["OCF"].iloc[-1] / df["OCF"].iloc[0]) ** (1 / years) - 1

    # 1️⃣ Profitability-backed growth (30)
    profit_score = 30 if ni_cagr >= revenue_cagr else 15

    # 2️⃣ Cash-backed growth (30)
    cash_score = 30 if ocf_cagr >= ni_cagr else 15

    # 3️⃣ ROIC sustainability (20)
    roic_mean = roic_df["ROIC"].mean()
    roic_score = 20 if roic_mean > 0.12 else 10

    # 4️⃣ Growth consistency (20)
    revenue_yoy = df["Revenue"].pct_change().dropna()
    volatility = revenue_yoy.std()

    consistency_score = 20 if volatility < 0.15 else 10

    total_score = profit_score + cash_score + roic_score + consistency_score

    label = (
        "High-Quality Growth"
        if total_score >= 80
        else "Moderate-Quality Growth"
        if total_score >= 50
        else "Low-Quality Growth"
    )

    return {
        "Revenue CAGR": revenue_cagr,
        "Net Income CAGR": ni_cagr,
        "OCF CAGR": ocf_cagr,
        "ROIC (Avg)": roic_mean,
        "Growth Volatility": volatility,
        "Growth Quality Score": total_score,
        "Growth Quality Label": label,
    }
