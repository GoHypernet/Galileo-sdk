import pandas
import click

from galileo_sdk import GalileoSdk
from halo import Halo


def profiles_cli(main, galileo: GalileoSdk):
    @main.group()
    def profiles():
        """
        View other Galileo profiles or your own.
        """

    @profiles.command()
    def self():
        """
        Details of your Galileo profile.
        """
        r = galileo.profiles.self()
        click.echo(pandas.json_normalize(r.__dict__))

    @profiles.command()
    @click.argument("index", type=int, required=False)
    @click.option(
        "-i",
        "--id",
        type=str,
        multiple=True,
        help="Filter by userids, can provide multiple options.",
    )
    @click.option(
        "-u",
        "--username",
        type=str,
        multiple=True,
        help="Filter by usernames, can provide multiple options.",
    )
    @click.option(
        "-p",
        "--partialname",
        type=str,
        multiple=True,
        help="Filter by partial usernames, can provide multiple options.",
    )
    @click.option("--page", type=int, help="Filter by page number.")
    @click.option(
        "--items",
        type=int,
        help="Filter by number of items in the page.",
    )
    @click.option('-n', '--head', type=int, help="Number of items to display.")
    def ls(index, id, username, partialname, page, items, head):
        """
        List of all the profiles.
        """
        spinner = Halo("Retrieving users", spinner="dot").start()
        r = galileo.profiles.list_users(
            user_ids=list(id),
            usernames=list(username),
            partial_usernames=list(partialname),
            page=page,
            items=items,
        )

        if len(r) == 0:
            spinner.stop()
            click.echo("No user matches that query.")
            return

        if isinstance(index, int):
            users_list = r[index]
        else:
            users_list = r

        users_list = [user.__dict__ for user in users_list]
        users_df = pandas.json_normalize(users_list)
        users_df = users_df[["username", "user_id", "lz_ids"]]

        spinner.stop()
        if head:
            click.echo(users_df.head(head))
        else:
            click.echo("(Displaying only first 30 items)\n")
            click.echo(users_df.head(30))

    @profiles.command()
    def invites():
        """
        Gives a list of all your station invites.
        """
        spinner = Halo("Retrieving invites", spinner="dot").start()
        r = galileo.profiles.list_station_invites()

        if len(r) == 0:
            spinner.stop()
            click.echo("No user matches that query.")
            return

        invites_list = [invites.__dict__ for invites in r]
        spinner.stop()
        click.echo(pandas.json_normalize(invites_list))
