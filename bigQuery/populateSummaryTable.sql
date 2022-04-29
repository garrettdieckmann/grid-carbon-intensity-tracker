CREATE OR REPLACE PROCEDURE WattTime.populateSummaryTable()
BEGIN
    /*
    Create ARIMA model
    */
    CREATE OR REPLACE MODEL
    `WattTime.predictions` OPTIONS(MODEL_TYPE='ARIMA_PLUS',
        time_series_timestamp_col='point_time',
        time_series_data_col='percent',
        time_series_id_col='ba',
        horizon=864) AS
    SELECT
    point_time,
    percent,
    ba
    FROM
    `WattTime.scrapedData`
    WHERE
    DATE(_PARTITIONTIME) > DATE_SUB(CURRENT_DATE(), INTERVAL 1 WEEK) -- just last 1 week
  ; -- end
  
    /*
        Query model to get top 5 times for next 3 days
    */
    SELECT t.ba,
    t.forecast_timestamp,
    t.forecast_value
    FROM (
    SELECT
        ba,
        forecast_timestamp,
        forecast_value,
        ROW_NUMBER() OVER (PARTITION BY ba, DATE(forecast_timestamp) ORDER BY forecast_value ASC) AS seqnum
    FROM
        ML.FORECAST(MODEL WattTime.predictions, STRUCT(864 AS horizon, 0.95 AS confidence_level)) -- horizon of 864 is 3 days of 5 minute measurements
    WHERE
        DATE(forecast_timestamp) < DATE_ADD(CURRENT_DATE(), INTERVAL 3 DAY) -- Only next 3 days
    ) AS t
    WHERE
    t.seqnum <= 5 -- limit to "top" 5 forecasted times
    ORDER BY
    t.forecast_timestamp,
    t.forecast_value
    -- TODO: Needs to insert somewhere!
  ;
END
;
-- Execute procedure via: CALL WattTime.populateSummaryTable();