{{
    config(
        materialized='view'
    )
}}

with source as (
    -- Pull all columns from the departments source table
    select * 
    from {{ source('staging', 'departments') }}
),

cleaned_departments as (
    -- Perform any necessary data transformations or cleaning here
    select
        -- identifiers
        department_id,
        department
    from source
)

-- Return the cleaned data
select * from cleaned_departments;
-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}