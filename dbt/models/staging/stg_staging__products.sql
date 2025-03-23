
{{
    config(
        materialized='view'
    )
}}

with source as (
    -- Pull all columns from the products source table
    select * 
    from {{ source('staging', 'products') }}
),

cleaned_products as (
    -- Perform any necessary data transformations or cleaning here
    select
        -- identifiers
        product_id,
        product_name,
        {{ dbt.safe_cast("aisle_id", api.Column.translate_type("integer")) }} as aisle_id,
        {{ dbt.safe_cast("department_id", api.Column.translate_type("integer")) }} as department_id
    from source
)

-- Return the cleaned data
select * from cleaned_products;
-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}