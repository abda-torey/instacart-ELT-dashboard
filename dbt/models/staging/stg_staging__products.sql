
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
        int64_field_0 as product_id,
        string_field_1 as product_name,
        {{ dbt.safe_cast("int64_field_2", api.Column.translate_type("integer")) }} as aisle_id,
        {{ dbt.safe_cast("int64_field_3", api.Column.translate_type("integer")) }} as department_id
    from source
)

-- Return the cleaned data
select * from cleaned_products
-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}