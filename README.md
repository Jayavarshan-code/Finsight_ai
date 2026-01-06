# FinSight AI – Financial Valuation & Analytics Platform

## Overview
FinSight AI is a Streamlit-based financial analytics application that performs:
- DCF Valuation (FCFF & FCFE)
- ROIC & Value Creation Analysis
- Relative Valuation (EV/EBITDA, P/E)
- Sensitivity Analysis
- Export reports to PDF & Excel

## Tech Stack
- Python
- Streamlit
- Pandas, NumPy
- FPDF / ReportLab
- GitHub

## How to Run Locally
```bash
git clone https://github.com/username/finsight_ai.git
cd finsight_ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
