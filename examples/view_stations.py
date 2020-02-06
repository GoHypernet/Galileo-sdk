#! /usr/bin/env python3
import argparse
import getpass
import json
import sys
from typing import Optional

from src import GalileoSdk


def main(
    username: Optional[str] = None,
    password: Optional[str] = None,
    access_token: Optional[str] = None,
    refresh_token: Optional[str] = None,
    config: str = None,
):
    galileo = GalileoSdk(
        username=username,
        password=password,
        auth_token=access_token,
        refresh_token=refresh_token,
        config=config,
    )
    stations_list = galileo.stations.list_stations()

    while True:
        print("\n===STATIONS===")
        for index, station in enumerate(stations_list["stations"]):
            name = station["name"]
            print(f"[{index}] {name}")

        station = ""
        while not isinstance(station, int):
            station = input("Which station do you want to view? ")
            station = int(station)

        print("\n===STATION_DETAILS===")
        print(json.dumps(stations_list["stations"][station], indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="View station details")

    parser.add_argument(
        "--username", default="", help="Username for login", type=str, required=False
    )

    parser.add_argument(
        "--password", default="", help="Password for username", type=str, required=False
    )

    parser.add_argument(
        "--config",
        default="production",
        help="Must be either in 'production' mode or 'development' mode",
        type=str,
        required=False,
    )

    args = sys.argv[1:]
    args = parser.parse_args(args)

    if not args.username:
        args.username = input("Username: ")

    if args.username and not args.password:
        args.password = getpass.getpass("Password: ")
    elif args.access_token and not args.refresh_token:
        args.refresh_token = input("Refresh_token: ")

    return vars(args)


if __name__ == "__main__":
    main(**parse_args())
