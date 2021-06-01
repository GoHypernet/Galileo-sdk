import click
import pandas

from galileo_sdk import GalileoSdk
from halo import Halo


def lzs_cli(main, galileo: GalileoSdk):
    @main.group()
    def lzs():
        """
        Get information about your Landing Zones.
        """
        pass

    @lzs.command()
    @click.option(
        "--lz_ids", 
        multiple=True, 
        type=str, 
        help="Filter by Landing Zone id."
    )
    @click.option(
        "--userid",
        required=False,
        type=str,
        help="Filter by page number."
    )
    @click.option(
        "--page", 
        type=int, 
        help="Filter by page number."
    )
    @click.option(
        "--items", 
        type=int, 
        help="Filter by number of items in the page.",
    )
    @click.option(
        '-e', 
        '--everything', 
        is_flag=True
    )
    def ls(lz_ids, userid, page=0, items=10, everything=False):
        """
        List all Landing Zones in your Galileo account.
        """
        
        spinner = Halo("Retrieving lzs", spinner="dot")
        spinner.start()

        self = galileo.profiles.self()
        userids = []
        if not everything:
            userids.append(self.userid)

        lzs = galileo.lz.list_lz(
           lz_ids=list(lz_ids), userids=list(userids), page=page, items=items,
        )

        if len(lzs) == 0:
            spinner.stop()
            click.echo("No Landing Zones found.")
            return


        lzs = [lz.__dict__ for lz in lzs]

        lzs_df = pandas.json_normalize(lzs)
        lzs_df = lzs_df[
            [
                "name",
                "lz_id",
                "arch",
                "status",
                "userid",
                "cpu_count",
                "gpu_count",
                "memory_amount",
            ]
        ]

        spinner.stop()
        click.echo(lzs_df.head(items))
