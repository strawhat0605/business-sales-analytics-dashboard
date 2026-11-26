from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"data"/"sales_data.csv",parse_dates=["order_date"])
df["month"]=df.order_date.dt.to_period("M").astype(str)
monthly=df.groupby("month",as_index=False).agg(Orders=("order_id","nunique"),Revenue=("revenue","sum"),Profit=("profit","sum"))
products=df.groupby(["product_name","category"],as_index=False).agg(Units=("quantity","sum"),Revenue=("revenue","sum"),Profit=("profit","sum")).sort_values("Revenue",ascending=False)
regions=df.groupby("region",as_index=False).agg(Orders=("order_id","nunique"),Revenue=("revenue","sum"),Profit=("profit","sum"))
customers=df.groupby("customer_id",as_index=False).agg(Orders=("order_id","nunique"),Revenue=("revenue","sum"),Last_Order=("order_date","max"))
dictionary=pd.DataFrame({"Column":df.columns,"Description":["Unique order identifier","Order date","Customer identifier","Product","Category","Units sold","Unit selling price","Discount fraction","Net revenue","Cost","Profit","Sales region","Sales channel","Customer segment","Calendar month"]})
out=ROOT/"data"/"sales_analysis.xlsx"
with pd.ExcelWriter(out,engine="openpyxl") as writer:
    for name,frame in [("Sales_Data",df),("Monthly_Summary",monthly),("Product_Performance",products),("Region_Summary",regions),("Customer_Summary",customers),("Data_Dictionary",dictionary)]:
        frame.to_excel(writer,sheet_name=name,index=False)
    for ws in writer.book.worksheets:
        ws.freeze_panes="A2"; ws.auto_filter.ref=ws.dimensions
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width=min(max(max(len(str(c.value or "")) for c in col)+2,12),32)
print(f"Created {out}")
