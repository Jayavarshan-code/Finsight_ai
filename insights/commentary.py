from openai import OpenAI

def generate_analyst_commentary(
    ratios_df,
    cagr_df,
    red_flags,
    api_key: str
):
    """
    Generate professional analyst-style commentary using OpenAI (new SDK)
    """

    client = OpenAI(api_key=api_key)

    latest = ratios_df.iloc[-1]

    summary_text = f"""
Financial Snapshot:
- ROE: {latest['ROE']:.2%}
- EBITDA Margin: {latest['EBITDA_Margin']:.2%}
- Debt to Equity: {latest['Debt_to_Equity']:.2f}

Growth (CAGR):
{cagr_df.to_string(index=False)}

Red Flags:
{chr(10).join(red_flags)}
"""

    prompt = f"""
You are a professional equity research analyst.

Based on the financial data below, write a concise analyst-style commentary covering:
1. Business performance
2. Key strengths
3. Key risks
4. Overall analytical conclusion (no buy/sell recommendation)

Data:
{summary_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional equity research analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content
