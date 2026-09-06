import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from lifetimes import BetaGeoFitter, GammaGammaFitter

def run_predictive_pipeline(cleaned_csv, bav_csv, output_csv):
    print("Loading ledger and valuation matrix...")
    df = pd.read_csv(cleaned_csv, parse_dates=['InvoiceDate'])
    bav = pd.read_csv(bav_csv)
    
    # 1. Churn / Liquidation Label (Inactivity > 90 days)
    bav['Is_Liquidated'] = (bav['Recency'] > 90).astype(int)
    
    # 2. Random Forest Liquidation Model
    print("Training Random Forest Liquidation Model...")
    X = bav[['Recency', 'Frequency', 'Monetary']]
    y = bav['Is_Liquidated']
    
    rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    rf.fit(X, y)
    bav['Liquidation_Probability'] = rf.predict_proba(X)[:, 1]
    
    # 3. Lifetimes BG/NBD + Gamma-Gamma Model
    print("Fitting BG/NBD and Gamma-Gamma Yield Models...")
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    summary = df.groupby('Customer ID').agg({
        'InvoiceDate': [
            lambda x: (x.max() - x.min()).days,            # Recency (T_rec)
            lambda x: (snapshot_date - x.min()).days      # Age (T)
        ],
        'Invoice': 'nunique',
        'Revenue': 'mean'
    })
    summary.columns = ['recency_days', 'T_days', 'frequency', 'monetary_value']
    summary['frequency'] = summary['frequency'] - 1  # Repeat purchases only
    
    bgf = BetaGeoFitter(penalizer_coef=0.01)
    bgf.fit(summary['frequency'], summary['recency_days'], summary['T_days'])
    
    repeat_buyers = summary[summary['frequency'] > 0]
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(repeat_buyers['frequency'], repeat_buyers['monetary_value'])
    
    # Calculate 12-Month Projected Asset Yield (PAY)
    summary['Projected_Asset_Yield'] = ggf.customer_lifetime_value(
        bgf, summary['frequency'], summary['recency_days'], summary['T_days'], summary['monetary_value'],
        time=12, discount_rate=0.01
    )
    
    # Merge and calculate CELR = LP x PAY
    bav = bav.merge(summary[['Projected_Asset_Yield']], on='Customer ID', how='left').fillna(0)
    bav['CELR'] = bav['Liquidation_Probability'] * bav['Projected_Asset_Yield']
    
    bav.sort_values(by='CELR', ascending=False, inplace=True)
    bav.to_csv(output_csv, index=False)
    print(f"Predictive models finished. CELR Ranked Assets saved to {output_csv}.")

if __name__ == "__main__":
    run_predictive_pipeline("output/cleaned_asset_ledger.csv", "output/bav_matrix.csv", "output/celr_ranked_assets.csv")