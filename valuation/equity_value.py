def calculate_equity_value(
    enterprise_value: float,
    total_debt: float,
    cash: float,
    shares_outstanding: float,
    current_price: float = None,
):
    """
    Convert Enterprise Value to Equity Value and Target Price
    """

    net_debt = total_debt - cash
    equity_value = enterprise_value - net_debt
    target_price = equity_value / shares_outstanding

    result = {
        "Enterprise Value": enterprise_value,
        "Net Debt": net_debt,
        "Equity Value": equity_value,
        "Target Price": target_price,
    }

    if current_price:
        upside = (target_price / current_price) - 1
        result["Upside / Downside"] = upside

    return result