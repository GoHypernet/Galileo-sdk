import click
import pandas
from halo import Halo

from galileo_sdk import GalileoSdk

def missions_cli(main, galileo: GalileoSdk):
    @main.group()
    def missions():
        pass

    @missions.command()
    @click.argument("index", type=int, required=False)
    @click.option(
        "-i",
        "--id",
        type=str,
        multiple=True,
        help="Filter by Mission id, can provide multiple options.",
    )
    @click.option(
        "-n",
        "--name",
        type=str,
        multiple=True,
        help="Filter by Mission name, can provide multiple options.",
    )
    @click.option(
        "-u",
        "--userid",
        type=str,
        multiple=True,
        help="Filter by userids, can provide multiple options.",
    )
    @click.option("--page", type=int, help="Filter by page number.")
    @click.option(
        "--items", type=int, help="Filter by number of items in the page.",
    )
    @click.option('-n', '--head', type=int, help="Number of items to display.")
    def ls(index, id, name, userid, page, items, head):
        """
        List all Missions in your Galileo profile.
        """
        spinner = Halo("Retrieving information", spinner="dot").start()
        self = galileo.profiles.self()
        spinner.stop()
        spinner = Halo("Retrieving your Mission", spinner="dot").start()
        userid += (self.userid,)
        missions = galileo.missions.list_missions(
            ids=list(id),
            names=list(name),
            user_ids=list(userid),
            page=page,
            items=items,
        )

        if len(missions) == 0:
            spinner.stop()
            click.echo("No mission matches that query.")
            return

        if isinstance(index, int):
            missions_ls = missions[index]
        else:
            missions_ls = missions

        missions_ls = [mission.__dict__ for mission in missions_ls]

        missions_df = pandas.json_normalize(missions_ls)
        missions_df['creation_timestamp'] = pandas.to_datetime(missions_df.creation_timestamp)
        missions_df = missions_df.sort_values(by="creation_timestamp", ascending=False)
        missions_df = missions_df[
            [
                "name",
                "mission_id",
                "description",
                "creation_timestamp",
            ]
        ]

        spinner.stop()

        if head:
            click.echo(missions_df.head(head))
        else:
            click.echo("(Displaying only first 30 items)\n")
            click.echo(missions_df.head(30))
