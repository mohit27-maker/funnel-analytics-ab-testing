WITH base AS (
  SELECT
    user_pseudo_id,
    (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS session_id,
    event_name,
    MIN(event_timestamp) AS ts
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE event_name IN ('view_item','add_to_cart','begin_checkout','purchase')
  GROUP BY user_pseudo_id, session_id, event_name
),
paths AS (
  SELECT user_pseudo_id, session_id,
         STRING_AGG(event_name, ' > ' ORDER BY ts) AS path
  FROM base
  GROUP BY user_pseudo_id, session_id
)
SELECT path,
       COUNT(*) AS sessions,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM paths
GROUP BY path
ORDER BY sessions DESC
LIMIT 15;