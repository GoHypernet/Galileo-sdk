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
        "--items", type=int, help="Filter by number of items in the page.",
    )
    def ls(index, id, name, mid, user_role, volume, description, page, items):
        """
        List stations.
        """
        spinner = Halo("Retrieving stations", spinner="dot").start()
        r = galileo.stations.list_stations(
            stationids=list(id),
            names=list(name),
            mids=list(mid),
            user_roles=list(user_role),
            volumeids=list(volume),
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
        stations_df = stations_df[
            ["stationid", "name", "description", "users", "mids", "volumes"]
        ]
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
        prompt="Description of station",
        type=str,
        help="Description of station.",
    )
    @click.option(
        "-u",
        "--userid",
        multiple=True,
        prompt="User ID to invite",
        type=str,
        help="Users to invite to station.",
    )
    def create(name, description, userid):
        """
        Create a station.
        """
        station = galileo.stations.create_station(name, description, list(userid))[
            "station"
        ]
        station_df = pandas.json_normalize(station.__dict__)
        station_df = station_df[
            ["stationid", "name", "description", "users", "volumes"]
        ]
        click.echo(station_df)

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-u",
        "--userid",
        type=str,
        prompt="User ID to invite",
        required=True,
        multiple=True,
        help="Userids to invite, can provide multiple options.",
    )
    def invite(id, userid):
        """
        Invite user(s) to station.
        """
        if galileo.stations.invite_to_station(id, list(userid)):
            click.echo(f"Invited {userid} to station {id}!")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    def accept_invite(id):
        """
        Accept a station invite.
        """
        if galileo.stations.accept_station_invite(id):
            click.echo(f"Station invite to {id} accepted!")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    def reject_invite(id):
        """
        Reject a station invite.
        """
        if galileo.stations.reject_station_invite(id):
            click.echo(f"Station invite to {id} rejected.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    def request(id):
        """
        Request to join a station.
        """
        if galileo.stations.request_to_join(id):
            click.echo(f"Requested to join station {id}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-u",
        "--userid",
        type=str,
        prompt="User ID to approve",
        multiple=True,
        required=True,
        help="Approved userids, can provide multiple options.",
    )
    def approve_request(id, userid):
        """
        Approve user(s) to join a station (only if owner or admin).
        """
        if galileo.stations.approve_request_to_join(id, list(userid)):
            click.echo(f"Approved {userid} request(s) to join station {id}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-u",
        "--userid",
        type=str,
        prompt="User ID to reject",
        multiple=True,
        required=True,
        help="Rejected userids, can provide multiple options.",
    )
    def reject_request(id, userid):
        """
        Reject user(s) from joining a station (only if owner or admin).
        """
        if galileo.stations.reject_request_to_join(id, list(userid)):
            click.echo(f"Rejected {userid} request(s) to join station {id}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    def leave_station(id):
        """
        Leave a station.
        """
        if galileo.stations.leave_station(id):
            click.echo(f"Leaving station {id}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-u",
        "--userid",
        prompt="User ID to remove",
        type=str,
        required=True,
        help="Remove by userids, can provide multiple options.",
    )
    def remove_member(id, userid):
        """
        Remove a member from the station.
        """
        if galileo.stations.remove_member_from_station(id, userid):
            click.echo(f"Removed member {userid} from station {id}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    def delete_station(id):
        """
        Delete a station you own.
        """
        if galileo.stations.delete_station(id):
            click.echo(f"Deleted station {id}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-m",
        "--mid",
        type=str,
        prompt="Machine ID to add",
        required=True,
        help="Machine to add to station.",
    )
    def add_machines(id, mid):
        """
        Add machine(s) to a station.
        """
        if galileo.stations.add_machines_to_station(id, [mid]):
            click.echo(f"Added machines {mid} to station {id}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-m",
        "--mid",
        type=str,
        prompt="Machine ID to remove",
        required=True,
        help="List of machines to remove from station, can provide multiple options.",
    )
    def remove_machines(id, mid):
        """
        Remove machines from a station.
        """
        if galileo.stations.remove_machines_from_station(id, [mid]):
            click.echo(f"Removed machines {mid} from station {id}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-n",
        "--name",
        type=str,
        prompt="Volume name",
        required=True,
        help="Volume's name.",
    )
    @click.option(
        "-m",
        "--mountpath",
        type=str,
        prompt="Mount path",
        required=True,
        help="Mount path.",
    )
    @click.option(
        "-a",
        "--access",
        type=str,
        prompt="Access (r) or (rw)",
        required=True,
        help="Access permissions: either 'r' or 'rw'.",
    )
    def add_volume(id, name, mountpath, access):
        """
        Add a volume to a station.
        """
        r = galileo.stations.add_volumes_to_station(id, name, mountpath, access)
        volumes_list = [volume.__dict__ for volume in r]
        print(pandas.json_normalize(volumes_list))

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-v", "--vid", type=str, prompt="Volume ID", required=True, help="Volume id.",
    )
    @click.option(
        "-m", "--mid", type=str, prompt="Machine ID", required=True, help="Machine id.",
    )
    @click.option(
        "-h",
        "--hostpath",
        type=str,
        prompt="Host path",
        required=True,
        help="Host path.",
    )
    def add_hostpath(id, vid, mid, hostpath):
        """
        Add host path to volume.
        """
        r = galileo.stations.add_host_path_to_volume(id, vid, mid, hostpath)
        print(pandas.json_normalize(r.__dict__))

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-v", "--vid", type=str, prompt="Volume ID", required=True, help="Volume id.",
    )
    @click.option(
        "-h",
        "--hostpathid",
        type=str,
        prompt="Host path",
        required=True,
        help="Host path id.",
    )
    def remove_hostpath(id, vid, hostpathid):
        """
        Remove host path from volume.
        """
        if galileo.stations.delete_host_path_from_volume(id, vid, hostpathid):
            click.echo(f"Deleted host path {hostpathid}.")

    @stations.command()
    @click.option(
        "-i", "--id", type=str, prompt="Station ID", required=True, help="Station id.",
    )
    @click.option(
        "-v", "--vid", type=str, prompt="Volume ID", required=True, help="Volume id.",
    )
    def remove_volume(id, vid):
        """
        Remove volume from station.
        """
        if galileo.stations.remove_volume_from_station(id, vid):
            click.echo(f"Deleted volume {vid} from station {id}.")

    @stations.command()
    @click.option(
        "-s",
        "--sid",
        type=str,
        required=True,
        prompt="Station ID",
        help="Filter by station id, can provide multiple options.",
    )
    def volumes(sid):
        """
        List volumes.
        """
        spinner = Halo("Retrieving volumes", spinner="dot").start()
        r = galileo.stations.list_stations(stationids=[sid])

        if len(r):
            spinner.stop()
            click.echo("No station matches that query.")
            return

        volumes_list = r[0].volumes
        volumes_list = [volume.__dict__ for volume in volumes_list]
        volumes_df = pandas.json_normalize(volumes_list)
        volumes_df = volumes_df[
            ["volumeid", "stationid", "name", "host_paths", "access"]
        ]
        spinner.stop()
        click.echo(volumes_df)

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
        List users.
        """
        spinner = Halo("Retrieving station users", spinner="dot").start()
        r = galileo.stations.list_stations(stationids=[sid])

        if len(r) == 0:
            spinner.stop()
            click.echo("No station matches that query.")
            return

        users_list = r.stations[0].users
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
    def machines(sid):
        """
        List machines.
        """
        spinner = Halo("Retrieving station machines", spinner="dot").start()
        r = galileo.stations.list_stations(stationids=[sid])

        if len(r) == 0:
            spinner.stop()
            click.echo("No station matches that query.")
            return

        machines_list = r.stations[0].mids
        spinner.stop()
        pp = pprint.PrettyPrinter(indent=2)
        click.echo(pp.pprint(machines_list))

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
        "-v",
        "--volume",
        type=int,
        required=True,
        prompt="Volume index from (stations volumes)",
        help="Volume's index from `stations volumes`.",
    )
    def hostpaths(sid, volume):
        """
        List host paths.
        """
        spinner = Halo("Retrieving host paths", spinner="dot").start()
        r = galileo.stations.list_stations(stationids=[sid])

        if len(r) == 0:
            spinner.stop()
            click.echo("No station matches that query.")
            return

        volumes_list = r.stations[0].volumes[volume].host_paths
        volumes_list = [volume.__dict__ for volume in volumes_list]
        volumes_df = pandas.json_normalize(volumes_list)
        spinner.stop()
        click.echo(volumes_df)
