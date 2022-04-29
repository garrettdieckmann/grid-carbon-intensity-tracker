import base64
import json
from os import environ
from google.cloud import bigquery

# Receive the event, transform and write to BigQuery

def sink_scraped_data(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    scraped_data = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    bq_sink = BigQuerySink(environ.get('BIGQUERY_DESTINATION_TABLE')) # 'your-project.your_dataset.your_table'
    bq_sink.sink(scraped_data)

class BigQuerySink:
    def __init__(self, table_id):
        self.dest_table = bigquery.Table.from_string(table_id)
        self.client = bigquery.Client()

    def sink(self, data):
        errors = self.client.insert_rows_json(self.dest_table, self.raw_to_bq(data))
        for error in errors:
            print(f"Unable to insert rows: {error}")

    def raw_to_bq(self, data):
        row_to_insert = [{
            u"ba": data['ba'],
            u"point_time": data['point_time'],
            u"percent": data['percent']
        }]
        return row_to_insert