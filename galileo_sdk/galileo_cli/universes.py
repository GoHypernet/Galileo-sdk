import click
import pandas
import os
from halo import Halo

from galileo_sdk import GalileoSdk

def universes_cli(main, galileo: GalileoSdk):
    @main.group()
    def universes():
        pass

    @universes.command()
    def ls():
        """
        List all Galileo Universes your account belongs to. 
        """
        spinner = Halo("Checking your Universe membership", spinner="dot").start()
        universes_ls = galileo.universes.list_universes()
        spinner.stop()
        
        universes_ls = [universe.__dict__ for universe in universes_ls]

        universes_df = pandas.json_normalize(universes_ls)
        universes_df['creation_timestamp'] = pandas.to_datetime(universes_df.creation_timestamp)
        universes_df = universes_df.sort_values(by="creation_timestamp", ascending=False)
        universes_df = universes_df[
            [
                "universe_id",
                "name",
                "creation_timestamp"
            ]
        ]
        spinner.stop()
        click.echo(universes_df)

    @universes.command()
    @click.option("-i", "--uuid", type=str, multiple=False, help="Set your active Universe by its uuid.")
    @click.option("-n", "--name", type=str, multiple=False, help="Set your active Universe by its name.")
    def set(uuid, name):
        """
        Set your active Universe. 
        """
        
        if name and uuid:
            print("Please give a name or a UUID, not both.")
            return
        
        spinner = Halo("Checking your Universe membership", spinner="dot").start()
        universes = galileo.universes.list_universes()
        spinner.stop()
        
        uni_dict = {}
        if uuid:
            for universe in universes:
                uni_dict[universe.universe_id] = universe.name
            
            if uuid not in uni_dict:
                print("Could not find a universe with that uuid.")
                return
            else:
                name = uni_dict[uuid]
        
        if name:
            for universe in universes:
                uni_dict[universe.name] = universe.universe_id
            
            if name not in uni_dict:
                print("Could not find a universe with that name.")
                return
            else:
                uuid = uni_dict[name]
        
        spinner = Halo(f'Setting your Universe Context to {name}', spinner="dot").start()
        galileo.set_universe(uuid)
        spinner.stop()
        if name:
            print(f'Universe context set to {name}')
        else:
            print(f'Universe context set to default')
        return

    @universes.command()
    @click.option("-u", "--user-id", required=True, type=str, multiple=False, help="Set your active Universe by its uuid.")
    @click.option("-n", "--name", required=True, type=str, multiple=False, help="Set your active Universe by its name.")
    def create(user_id, name):
        """
        Create a Universe. 
        """
        spinner = Halo("Creating your universe", spinner="dot").start()
        try:
            universe = galileo.universes.create_universe(name, [user_id])
            spinner.stop()
            click.echo("Created universe: with name {name} and id {id}".format(name=universe.name, id=universe.universe_id))
        except Exception as e:
            spinner.stop()
            click.echo("Error", e)
