import pandas as pd

REQUIRED_COLUMNS = [
    "Year", "Revenue", "EBITDA", "NetIncome",
    "TotalAssets", "TotalEquity", "Debt", "OCF"
]

def load_financials(file_path: str) -> pd.DataFrame:
    """
    Load and validate financial data
    """
    df = pd.read_csv(file_path)

    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    df = df.sort_values("Year").reset_index(drop=True)
    return df
