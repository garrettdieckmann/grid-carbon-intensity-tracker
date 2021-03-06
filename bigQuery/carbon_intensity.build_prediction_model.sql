CREATE OR REPLACE PROCEDURE carbon_intensity.build_prediction_models()
BEGIN
    /*
    Create percentage-based ARIMA model
    */
    CREATE OR REPLACE MODEL `carbon_intensity.relative_forecasts` OPTIONS(
        MODEL_TYPE='ARIMA_PLUS',
        time_series_timestamp_col='point_time',
        time_series_data_col='percent',
        time_series_id_col='ba',
        horizon=864) AS
    SELECT
        point_time,
        percent,
        ba
    FROM
        `carbon_intensity.raw_data`
    WHERE DATE(_PARTITIONTIME) > DATE_SUB(CURRENT_DATE(), INTERVAL 1 WEEK) -- just last 1 week
  ; -- end

    /*
    Create moer-based ARIMA model
    */
    CREATE OR REPLACE MODEL `carbon_intensity.moer_forecasts` OPTIONS(
        MODEL_TYPE='ARIMA_PLUS',
        time_series_timestamp_col='point_time',
        time_series_data_col='moer',
        time_series_id_col='ba',
        horizon=864) AS
    SELECT
        point_time,
        moer,
        ba
    FROM
        `carbon_intensity.raw_data`
    WHERE DATE(_PARTITIONTIME) > DATE_SUB(CURRENT_DATE(), INTERVAL 1 WEEK) -- just last 1 week
        AND moer IS NOT NULL
  ; -- end
END
;
-- Execute procedure via: CALL carbon_intensity.build_prediction_models();