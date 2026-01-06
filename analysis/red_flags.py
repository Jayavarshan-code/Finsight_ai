import pandas as pd

def detect_red_flags(df: pd.DataFrame) -> list:
    """
    Detect financial red flags based on rule-based logic
    """
    flags = []

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else None

    # 1. Earnings Quality Issue
    if latest["NetIncome"] > 0 and latest["OCF"] < latest["NetIncome"]:
        flags.append(
            "⚠️ Earnings Quality Risk: Net income exceeds operating cash flow, indicating potential accrual-based earnings."
        )

    # 2. Rising Leverage
    if previous is not None:
        if latest["Debt"] > previous["Debt"] and latest["TotalEquity"] <= previous["TotalEquity"]:
            flags.append(
                "⚠️ Leverage Risk: Debt is increasing without corresponding equity growth."
            )

    # 3. Margin Pressure
    if previous is not None:
        prev_margin = previous["EBITDA"] / previous["Revenue"]
        curr_margin = latest["EBITDA"] / latest["Revenue"]

        if curr_margin < prev_margin:
            flags.append(
                "⚠️ Margin Pressure: EBITDA margin has declined compared to the previous period."
            )

    # 4. Weak Asset Utilization
    asset_turnover = latest["Revenue"] / latest["TotalAssets"]
    if asset_turnover < 0.5:
        flags.append(
            "⚠️ Efficiency Risk: Low asset turnover may indicate inefficient asset utilization."
        )

    if not flags:
        flags.append("✅ No major financial red flags detected based on current rules.")

    return flags