{{ config(
    materialized='table'
) }}

with source as (
    select *
    from {{ source('staging', 'products') }}
),

cleaned_products as (
    select
        product_id,
        product_name,
        aisle_id,
        department_id
    from source
)

select * from cleaned_products;
