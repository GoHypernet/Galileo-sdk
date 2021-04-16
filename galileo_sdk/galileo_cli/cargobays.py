import click
import pandas
import os
from halo import Halo

from galileo_sdk import GalileoSdk

def cargobays_cli(main, galileo: GalileoSdk):
    @main.group()
    def cargobays():
        pass

    @cargobays.command()
    @click.option('-n', '--head', type=int, help="Number of Cargo Bays to display.")
    def ls(head):
        """
        List all Cargo Bays attached to your Galileo Account.
        """
        spinner = Halo("Getting the list of your Cargo Bays", spinner="dot").start()
        try:
            cargobays_ls = galileo.cargobays.list_cargobays()
            spinner.stop()
        except Exception as e:
            spinner.stop()
            print("Problem retrieving Cargo Bay list.", e)
            return

        cargobays_ls = [cargobay.__dict__ for cargobay in cargobays_ls]
        
        cargobays_df = pandas.json_normalize(cargobays_ls)
        cargobays_df['creation_timestamp'] = pandas.to_datetime(cargobays_df.creation_timestamp)
        cargobays_df = cargobays_df.sort_values(by="creation_timestamp", ascending=False)
        cargobays_df = cargobays_df[
            [
                "name",
                "storage_id",
                "storage_type",
                "creation_timestamp"
            ]
        ]
        spinner.stop()
        if head:
            click.echo(cargobays_df.head(head))
        else:
            print("Displaying first 10 Cargo Bays.")
            click.echo(cargobays_df.head(10))
