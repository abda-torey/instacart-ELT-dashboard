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
        int64_field_0 as aisle_id,
        string_field_1 as aisle
    from source
)

-- Return the cleaned data
select * from cleaned_aisles
-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}