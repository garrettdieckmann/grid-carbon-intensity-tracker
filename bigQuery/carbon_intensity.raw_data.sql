/*
    Create the scrape/raw data table
*/
CREATE TABLE `carbon_intensity.raw_data`
(
  ba STRING NOT NULL OPTIONS(description="Balancing Authority"),
  point_time TIMESTAMP NOT NULL OPTIONS(description="Point in time of percentage calculation"),
  percent INT64 NOT NULL OPTIONS(description="relative realtime marginal emissions intensity")
)
PARTITION BY TIMESTAMP_TRUNC(_PARTITIONTIME, DAY)
OPTIONS(
  require_partition_filter=true
);