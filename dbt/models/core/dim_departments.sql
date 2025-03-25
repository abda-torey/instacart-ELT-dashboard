{{ config(
    materialized='table'
) }}

with source as (
    select *
    from {{ ref('stg_staging__departments') }}
),

cleaned_departments as (
    select
        department_id,
        department
    from source
)

select * from cleaned_departments
