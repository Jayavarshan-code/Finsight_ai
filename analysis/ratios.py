import pandas as pd

def calculate_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate key financial ratios for analysis
    """

    ratios_df = df.copy()

    # Profitability Ratios
    ratios_df["EBITDA_Margin"] = ratios_df["EBITDA"] / ratios_df["Revenue"]
    ratios_df["Net_Margin"] = ratios_df["NetIncome"] / ratios_df["Revenue"]

    # Return Ratios
    ratios_df["ROE"] = ratios_df["NetIncome"] / ratios_df["TotalEquity"]
    ratios_df["ROA"] = ratios_df["NetIncome"] / ratios_df["TotalAssets"]

    # Leverage Ratios
    ratios_df["Debt_to_Equity"] = ratios_df["Debt"] / ratios_df["TotalEquity"]

    # Efficiency Ratios
    ratios_df["Asset_Turnover"] = ratios_df["Revenue"] / ratios_df["TotalAssets"]

    return ratios_df