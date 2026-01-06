import pandas as pd
from valuation.dcf import calculate_dcf_value

def dcf_sensitivity_analysis(
    fcff_df,
    wacc_range,
    growth_range,
):
    """
    Generate DCF Enterprise Value sensitivity matrix
    across WACC and terminal growth assumptions.
    """

    sensitivity = {}

    for g in growth_range:
        row = {}
        for w in wacc_range:
            # Skip invalid valuation cases
            if w <= g:
                continue

            ev, _ = calculate_dcf_value(
                fcff_df,
                wacc=w,
                terminal_growth=g
            )
            row[f"{w:.2%}"] = ev

        sensitivity[f"{g:.2%}"] = row

    sensitivity_df = pd.DataFrame(sensitivity).T
    sensitivity_df.index.name = "Terminal Growth"

    return sensitivity_df