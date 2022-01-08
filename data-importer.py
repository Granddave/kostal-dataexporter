#!/usr/bin/env python3

import argparse
from datetime import datetime
from io import StringIO
import os
from numpy import log

import pandas as pd
from influxdb_client import InfluxDBClient as InfluxDB2Client
from influxdb_client.client.write_api import SYNCHRONOUS


def _insert_data_into_influxdb2(df):
    influxClient = InfluxDB2Client(
        url=os.environ["INFLUXDB_URL"],
        token=os.environ["INFLUXDB_TOKEN"],
    )

    write_api = influxClient.write_api(write_options=SYNCHRONOUS)
    write_api.write(
        os.environ["INFLUXDB_BUCKET"],
        os.environ["INFLUXDB_ORG"],
        record=df,
        data_frame_measurement_name="pvwr",
    )


def parse_measurements(args, logdata_df):
    columns = {
        "DC1 U": "pv_generator_dc_input_1_voltage",
        "DC1 I": "pv_generator_dc_input_1_current",
        "DC1 P": "pv_generator_dc_input_1_power",
        "DC2 U": "pv_generator_dc_input_2_voltage",
        "DC2 I": "pv_generator_dc_input_2_current",
        "DC2 P": "pv_generator_dc_input_2_power",
        "DC3 U": "pv_generator_dc_input_3_voltage",
        "DC3 I": "pv_generator_dc_input_3_current",
        "DC3 P": "pv_generator_dc_input_3_power",
        "AC1 U": "grid_phase_1_voltage",
        "AC1 I": "grid_phase_1_current",
        "AC1 P": "grid_phase_1_power",
        "AC2 U": "grid_phase_2_voltage",
        "AC2 I": "grid_phase_2_current",
        "AC2 P": "grid_phase_2_power",
        "AC3 U": "grid_phase_3_voltage",
        "AC3 I": "grid_phase_3_current",
        "AC3 P": "grid_phase_3_power",
        "AC F": "grid_grid_parameters_grid_frequency",
        # NOTE: These are disabled since my inverter can't sample these values and thus are untested
        # "SC1 P": "house_phase_selective_home_consumption_phase_1",
        # "SC2 P": "house_phase_selective_home_consumption_phase_2",
        # "SC3 P": "house_phase_selective_home_consumption_phase_3",
        # NOTE: There might be more columns that map to a dxs value...
    }

    df = logdata_df.filter(columns.keys())
    df.rename(columns=columns, inplace=True)
    df = df[df["pv_generator_dc_input_1_voltage"] > 0]  # Skip empty rows
    df["grid_grid_parameters_output_power"] = (
        logdata_df["AC1 P"] + logdata_df["AC2 P"] + logdata_df["AC3 P"]
    )
    df["timestamp"] = pd.to_datetime(logdata_df["Zeit"], unit="s").dt.tz_localize(
        args.timezone
    )
    df.set_index("timestamp", inplace=True)
    df = df.loc[args.start : args.end]
    return df


def _read_file(filepath):
    with open(filepath, mode="r") as fh:
        return fh.read().split("\n")


def parse_file(filepath):
    file_content = _read_file(filepath)

    # Skip the first rows with metadata
    csv_table = "\n".join(file_content[6:])
    return pd.read_csv(StringIO(csv_table), sep="\t")


def _parse_args():
    parser = argparse.ArgumentParser(description="Kostal log data importer")
    parser.add_argument(
        "filepath",
        type=str,
        default="LogData.dat",
        help="log file exported via the kostal web interface",
    )
    parser.add_argument(
        "--timezone",
        "-tz",
        type=str,
        default=datetime.now().astimezone().tzinfo,
        help='timezone string. The hosts timezone by default. e.g. "UTC" or "Europe/Stockholm"',
    )
    parser.add_argument("--start", type=str, help="start date. format: yyyy-mm-dd")
    parser.add_argument("--end", type=str, help="end date. format: yyyy-mm-dd")
    return parser.parse_args()


def main():
    args = _parse_args()
    logdata_df = parse_file(args.filepath)
    df = parse_measurements(args, logdata_df)

    print(
        f"Found {len(df)} measurements between "
        f"'{df.first_valid_index()}' and '{df.last_valid_index()}'"
    )
    ans = input("Insert data into InfluxDB2? [y/N]: ")
    if "y" in ans.lower():
        _insert_data_into_influxdb2(df)
        print("Done")


if __name__ == "__main__":
    main()
