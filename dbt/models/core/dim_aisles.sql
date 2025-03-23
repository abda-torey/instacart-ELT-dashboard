{{ config(
    materialized='table'
) }}

with source as (
    select *
    from {{ source('staging', 'aisles') }}
),

cleaned_aisles as (
    select
        aisle_id,
        aisle
    from source
)

select * from cleaned_aisles;
