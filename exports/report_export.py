from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile


def generate_full_report(data: dict):
    """
    Generate full analyst-style financial report PDF
    """

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_path)
    story = []

    def h(text):
        story.append(Paragraph(f"<b>{text}</b>", styles["Heading2"]))
        story.append(Spacer(1, 10))

    def p(text):
        story.append(Paragraph(text, styles["BodyText"]))
        story.append(Spacer(1, 8))

    # -----------------------------
    # 1. Executive Summary
    # -----------------------------
    h("Executive Summary")
    p(
        f"""
        The company demonstrates {data['growth_label'].lower()} growth characteristics
        with a conviction score of <b>{data['conviction_score']}/100</b>.
        Value creation analysis indicates that returns on invested capital
        are {'above' if data['roic_spread'] > 0 else 'below'} the cost of capital.
        """
    )

    # -----------------------------
    # 2. Financial Performance
    # -----------------------------
    h("Financial Performance Overview")
    p(
        f"""
        Revenue has grown at a CAGR of <b>{data['revenue_cagr']}</b>,
        supported by EBITDA margin of <b>{data['ebitda_margin']}</b>.
        Profitability trends indicate {'operating leverage' if data['ebitda_margin_val'] > 0.2 else 'moderate margins'}.
        """
    )

    # -----------------------------
    # 3. Cash Flow & Earnings Quality
    # -----------------------------
    h("Cash Flow & Earnings Quality")
    p(
        "Operating cash flows "
        + ("support" if not data["red_flags"] else "lag")
        + " reported earnings. "
        + ("No major accounting concerns identified." if not data["red_flags"] else "Key risk indicators observed.")
    )

    # -----------------------------
    # 4. ROIC & Value Creation
    # -----------------------------
    h("ROIC & Value Creation")
    p(
        f"""
        The company generates a ROIC of <b>{data['roic']}</b>
        against a WACC of <b>{data['wacc']}</b>,
        resulting in a value creation spread of <b>{data['roic_spread']}</b>.
        """
    )

    # -----------------------------
    # 5. Growth Quality
    # -----------------------------
    h("Growth Quality Assessment")
    p(
        f"""
        Growth quality analysis classifies the company as
        <b>{data['growth_label']}</b>, driven by profitability,
        cash flow support, and capital efficiency.
        """
    )

    # -----------------------------
    # 6. Valuation
    # -----------------------------
    h("Valuation Analysis")
    p(
        f"""
        DCF-based intrinsic valuation indicates an enterprise value of
        <b>{data['enterprise_value']}</b>, translating to a target price of
        <b>{data['target_price']}</b>, implying an upside/downside of
        <b>{data['upside']}</b>.
        """
    )

    # -----------------------------
    # 7. Relative Valuation
    # -----------------------------
    h("Relative Valuation")
    p(
        f"""
        Relative valuation suggests the stock is trading at
        <b>{data['pe']}</b> P/E and <b>{data['ev_ebitda']}</b> EV/EBITDA,
        indicating {data['relative_view'].lower()} valuation versus peers.
        """
    )

    # -----------------------------
    # 8. Risks & Suggestions
    # -----------------------------
    h("Risks & Strategic Suggestions")
    if data["red_flags"]:
        for flag in data["red_flags"]:
            p(flag)
    else:
        p("No material financial risks detected based on current analysis.")

    p(
        """
        Strategic focus should remain on sustaining ROIC above WACC,
        disciplined capital allocation, and cash-backed growth
        to enhance long-term shareholder value.
        """
    )

    # -----------------------------
    # Disclaimer
    # -----------------------------
    h("Disclaimer")
    p(
        "This report is generated for analytical and educational purposes only and does not constitute investment advice."
    )

    doc.build(story)
    return pdf_path
