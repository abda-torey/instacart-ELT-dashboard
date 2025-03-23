{{ config(
    materialized='table'
) }}

with source as (
    select *
    from {{ source('staging', 'departments') }}
),

cleaned_departments as (
    select
        department_id,
        department
    from source
)

select * from cleaned_departments;
