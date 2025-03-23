{{ config(
    materialized='table'
) }}

with source as (
    select *
    from {{ source('staging', 'orders') }}
),

dim_orders as (
    select
    order_id,
    user_id,
    eval_set,
    order_number,
    order_dow,
    order_hour_of_day,
    days_since_prior_order
    from source
)

select * from dim_orders;
