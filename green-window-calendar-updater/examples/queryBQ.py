from pandas import to_datetime
from datetime import timedelta
from google.cloud import bigquery

bqclient = bigquery.Client()

# Download query results.
query_string = """
SELECT forecast_timestamp,
  forecast_value
FROM ML.FORECAST(MODEL carbon_intensity.relative_forecasts, STRUCT(864 AS horizon, 0.95 AS confidence_level))
-- forecast_timestamp is from now() until end of today()
where forecast_timestamp between 
    CURRENT_TIMESTAMP() -- now
  and
    TIMESTAMP(DATE_ADD(CURRENT_DATE(@tz), INTERVAL 1 DAY), @tz) -- remainder of today for given timezone
  and ba = @ba -- need this value somehow
"""
# TODO: If 'select distinct ba', then how get appropriate TZ for BA?

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("tz", "STRING", "America/Los_Angeles"),
        bigquery.ScalarQueryParameter("ba", "STRING", "SCL"),
    ]
)

dataframe = (
    bqclient.query(query_string, job_config=job_config)
    .result()
    .to_dataframe()
)

# Get Simple Moving Average over 2 hours.
dataframe['SMA'] = dataframe['forecast_value'].rolling(24).mean()
# Get row with smallest average
green_zone_endtime = dataframe[dataframe.SMA == dataframe.SMA.min()]

# Smallest average is the "end time" of the Green Zone.
# Can compute "start time" = (end_time - 2 hours)
green_zone_endtime = green_zone_endtime['forecast_timestamp'].values[0]
green_zone_endtime = to_datetime(green_zone_endtime).tz_localize('UTC').tz_convert('America/Los_Angeles')
print('Green Zone EndTime:')
print(green_zone_endtime)
print('Start time:')
print(green_zone_endtime - timedelta(hours=2))