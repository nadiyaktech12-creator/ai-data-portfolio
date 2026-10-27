{{ config(materialized='view') }}

SELECT
    contact_id,
    LOWER(email) AS email,
    first_name,
    last_name,
    company,
    CAST(created_at AS TIMESTAMP) AS created_at,
    LOWER(lifecycle_stage) AS lifecycle_stage
FROM {{ source('raw', 'hubspot_contacts') }}