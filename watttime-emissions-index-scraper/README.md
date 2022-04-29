# WattTime Emissions Index Scraper Function
Google Cloud Function, which scrapes realtime carbon intensity data from the [WattTime Real-time Emissions Index API](https://www.watttime.org/api-documentation/#real-time-emissions-index).

Data is scraped on a recurring schedule, and published into an intermediary Pub/Sub topic.

Data in the intermediary Pub/Sub topic is retrieved by the [Emissions Data Sinker Function](../emissions-data-sinker/README.md).

## Steps to create
### Configure dependencies
* Create a Google Cloud Pub/Sub topic
* Create a Google Cloud Scheduler job, which:
    * Runs every 5 minutes
    * Publishes to the Pub/Sub topic created above
    * Has a message body with an array of Balancing Authority codes to collect carbon intensity data on
        * Example: ["SCL","NYISO_NYC","CAISO_SANDIEGO"] (1 message will be published for *each* BA - in this example, 3 messages will be published)
    * Has a message attribute with a `replyTo` key, which tells downstream systems where to publish the collected data
        * Format: `projects/<project-name>/topics/<topic-name>`
* Create 2 secrets in Google Cloud Secret Manager:
    1) WattTime API Username
    2) WattTime API Password
* Create a Google Cloud Function, with the following configuration:
    * Uses a Python 3 runtime
    * Uses the `main.py` Python code from this folder
    * Maps the 2 previously created Secrets as environment variables:
        * `WATTTIME_USERNAME` = WattTime API Username
        * `WATTTIME_PASSWORD` = WattTime API Password