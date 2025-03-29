{{
    config(
        materialized='view'
    )
}}

with orders_data as (
  select *,
    row_number() over(partition by order_id, user_id) as rn
  from {{ source('staging', 'orders') }}
  where order_id is not null
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['order_id', 'user_id']) }} as order_key,
    {{ dbt.safe_cast("order_id", api.Column.translate_type("integer")) }} as order_id,
    {{ dbt.safe_cast("user_id", api.Column.translate_type("integer")) }} as user_id,

    -- order details
    {{ dbt.safe_cast("order_dow", api.Column.translate_type("integer")) }} as order_dow,
    {{get_day_description("order_dow")}} as day,
    {{ dbt.safe_cast("order_hour_of_day", api.Column.translate_type("integer")) }} as order_hour_of_day,
    cast(days_since_prior_order as numeric) as days_since_prior_order

from orders_data
where rn = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
