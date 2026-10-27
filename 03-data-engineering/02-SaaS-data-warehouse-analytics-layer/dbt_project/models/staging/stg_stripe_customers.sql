{{ config(materialized='view') }}

SELECT
    customer_id,
    contact_id,
    LOWER(email) AS email,
    CAST(created_at AS TIMESTAMP) AS created_at
FROM {{ source('raw', 'stripe_customers') }}