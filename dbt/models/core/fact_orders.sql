-- models/fact_orders.sql

{{
    config(
        materialized='table'
    )
}}

with orders_data as (
    -- Get the base orders data from the staging table
    select
        order_id,
        user_id,
        order_dow,
        order_hour_of_day,
        days_since_prior_order
    from {{ source('staging', 'orders') }}
),

order_products_prior_data as (
    -- Join order_products_prior data to get details about the products in prior orders
    select
        op.order_id,
        count(op.product_id) as total_products,
        sum(case when op.reordered = 1 then 1 else 0 end) as total_reordered_products
    from {{ ref('stg_staging__order_products_prior') }} op
    group by op.order_id
),

enriched_orders as (
    -- Join the prior products data with the orders data
    select
        o.order_id,
        o.user_id,
        o.order_dow,
        o.order_hour_of_day,
        o.days_since_prior_order,

        -- Enrich with product data
        coalesce(op.total_products, 0) as total_products,
        coalesce(op.total_reordered_products, 0) as total_reordered_products
    from orders_data o
    left join order_products_prior_data op on o.order_id = op.order_id
)

select * from enriched_orders;

-- dbt build --select fact_orders
