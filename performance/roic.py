import pandas as pd

def calculate_roic(df: pd.DataFrame):
    """
    Calculate ROIC and Value Creation
    ROIC = NOPAT / Invested Capital
    """

    roic_df = df.copy()

    # NOPAT
    roic_df["NOPAT"] = roic_df["EBIT"] * (1 - roic_df["TaxRate"])

    # Invested Capital
    roic_df["Invested_Capital"] = (
        roic_df["TotalEquity"] + roic_df["Debt"] - roic_df["Cash"]
    )

    # ROIC
    roic_df["ROIC"] = roic_df["NOPAT"] / roic_df["Invested_Capital"]

    return roic_df[
        ["Year", "NOPAT", "Invested_Capital", "ROIC"]
    ]


def value_creation_analysis(roic_df: pd.DataFrame, wacc: float):
    """
    Compare ROIC vs WACC to assess value creation
    """

    vc_df = roic_df.copy()
    vc_df["WACC"] = wacc
    vc_df["Value_Creation_Spread"] = vc_df["ROIC"] - vc_df["WACC"]

    vc_df["Value_Creation"] = vc_df["Value_Creation_Spread"].apply(
        lambda x: "Value Creating" if x > 0 else "Value Destroying"
    )

    return vc_df[
        ["Year", "ROIC", "WACC", "Value_Creation_Spread", "Value_Creation"]
    ]