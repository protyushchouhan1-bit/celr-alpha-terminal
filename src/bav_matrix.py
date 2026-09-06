import pandas as pd

def build_bav_matrix(cleaned_ledger_path, output_path):
    print("Reading cleaned asset ledger...")
    df = pd.read_csv(cleaned_ledger_path, parse_dates=['InvoiceDate'])
    
    # Freeze analysis window 1 day after final transaction
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    # Compute base metrics: Recency, Frequency, Monetary
    bav = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'Invoice': 'nunique',
        'Revenue': 'sum'
    }).reset_index()
    
    bav.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']
    
    # Quintile Scoring (1-5)
    bav['R_Score'] = pd.qcut(bav['Recency'], 5, labels=[5, 4, 3, 2, 1])
    bav['F_Score'] = pd.qcut(bav['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    bav['M_Score'] = pd.qcut(bav['Monetary'], 5, labels=[1, 2, 3, 4, 5])
    
    # Map to Institutional Asset Tiers
    def segment_asset(row):
        r, f = int(row['R_Score']), int(row['F_Score'])
        if r >= 4 and f >= 4:
            return "Tier 1 Alpha Asset"
        elif r >= 3 and f >= 3:
            return "High-Yield Volatile"
        elif r <= 2 and f >= 3:
            return "Distressed Equity"
        else:
            return "Dormant Capital"
            
    bav['Asset_Tier'] = bav.apply(segment_asset, axis=1)
    
    bav.to_csv(output_path, index=False)
    print(f"BAV Matrix saved to {output_path} with {len(bav)} unique assets segmented.")

if __name__ == "__main__":
    build_bav_matrix("output/cleaned_asset_ledger.csv", "output/bav_matrix.csv")