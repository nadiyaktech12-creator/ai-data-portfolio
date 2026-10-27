{{ config(materialized='table') }}

SELECT
    s.subscription_id,
    s.customer_id,
    s.plan,
    s.status,
    s.started_at,
    s.canceled_at,
    s.monthly_amount,
    CASE 
        WHEN s.status = 'active' THEN s.monthly_amount 
        ELSE 0 
    END AS current_mrr,
    dc.company,
    dc.lifecycle_stage
FROM {{ ref('stg_stripe_subscriptions') }} s
LEFT JOIN {{ ref('dim_customers') }} dc
    ON s.customer_id = dc.customer_id