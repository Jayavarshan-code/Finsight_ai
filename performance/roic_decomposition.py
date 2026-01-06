import pandas as pd

def roic_decomposition(df: pd.DataFrame):
    """
    McKinsey-style ROIC decomposition:
    ROIC = Operating Margin × Capital Turnover
    """

    decomp_df = df.copy()

    # NOPAT
    decomp_df["NOPAT"] = decomp_df["EBIT"] * (1 - decomp_df["TaxRate"])

    # Invested Capital
    decomp_df["Invested_Capital"] = (
        decomp_df["TotalEquity"]
        + decomp_df["Debt"]
        - decomp_df["Cash"]
    )

    # Decomposition components
    decomp_df["Operating_Margin"] = decomp_df["NOPAT"] / decomp_df["Revenue"]
    decomp_df["Capital_Turnover"] = (
        decomp_df["Revenue"] / decomp_df["Invested_Capital"]
    )

    # ROIC check
    decomp_df["ROIC_Check"] = (
        decomp_df["Operating_Margin"]
        * decomp_df["Capital_Turnover"]
    )

    return decomp_df[
        [
            "Year",
            "Operating_Margin",
            "Capital_Turnover",
            "ROIC_Check",
        ]
    ]