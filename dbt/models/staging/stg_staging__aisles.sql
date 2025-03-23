{{
    config(
        materialized='view'
    )
}}

with source as (
    -- Pull all columns from the aisles source table
    select * 
    from {{ source('staging', 'aisles') }}
),

cleaned_aisles as (
    -- Perform any necessary data transformations or cleaning here
    select
        -- identifiers
        aisle_id,
        aisle
    from source
)

-- Return the cleaned data
select * from cleaned_aisles;
-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}