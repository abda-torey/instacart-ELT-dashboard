{#
    This macro returns the names of days alongside the day of the week (1 = Monday, ..., 7 = Sunday)
#}

{% macro get_day_description(day_of_week) -%}

    case {{ day_of_week }} 
        when 0 then 'Monday (1)'
        when 1 then 'Tuesday (2)'
        when 2 then 'Wednesday (3)'
        when 3 then 'Thursday (4)'
        when 4 then 'Friday (5)'
        when 5 then 'Saturday (6)'
        when 6 then 'Sunday (7)'
        else 'Invalid Day'
    end

{%- endmacro %}
