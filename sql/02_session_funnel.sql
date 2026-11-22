WITH s AS (
  SELECT
    user_pseudo_id,
    (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS session_id,
    MAX(IF(event_name = 'view_item', 1, 0))      AS viewed,
    MAX(IF(event_name = 'add_to_cart', 1, 0))    AS carted,
    MAX(IF(event_name = 'begin_checkout', 1, 0)) AS checkout,
    MAX(IF(event_name = 'purchase', 1, 0))       AS bought
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  GROUP BY user_pseudo_id, session_id
)
SELECT
  COUNT(*)      AS sessions,
  SUM(viewed)   AS viewed,
  SUM(carted)   AS carted,
  SUM(checkout) AS checkout,
  SUM(bought)   AS bought
FROM s;