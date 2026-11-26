-- 1. Monthly revenue and month-over-month growth
WITH m AS (SELECT strftime('%Y-%m',order_date) month,SUM(revenue) revenue FROM sales GROUP BY 1)
SELECT month,ROUND(revenue,2) revenue,ROUND(100.0*(revenue-LAG(revenue) OVER(ORDER BY month))/NULLIF(LAG(revenue) OVER(ORDER BY month),0),2) mom_growth_pct FROM m ORDER BY month;
-- 2. Top 10 products
SELECT product_name,category,SUM(quantity) units_sold,ROUND(SUM(revenue),2) revenue,ROUND(SUM(profit),2) profit FROM sales GROUP BY 1,2 ORDER BY revenue DESC LIMIT 10;
-- 3. Customer lifetime value
SELECT customer_id,COUNT(DISTINCT order_id) orders,ROUND(SUM(revenue),2) lifetime_revenue,MAX(order_date) last_order_date FROM sales GROUP BY 1 ORDER BY lifetime_revenue DESC;
-- 4. Region and channel
SELECT region,sales_channel,COUNT(DISTINCT order_id) orders,ROUND(SUM(revenue),2) revenue,ROUND(SUM(profit),2) profit FROM sales GROUP BY 1,2 ORDER BY revenue DESC;
-- 5. Category contribution
SELECT category,ROUND(SUM(revenue),2) revenue,ROUND(100.0*SUM(revenue)/(SELECT SUM(revenue) FROM sales),2) revenue_share_pct FROM sales GROUP BY 1 ORDER BY revenue DESC;
-- 6. Orders discounted above 10%
SELECT order_id,order_date,product_name,discount_pct,revenue,profit FROM sales WHERE discount_pct>0.10 ORDER BY order_date DESC;
