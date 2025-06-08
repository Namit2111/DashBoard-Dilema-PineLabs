import pandas as pd
from sqlalchemy import create_engine

# Create a local SQLite .db file
engine = create_engine("sqlite:///merchant_insights.db")

# CSV file paths
settlement_file = "data/settlement_data.csv"
refund_file = "data/txn_refunds.csv"
support_file = "data/support_data.csv"

# Read and load Settlement Data
settlement_df = pd.read_csv(settlement_file,encoding="utf-8")
settlement_df.columns = [col.lower().strip().replace(" ", "_") for col in settlement_df.columns]
settlement_df.to_sql("settlement_data", engine, if_exists="replace", index=False)
print("✅ settlement_data table loaded.")

# Refund Data
refund_df = pd.read_csv(refund_file,encoding="utf-8")
refund_df.columns = [col.lower().strip().replace(" ", "_") for col in refund_df.columns]
refund_df.to_sql("refund_data", engine, if_exists="replace", index=False)
print("✅ refund_data table loaded.")

# Support Data
support_df = pd.read_csv(support_file, encoding="latin-1")
support_df.columns = [col.lower().strip().replace(" ", "_") for col in support_df.columns]
support_df.to_sql("support_data", engine, if_exists="replace", index=False)
print("✅ support_data table loaded.")
