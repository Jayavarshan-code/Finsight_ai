import pandas as pd

def calculate_fcff(df: pd.DataFrame):
    """
    Calculate Free Cash Flow to Firm (FCFF)
    using actual CapEx and Working Capital changes
    """

    fcff_df = df.copy()

    # Calculate NOPAT
    fcff_df["NOPAT"] = fcff_df["EBIT"] * (1 - fcff_df["TaxRate"])

    # Change in Working Capital
    fcff_df["Delta_WC"] = fcff_df["WorkingCapital"].diff()

    # FCFF formula
    fcff_df["FCFF"] = (
        fcff_df["NOPAT"]
        + fcff_df["Depreciation"]
        - fcff_df["CapEx"]
        - fcff_df["Delta_WC"].fillna(0)
    )

    return fcff_df[
        ["Year", "NOPAT", "Depreciation", "CapEx", "Delta_WC", "FCFF"]
    ]
def calculate_dcf_value(
    fcff_df: pd.DataFrame,
    wacc: float,
    terminal_growth=0.04,
):
    """
    Discount FCFF and calculate enterprise value
    """

    fcff_df = fcff_df.copy()
    fcff_df["Discount_Factor"] = [
        1 / ((1 + wacc) ** i) for i in range(1, len(fcff_df) + 1)
    ]

    fcff_df["PV_FCFF"] = fcff_df["FCFF"] * fcff_df["Discount_Factor"]

    terminal_value = (
        fcff_df["FCFF"].iloc[-1]
        * (1 + terminal_growth)
        / (wacc - terminal_growth)
    )

    pv_terminal_value = terminal_value * fcff_df["Discount_Factor"].iloc[-1]

    enterprise_value = fcff_df["PV_FCFF"].sum() + pv_terminal_value

    return enterprise_value, fcff_df
