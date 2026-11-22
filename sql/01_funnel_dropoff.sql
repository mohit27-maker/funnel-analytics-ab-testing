WITH stage_users AS (
  SELECT event_name, COUNT(DISTINCT user_pseudo_id) AS users
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE event_name IN ('session_start','view_item','add_to_cart','begin_checkout','purchase')
  GROUP BY event_name
),
ordered AS (
  SELECT
    CASE event_name
      WHEN 'session_start'  THEN 1
      WHEN 'view_item'      THEN 2
      WHEN 'add_to_cart'    THEN 3
      WHEN 'begin_checkout' THEN 4
      WHEN 'purchase'       THEN 5
    END AS step,
    event_name, users
  FROM stage_users
)
SELECT
  step, event_name, users,
  ROUND(100 * users / FIRST_VALUE(users) OVER (ORDER BY step), 1) AS pct_of_start,
  ROUND(100 * (1 - users / LAG(users) OVER (ORDER BY step)), 1)   AS dropoff_pct
FROM ordered
ORDER BY step;