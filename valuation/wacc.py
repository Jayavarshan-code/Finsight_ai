def calculate_wacc(
    cost_of_equity=0.12,
    cost_of_debt=0.08,
    tax_rate=0.25,
    equity_weight=0.7,
    debt_weight=0.3,
):
    """
    Calculate Weighted Average Cost of Capital (WACC)
    """

    wacc = (
        equity_weight * cost_of_equity
        + debt_weight * cost_of_debt * (1 - tax_rate)
    )

    return wacc