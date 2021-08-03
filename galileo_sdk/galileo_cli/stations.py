from galileo_sdk import GalileoSdk
import pandas
import click
from halo import Halo
import pprint


def stations_cli(main, galileo: GalileoSdk):
    @main.group()
    def stations():
        """
        Complete station actions to start your running your first project.
        :return:
        """
        pass

    @stations.command()
    @click.argument("index", type=int, required=False)
    @click.option(
        "-i",
        "--id",
        type=str,
        multiple=True,
        help="Filter by station id, can provide multiple options.",
    )
    @click.option(
        "-n",
        "--name",
        type=str,
        multiple=True,
        help="Filter by station name, can provide multiple options.",
    )
    @click.option(
        "-m",
        "--mid",
        type=str,
        multiple=True,
        help="Filter by machine id, can provide multiple options.",
    )
    @click.option(
        "-u",
        "--user_role",
        type=str,
        multiple=True,
        help="Filter by user roles, can provide multiple options.",
    )
    @click.option(
        "-v",
        "--volume",
        type=str,
        multiple=True,
        help="Filter by volume id, can provide multiple options.",
    )
    @click.option(
        "-d",
        "--description",
        type=str,
        multiple=True,
        help="Filter by description, can provide multiple options.",
    )
    @click.option("--page", type=int, help="Filter by page number.")
    @click.option(
        "--items",
        type=int,
        help="Filter by number of items in the page.",
    )
    def ls(index, id, name, mid, user_role, volume, description, page, items):
        """
        List information about Stations available in your account.
        """
        spinner = Halo("Retrieving stations", spinner="dot").start()
        r = galileo.stations.list_stations(
            station_ids=list(id),
            names=list(name),
            lz_ids=list(mid),
            user_roles=list(user_role),
            volume_ids=list(volume),
            descriptions=list(description),
            page=page,
            items=items,
        )

        if len(r) == 0:
            spinner.stop()
            click.echo("No station matches that query.")
            return

        if isinstance(index, int):
            stations_list = r[index]
        else:
            stations_list = r

        stations_list = [station.__dict__ for station in stations_list]
        stations_df = pandas.json_normalize(stations_list)
        stations_df = stations_df[[
            "station_id", "name", "description", "users", "lz_ids", "volumes"
        ]]
        spinner.stop()
        click.echo(stations_df)

    @stations.command()
    @click.option(
        "-n",
        "--name",
        prompt="Name of station",
        required=True,
        type=str,
        help="Name of station.",
    )
    @click.option(
        "-d",
        "--description",
        required=True,
        prompt="Station Desciption",
        type=str,
        help="Description of station.",
    )
    @click.option(
        "-u",
        "--userid",
        multiple=False,
        type=str,
        help="Users to invite to station.",
    )
    def create(name, userid, description=''):
        """
        Create a new station.
        """

        if not userid:
            station = galileo.stations.create_station(name,
                                                      description=description)
        else:
            station = galileo.stations.create_station(name,
                                                      description=description,
                                                      user_ids=list(userid))

        station_df = pandas.json_normalize(station.__dict__)
        station_df = station_df[["stationid", "name", "description"]]
        click.echo(station_df)

    @stations.command()
    @click.option(
        "-s",
        "--sid",
        type=str,
        required=True,
        prompt="Station ID",
        help="Filter by station id, can provide multiple options.",
    )
    def users(sid):
        """
        List users in a Station.
        """
        spinner = Halo("Retrieving station users", spinner="dot").start()
        r = galileo.stations.list_stations(station_ids=[sid])

        if len(r) == 0:
            spinner.stop()
            click.echo("No station matches that query.")
            return
        users_list = r[0].users
        users_list = [user.__dict__ for user in users_list]
        users_df = pandas.json_normalize(users_list)
        spinner.stop()
        click.echo(users_df)

    @stations.command()
    @click.option(
        "-s",
        "--sid",
        type=str,
        required=True,
        prompt="Station ID",
        help="Filter by station id, can provide multiple options.",
    )
    @click.option(
        "-a",
        "--add",
        type=str,
        required=False,
        help=
        "List of Landing Zone ids to add to a Station (can accept multiple options).",
    )
    @click.option(
        "-r",
        "--remove",
        type=str,
        required=False,
        help=
        "List of Landing Zone ids to remove to a Station (can accept multiple options).",
    )
    def LZs(sid, add, remove):
        """
        List, add, and remove Landing Zones from a Station.
        """
        spinner = Halo("Retrieving station machines", spinner="dot").start()
        stations = galileo.stations.list_stations(station_ids=[sid])

        if len(stations) == 0:
            spinner.stop()
            click.echo("No station matches that query.")
            return

        if remove:
            if galileo.stations.remove_lz_from_station(sid, [remove]):
                click.echo(f"Removed LZ {remove} from station {sid}.")

        if add:
            if galileo.stations.add_lz_to_station(sid, [add]):
                click.echo(f"Added LZ {add} to station {sid}.")

        lz_list = stations[0].lz_ids
        spinner.stop()
        pp = pprint.PrettyPrinter(indent=2)
        click.echo(pp.pprint(lz_list))

    @stations.command()
    @click.option("-s",
                  "--station-id",
                  type=str,
                  required=True,
                  prompt="Station ID")
    @click.option("-r", "--role", type=str, required=True, default="launcher")
    @click.argument(
        "user-ids",
        nargs=-1,
        type=str,
        required=True,
    )
    def invite(station_id, role, user_ids):
        """
        Invite users in a Station.
        """
        spinner = Halo("Inviting users to station", spinner="dot").start()
        role_id = galileo.stations.get_station_roles(station_id,
                                                     names=[role])[0]
        for user in user_ids:
            try:
                spinner.stop()
                r = galileo.stations.invite_to_station(station_id, [user],
                                                       role_id.id)
                username = galileo.profiles.list_users(
                    user_ids=[user])[0].username
                station_name = galileo.stations.list_stations(
                    station_ids=[station_id])[0].name
                click.echo(
                    "Invited {name} to station {station_name} ({station_id}) with role {role_id}"
                    .format(name=username,
                            station_name=station_name,
                            station_id=station_id,
                            role_id=role))
            except Exception as e:
                spinner.stop()
                click.echo("Error", e)

    @stations.command()
    @click.option("-s",
                  "--station-id",
                  type=str,
                  required=True,
                  prompt="Station ID")
    @click.argument(
        "user-ids",
        nargs=-1,
        type=str,
        required=True,
    )
    def kick(station_id, user_ids):
        """
        Remove users from a Station.
        """
        spinner = Halo("Removing users from station", spinner="dot").start()
        for user in user_ids:
            try:
                spinner.stop()
                r = galileo.stations.remove_member_from_station(
                    station_id, user)
                username = galileo.profiles.list_users(
                    user_ids=[user])[0].username
                station_name = galileo.stations.list_stations(
                    station_ids=[station_id])[0].name
                click.echo(
                    "Removed {name} from station {station_name} ({station_id})"
                    .format(name=username,
                            station_name=station_name,
                            station_id=station_id))
            except Exception as e:
                spinner.stop()
                click.echo("Error", e)