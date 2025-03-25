{{ config(
    materialized='table'
) }}

with source as (
    select *
    from {{ ref('stg_staging__aisles') }}
),

cleaned_aisles as (
    select
        aisle_id,
        aisle
    from source
)

select * from cleaned_aisles
