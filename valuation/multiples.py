def calculate_trading_multiples(
    market_cap: float,
    enterprise_value: float,
    net_income: float,
    ebitda: float,
):
    """
    Calculate core trading multiples
    """

    pe = market_cap / net_income if net_income > 0 else None
    ev_ebitda = enterprise_value / ebitda if ebitda > 0 else None

    return {
        "P/E": pe,
        "EV/EBITDA": ev_ebitda,
    }


def relative_valuation_assessment(
    multiples: dict,
    peer_pe: float,
    peer_ev_ebitda: float,
):
    """
    Compare company multiples vs peer benchmarks
    """

    assessment = {}

    if multiples["P/E"] is not None:
        assessment["P/E Valuation"] = (
            "Undervalued"
            if multiples["P/E"] < peer_pe
            else "Overvalued"
        )

    if multiples["EV/EBITDA"] is not None:
        assessment["EV/EBITDA Valuation"] = (
            "Undervalued"
            if multiples["EV/EBITDA"] < peer_ev_ebitda
            else "Overvalued"
        )

    return assessment