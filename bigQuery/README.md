# Steps to create
### Create BigQuery dataset
```
bq --location=us-west1 mk carbon_intensity
```


```
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  grafana/grafana
docker exec -it grafana sh
/usr/share/grafana $ grafana-cli --pluginUrl https://github.com/doitintl/bigquery-grafana/releases/download/2.0.3/doitintl-bigquery-datasource-2.0.3.zip plugins install doitintl-bigque
ry-datasource
docker restart grafana
```