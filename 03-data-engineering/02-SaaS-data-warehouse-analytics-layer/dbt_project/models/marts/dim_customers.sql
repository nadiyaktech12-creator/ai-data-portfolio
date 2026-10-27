{{ config(materialized='table') }}

SELECT
    c.customer_id,
    c.contact_id,
    c.email,
    hc.first_name,
    hc.last_name,
    hc.company,
    hc.lifecycle_stage,
    c.created_at AS customer_created_at,
    hc.created_at AS contact_created_at
FROM {{ ref('stg_stripe_customers') }} c
LEFT JOIN {{ ref('stg_hubspot_contacts') }} hc
    ON c.contact_id = hc.contact_id