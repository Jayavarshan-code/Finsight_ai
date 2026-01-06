import pandas as pd

def calculate_trends(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Calculate YoY growth and CAGR for selected financial metrics
    """

    trend_df = df[["Year"] + columns].copy()

    # YoY Growth
    for col in columns:
        trend_df[f"{col}_YoY_Growth"] = trend_df[col].pct_change()

    # CAGR (from first to last year)
    years = trend_df["Year"].iloc[-1] - trend_df["Year"].iloc[0]

    cagr_data = {}
    for col in columns:
        start = trend_df[col].iloc[0]
        end = trend_df[col].iloc[-1]
        cagr_data[col] = (end / start) ** (1 / years) - 1 if start != 0 else None

    cagr_df = pd.DataFrame(
        list(cagr_data.items()),
        columns=["Metric", "CAGR"]
    )

    return trend_df, cagr_df