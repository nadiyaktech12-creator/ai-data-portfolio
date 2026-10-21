{{ config(materialized='table') }}

SELECT
    customer_id,
    COUNT(*) AS lifetime_orders,
    SUM(net_amount) AS lifetime_value,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date,
    COUNT(DISTINCT product_category) AS categories_purchased
FROM {{ ref('int_order_enriched') }}
WHERE is_completed = 1
GROUP BY 1