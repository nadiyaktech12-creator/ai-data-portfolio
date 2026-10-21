{{ config(materialized='table') }}

SELECT
    order_id,
    customer_id,
    order_date,
    product_category,
    quantity,
    unit_price,
    discount_pct,
    status,
    region,
    total_amount,
    quantity * unit_price AS gross_amount,
    total_amount AS net_amount,
    CASE 
        WHEN status = 'completed' THEN 1 
        ELSE 0 
    END AS is_completed,
    loaded_at
FROM {{ ref('stg_orders') }}