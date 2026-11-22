WITH activity AS (
  SELECT DISTINCT user_pseudo_id,
         PARSE_DATE('%Y%m%d', event_date) AS d
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
),
first AS (
  SELECT user_pseudo_id, MIN(d) AS first_day
  FROM activity GROUP BY 1
)
SELECT
  DATE_TRUNC(f.first_day, WEEK) AS cohort_week,
  DIV(DATE_DIFF(a.d, f.first_day, DAY), 7) AS week_n,
  COUNT(DISTINCT a.user_pseudo_id) AS users
FROM activity a
JOIN first f USING (user_pseudo_id)
GROUP BY 1, 2
ORDER BY 1, 2;