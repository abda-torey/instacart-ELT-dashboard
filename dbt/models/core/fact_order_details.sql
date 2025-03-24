-- models/fact_order_details.sql
{{ config(
    enabled = false
) }}
with order_prior as (
    select
        op.order_id,
        op.product_id,
        op.add_to_cart_order,
        op.reordered
    from {{ source('instacart', 'order_prior') }} op
),

orders as (
    select
        o.order_id,
        o.user_id,
        o.order_number,
        o.order_dow,
        o.order_hour_of_day,
        o.days_since_prior_order
    from {{ source('instacart', 'orders') }} o
),

-- Instead of querying product details from the raw source table, we will reference the product dimension table
product_details as (
    select
        dp.product_id,
        dp.product_name,
        dp.aisle_id,
        da.aisle_name,
        dp.department_id,
        dd.department_name
    from {{ ref('dim_products') }} dp
    left join {{ ref('dim_aisles') }} da on dp.aisle_id = da.aisle_id
    left join {{ ref('dim_departments') }} dd on dp.department_id = dd.department_id
)

select
    op.order_id,
    o.user_id,
    op.product_id,
    pd.product_name,
    op.add_to_cart_order,
    op.reordered,
    o.order_number,
    o.order_dow,
    o.order_hour_of_day,
    o.days_since_prior_order,
    pd.aisle_name,
    pd.department_name
from order_prior op
join orders o on op.order_id = o.order_id
join product_details pd on op.product_id = pd.product_id
