{{ config(materialized='table') }}

WITH raw_cars AS (
    SELECT * FROM {{ source('external_api', 'src_cars') }}
)

SELECT 
    id_car,
    UPPER(plate) AS plate,
    model_name,
    COALESCE(brand_name, 'NOT DEFINED') as brand_name,
    -- Handling the NULLs we saw in your data
    COALESCE(year, 'NOT DEFINED') AS model_year,
    COALESCE(color_name, 'NOT DEFINED') AS color,
    -- Fixing the 20k Celta (filtering out outliers)
    CAST(price AS DECIMAL(10,2)) AS price_per_day
FROM raw_cars
WHERE 1 = 1 
AND CAST(price AS DECIMAL) < 10000
AND id_car IS NOT NULL