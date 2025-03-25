-- models/staging/instacart/stg_instacart__order_products_prior.sql

{{
    config(
        materialized='view'
    )
}}

with source as (
    -- Pull all columns from the order_products_prior source table
    select * 
    from {{ source('staging', 'order_products_prior') }}
),

cleaned_order_products_prior as (
    -- Perform any necessary data transformations or cleaning here
    select
        -- identifiers
        int64_field_0 as order_id,
        {{ dbt.safe_cast("int64_field_1", api.Column.translate_type("integer")) }} as product_id,
        {{ dbt.safe_cast("int64_field_2", api.Column.translate_type("integer")) }} as add_to_cart_order,
        {{ dbt.safe_cast("int64_field_3", api.Column.translate_type("integer")) }} as reordered
    from source
)

-- Return the cleaned data
select * from cleaned_order_products_prior
-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}