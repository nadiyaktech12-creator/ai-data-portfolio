{{ config(materialized='table') }}

SELECT
    order_date,
    product_category,
    region,
    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,
    SUM(net_amount) AS total_revenue,
    AVG(net_amount) AS avg_order_value,
    SUM(CASE WHEN is_completed = 1 THEN net_amount ELSE 0 END) AS completed_revenue
FROM {{ ref('int_order_enriched') }}
GROUP BY 1, 2, 3