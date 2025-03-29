{{ config(
    materialized='table'
) }}

with source as (
    select *
    from {{ ref('stg_staging__orders') }}
),

dim_orders as (
    select
    order_key,
    order_id,
    user_id,
    order_dow,
    day,
    order_hour_of_day,
    days_since_prior_order
    from source
)

select * from dim_orders
