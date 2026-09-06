# ⚡ CELR Alpha Terminal: Institutional Capital Preservation Engine

An enterprise-grade predictive analytics terminal built to model **Customer Equity Liquidation Risk (CELR)**, assess capital loss exposure, and simulate intervention yield recovery for dynamic portfolio management.

---

## 📌 Executive Overview

The **CELR Alpha Terminal** addresses capital attrition in institutional portfolios and commerce by identifying high-risk, high-value accounts prior to churn or asset liquidation. By coupling machine learning predictive modeling with real-time stress-testing controls, the system provides risk managers with actionable metrics to deploy targeted retention capital.

### Key Value Propositions
* **Predictive Risk Scoring**: Quantifies individual account liquidation probabilities ($P_{\text{Liquidation}}$).
* **Capital Risk Prioritization**: Computes total monetary capital exposure ($\text{CELR}$) across active account portfolios.
* **Intervention ROI Simulation**: Real-time scenario modeling to evaluate net returns on deployed rescue capital.

---

## 🧮 Mathematical Formulation

The Core Risk Index evaluates expected financial loss exposure per asset:

$$\text{CELR}_i = P(\text{Liquidation}_i) \times \text{PAY}_i$$

Where:
* **$\text{CELR}_i$**: Customer Equity Liquidation Risk exposure for asset $i$ (£).
* **$P(\text{Liquidation}_i)$**: Model-estimated probability of account churn/liquidation ($0 \le P \le 1$).
* **$\text{PAY}_i$**: Projected Asset Yield—the expected long-term gross margin of customer $i$ (£).

---

## 🏷️ Asset Classification Taxonomy

Accounts are dynamically stratified into four distinct operational tiers:

| Asset Tier | Risk Profile ($P_{\text{Liquidation}}$) | Yield Profile ($\text{PAY}$) | Strategic Action |
| :--- | :--- | :--- | :--- |
| **Tier 1 Alpha Asset** | Low ($< 30\%$) | High ($\ge £1,000$) | Core engagement & VIP cross-sell |
| **High-Yield Volatile** | High ($\ge 50\%$) | High ($\ge £1,000$) | Immediate capital intervention & custom outreach |
| **Distressed Equity** | High ($\ge 50\%$) | Low ($< £1,000$) | Automated re-engagement workflows |
| **Dormant Capital** | Low ($< 30\%$) | Low ($< £1,000$) | Low-touch background monitoring |

---

## 🏗️ Repository Architecture
celr-alpha-terminal/
├── data/                       # Raw input datasets
├── output/                     # Processed datasets and ML outputs
│   └── celr_ranked_assets.csv  # Calculated risk matrix dataset
├── src/                        # Modular processing & modeling scripts
│   ├── data_cleaning.py        # Data hygiene and ETL pipeline
│   ├── cohort_analysis.py      # LTV & cohort retention metrics
│   ├── predictive_models.py    # Machine learning classifier training
│   └── bav_matrix.py           # Asset valuation and tier classification
├── app.py                      # Interactive Plotly Dash dashboard app
├── requirements.txt            # Environment dependencies
└── README.md                   # Repository documentation

---

## ⚡ Quickstart & Local Installation

### Prerequisites
* Python 3.10+
* Virtual environment tool (`venv` or `conda`)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/your-username/celr-alpha-terminal.git](https://github.com/your-username/celr-alpha-terminal.git)
   cd celr-alpha-terminal


Create and Activate a Virtual Environment

Bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate



Install Dependencies

Bash
pip install -r requirements.txt


Launch the Terminal App

Bash
python app.py
Open http://127.0.0.1:8050 in your browser to interact with the dashboard.


