# Kostal Piko Dataexporter

This Python scripts grabs content of the REST API of a [Kostal PIKO inverter](
https://www.kostal-solar-electric.com/en-gb/products/solar-inverter/piko-12-20)
and exports the data either to PostgreSQL Database, InfluxDB v1 or InfluxDB v2.

The API is undocumented and can be discovered by watching the network traffic between
a web browser and the inverter for e.g. `$HOST/#/current-values/pv-generator`

## Setup

 * PostgreSQL:
  * Generate the database schema with `python kostal-piko-dataexport.py --generate-schema [--piko-model MODEL]`
  * Import the `init.sql` into your database
 * InfluxDB: Create Database (eg `pv`)
 * Set environment variables with the relevant details
  * `KOSTAL_USERNAME`
  * `KOSTAL_PASSWORD`
  * `KOSTAL_HOST`
  * `KOSTAL_PIKO_MODEL` (optional, overrides `--piko-model`)
  * For PostgreSQL:
    * `DB_HOST`
    * `DB_PORT`
    * `DB_NAME`
    * `DB_USER`
    * `DB_PASSWORD`
  * For InfluxDB (1.x):
    * `INFLUXDB_HOST`
    * `INFLUXDB_PORT`
    * `INFLUXDB_NAME`
    * `INFLUXDB_USER`
    * `INFLUXDB_PASSWORD`
  * For InfluxDB (2.x):
    * `INFLUXDB_ORG`
    * `INFLUXDB_BUCKET`
    * `INFLUXDB_URL`
    * `INFLUXDB_TOKEN`
 * Run `python kostal-piko-dataexport.py`
    * `--influx {0,1}` Export to InfluxDB v1 (optional, default: `0`)
    * `--influx2 {0,1}` Export to InfluxDB v2 (optional, default: `1`)
    * `--postgres {0,1}` Export to PostgreSQL (optional, default: `0`)
    * `--generate-schema` Generate PostgreSQL schema and exit
    * `--piko-model {7,15}` Set PIKO model. Sets which metrics to scrape (optional, default: `7`)
    * `--oneshot` Scrape data, print to stdout and exit

There's also a Docker Image available on [Docker Hub](https://hub.docker.com/r/svijee/kostal-dataexporter).

## Grafana

By logging the data with this script it's easily possible to create a nice
Grafana Dashboard to display some of the interesting data:

![My dashboard on a sunny day in Germany](https://raw.githubusercontent.com/svijee/kostal-dataexporter/master/img/grafana-dashboard.png)

You can import the [dashboard-postgresql.json](dashboard-postgresql.json) for PostgreSQL and/or [dashboard-influx.json](dashboard-influx.json)
to use it in your Grafana instance.

## Note

This is just a quick-and-dirty script to grab to content of the REST-API of my
Kostal Piko 7.0 Inverter. This might be usable on other Inverters aswell.

The difference between supplying 7 vs 15 to `--piko-model` is that 15 adds
metrics for two additional dc input as well as two metrics that were not used in
the original exporter script. The two previously unused metrics are disabled by
default for backwards compatability.
