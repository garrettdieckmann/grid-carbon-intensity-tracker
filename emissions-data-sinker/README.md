# Emissions Data Sinker Function
Google Cloud Function, which retrieves raw carbon intensity data from the intermediary Pub/Sub topic, and sinks those messages into a BigQuery table.

Carbon intensity data is published into a Pub/Sub topic by the [WattTime Emissions Index Scraper Function](../watttime-emissions-index-scraper/README.md).

## Steps to create
### Configure dependencies
* Create a Google Cloud Pub/Sub topic
* Create a Google Cloud Function, with the following configuration:
    * Uses a Python 3 runtime
    * Uses the `main.py` Python code from this folder
    * Configures a runtime environment variable:
        * `BIGQUERY_DESTINATION_TABLE` = BigQuery table to sink carbon intensity data to
            * Format example: `<project>.<dataset>.<table>`