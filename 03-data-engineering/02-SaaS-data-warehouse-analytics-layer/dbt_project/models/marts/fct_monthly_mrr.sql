{{ config(materialized='table') }}

SELECT
    DATE_TRUNC('month', started_at) AS month,
    plan,
    COUNT(*) AS active_subscriptions,
    SUM(current_mrr) AS total_mrr
FROM {{ ref('fct_subscriptions') }}
WHERE status = 'active'
GROUP BY 1, 2
ORDER BY 1, 2