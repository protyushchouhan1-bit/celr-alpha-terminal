import pandas as pd

def build_cohort_matrix(cleaned_csv, output_csv):
    print("Building Liquidation Horizon Matrix...")
    df = pd.read_csv(cleaned_csv, parse_dates=['InvoiceDate'])

    # Cohort Month
    df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')
    df['CohortMonth'] = df.groupby('Customer ID')['InvoiceDate'].transform('min').dt.to_period('M')

    # Calculate period index
    cohort_group = df.groupby(['CohortMonth', 'InvoiceMonth'])
    cohort_data = cohort_group.agg({'Customer ID': 'nunique'}).reset_index()

    cohort_data['Period'] = (cohort_data['InvoiceMonth'].dt.year - cohort_data['CohortMonth'].dt.year) * 12 + \
                            (cohort_data['InvoiceMonth'].dt.month - cohort_data['CohortMonth'].dt.month)

    # Pivot matrix
    cohort_pivot = cohort_data.pivot(index='CohortMonth', columns='Period', values='Customer ID')
    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_sizes, axis=0) * 100

    retention_matrix.to_csv(output_csv)
    print(f"Liquidation Horizon Matrix saved to {output_csv}.")

if __name__ == "__main__":
    build_cohort_matrix("output/cleaned_asset_ledger.csv", "output/cohort_matrix.csv")