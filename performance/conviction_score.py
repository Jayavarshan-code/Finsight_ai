def calculate_conviction_score(
    equity_result: dict,
    roic_spread: float,
    gqi_score: int,
    debt_equity: float,
    earnings_flags: list,
):
    """
    Calculate Conviction Score (0–100)
    """

    score = 0
    breakdown = {}

    # 1️⃣ Valuation Upside (25)
    upside = equity_result.get("Upside / Downside", 0)
    if upside > 0.25:
        v_score = 25
    elif upside > 0.1:
        v_score = 18
    else:
        v_score = 10
    breakdown["Valuation"] = v_score
    score += v_score

    # 2️⃣ ROIC vs WACC (25)
    if roic_spread > 0.05:
        r_score = 25
    elif roic_spread > 0:
        r_score = 15
    else:
        r_score = 5
    breakdown["ROIC vs WACC"] = r_score
    score += r_score

    # 3️⃣ Growth Quality (20)
    g_score = min(20, int(gqi_score * 0.2))
    breakdown["Growth Quality"] = g_score
    score += g_score

    # 4️⃣ Balance Sheet Strength (15)
    if debt_equity < 0.5:
        b_score = 15
    elif debt_equity < 1:
        b_score = 10
    else:
        b_score = 5
    breakdown["Balance Sheet"] = b_score
    score += b_score

    # 5️⃣ Earnings Quality (15)
    eq_score = 15 if "⚠️" not in "".join(earnings_flags) else 8
    breakdown["Earnings Quality"] = eq_score
    score += eq_score

    label = (
        "High Conviction"
        if score >= 75
        else "Medium Conviction"
        if score >= 50
        else "Low Conviction"
    )

    return score, label, breakdown
