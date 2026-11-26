from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"data"/"sales_data.csv")
with sqlite3.connect(ROOT/"data"/"sales.db") as conn:
    conn.executescript((ROOT/"sql"/"schema.sql").read_text(encoding="utf-8"))
    df.to_sql("sales",conn,if_exists="replace",index=False)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id)")
print(f"Loaded {len(df):,} rows into data/sales.db")
