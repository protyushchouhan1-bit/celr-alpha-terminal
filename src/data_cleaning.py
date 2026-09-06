import pandas as pd
import os

def clean_ledger(input_path, output_path):
    print("Ingesting raw dataset...")
    xls = pd.ExcelFile(input_path)
    
    # Load and combine both year tabs
    df1 = pd.read_excel(xls, 'Year 2009-2010')
    df2 = pd.read_excel(xls, 'Year 2010-2011')
    df = pd.concat([df1, df2], ignore_index=True)
    
    # Harmonization steps
    df_clean = df.dropna(subset=['Customer ID']).copy()
    df_clean = df_clean[~df_clean['Invoice'].astype(str).str.startswith('C')]
    df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['Price'] > 0)]
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    df_clean['Revenue'] = df_clean['Quantity'] * df_clean['Price']
    
    # Save clean dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned ledger saved to {output_path} with {len(df_clean)} records.")

if __name__ == "__main__":
    clean_ledger("data/Copy of online_retail_II.xlsx", "output/cleaned_asset_ledger.csv")