# Power BI implementation guide

Import `data/sales_data.csv` in Power BI Desktop (Get Data → Text/CSV). Set `order_date` to Date, `discount_pct` to Decimal Number and monetary columns to Fixed Decimal/Currency.

## Suggested model
Use Sales as the fact table. Optionally create Date, Product, Customer, Region and Channel dimensions in Power Query and relate each one-to-many to Sales.

## DAX measures
```DAX
Total Revenue = SUM(Sales[revenue])
Total Profit = SUM(Sales[profit])
Total Orders = DISTINCTCOUNT(Sales[order_id])
Unique Customers = DISTINCTCOUNT(Sales[customer_id])
Units Sold = SUM(Sales[quantity])
Profit Margin = DIVIDE([Total Profit], [Total Revenue])
Average Order Value = DIVIDE([Total Revenue], [Total Orders])
Revenue per Customer = DIVIDE([Total Revenue], [Unique Customers])
Repeat Customers = COUNTROWS(FILTER(VALUES(Sales[customer_id]), CALCULATE(DISTINCTCOUNT(Sales[order_id])) > 1))
Repeat Customer Rate = DIVIDE([Repeat Customers], [Unique Customers])
```

## Report pages
1. Executive Overview: KPI cards, monthly trend, category mix and region/channel slicers.
2. Product Performance: top products by revenue, units, profit and category.
3. Customer Insights: repeat customers, monthly active customers, AOV and customer segment.

Add slicers for date, region, category, channel and customer segment. Save the native report as `Business_Sales_Analytics.pbix`; Power BI Desktop is required.
