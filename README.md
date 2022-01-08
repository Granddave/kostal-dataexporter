# Kostal Piko Dataexporter

This Python scripts grabs content of the REST API of a [Kostal PIKO inverter](
https://www.kostal-solar-electric.com/en-gb/products/solar-inverter/piko-12-20)
and exports the data either to PostgreSQL Database, InfluxDB v1 or InfluxDB v2.

The API is undocumented and can be discovered by watching the network traffic between
a web browser and the inverter for e.g. `$HOST/#/current-values/pv-generator`

## Setup

 * PostgreSQL: Import the `init.sql` into your Database
 * InfluxDB: Create Database (eg `pv`)
 * Set environment variables with the relevant details
  * `KOSTAL_USERNAME`
  * `KOSTAL_PASSWORD`
  * `KOSTAL_HOST`
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
    * `--influx 1` (on, optional) or `--influx 0` (off, optional)
    * `--influx2 1` (on, default) or `--influx 0` (off, optional)
    * `--postgres 1` (on, optional) or `--postgres 0` (off, default)
    * `--interval {seconds}` Scrape interval (default: 30)
    * `--oneshot` Scrape data, print to stdout and exit

There's also a Docker Image available on [Docker Hub](https://hub.docker.com/r/svijee/kostal-dataexporter).

## Grafana

By logging the data with this script it's easily possible to create a nice
Grafana Dashboard to display some of the interesting data:

![My dashboard on a sunny day in Germany](https://raw.githubusercontent.com/svijee/kostal-dataexporter/master/img/grafana-dashboard.png)

You can import the [dashboard-postgresql.json](dashboard-postgresql.json) for
PostgreSQL, [dashboard-influx.json](dashboard-influx.json) for influxdb v1 or
[dashboard-influxdb2.json](dashboard-influxdb2.json) to use it in your Grafana
instance.

## A note on compatability

This is just a quick-and-dirty script to grab to content of the REST-API
served by the Kostal Piko inverter.

Tested inverters:

* Kostal Piko 7
* Kostal Piko 15

Might work on other models as well.