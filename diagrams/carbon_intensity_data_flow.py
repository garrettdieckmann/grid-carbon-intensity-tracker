from diagrams import Cluster, Diagram
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.compute import Functions
from diagrams.gcp.analytics import Pubsub
from diagrams.gcp.analytics import Bigquery
from diagrams.onprem.monitoring import Grafana

with Diagram("Carbon Intensity Data Flow", show=False):
    grafana = Grafana("Grid Intensity Forecast")
    with Cluster("BigQuery"):
        carbon_intensity_raw_data = Bigquery("carbon_intensity.raw_data", labelloc="t")
        carbon_intensity_forecasts = Bigquery("carbon_intensity.forecasts", labelloc="b")

    Scheduler("WattTime_Emissions_Schedule") >> Pubsub("watttime-scrape-scheduling-topic", labelloc="t") >> Functions("watttime-emissions-index-scraper") >> Pubsub("watttime-scraped-data", labelloc="t") >> Functions("emissions-data-sinker") >> carbon_intensity_raw_data << grafana
    carbon_intensity_raw_data >> carbon_intensity_forecasts
    carbon_intensity_forecasts << grafana