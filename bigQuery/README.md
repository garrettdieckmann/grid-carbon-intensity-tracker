# Steps to create
### Create BigQuery components
* Create the `carbon_intensity` dataset in the `us-west1` location
```
bq --location=us-west1 mk carbon_intensity
```

* Run the included .sql scripts
    * `carbon_intensity.raw_data.sql`: creates the BigQuery table to store raw data
    * `carbon_intensity.build_prediction_model.sql`: BigQueryML model, with forecasted carbon intensity values

### Visualize with Grafana
* Run Grafana, locally, in a Docker container
```
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  grafana/grafana
```
* Install the BigQuery Grafana Data Source (which is not packaged with the default Grafana Docker image):
```
$ docker exec -it grafana sh
/usr/share/grafana $ grafana-cli --pluginUrl https://github.com/doitintl/bigquery-grafana/releases/download/2.0.3/doitintl-bigquery-datasource-2.0.3.zip plugins install doitintl-bigque
ry-datasource
/usr/share/grafana $ exit
$ docker restart grafana
```
* Access Grafana @ `http://localhost:3000/`
* Load the [included dashboard](GrafanaDashboards/gridEmissionsIndex.json)