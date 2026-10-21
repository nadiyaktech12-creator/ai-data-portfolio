{{ config(materialized='view') }}

SELECT
    order_id,
    customer_id,
    CAST(order_date AS DATE) AS order_date,
    product_category,
    quantity,
    unit_price,
    discount_pct,
    LOWER(status) AS status,
    region,
    total_amount,
    CURRENT_TIMESTAMP AS loaded_at
FROM {{ source('raw', 'orders') }}
WHERE order_id IS NOT NULL