{{ config(materialized='view') }}

SELECT
    subscription_id,
    customer_id,
    LOWER(plan) AS plan,
    LOWER(status) AS status,
    CAST(started_at AS TIMESTAMP) AS started_at,
    CAST(canceled_at AS TIMESTAMP) AS canceled_at,
    monthly_amount
FROM {{ source('raw', 'stripe_subscriptions') }}