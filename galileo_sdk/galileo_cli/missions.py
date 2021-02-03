import click
import pandas
import os
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

    @missions.command()
    def sync():
        """
        Sync your current job session with its Mission. 
        """
        spinner = Halo("Retrieving your Job Session info.", spinner="dot").start()
        try:
            # container hostnames are set based on their Galileo job id
            jobid = os.environ["HOSTNAME"]
        except:
            print("You are not in an active Galileo Job session.")
            spinner.stop()
            return
        
        # Retrieve the meta-data associated with this job
        jobs = galileo.jobs.list_jobs(jobids=[jobid])
        spinner.stop()
        
        
        if len(jobs) == 0:
            print("You are not in a recognized Galileo Job session")
            return
        elif len(jobs) == 1:
            job = jobs[0]
        else:
            print("The are multiple Jobs associated with the session.")
            return
            
        spinner = Halo("Retrieving the associated Mission.", spinner="dot").start()    
        # Find this jobs Mission id
        try:
            missions_ls = galileo.missions.list_missions(ids=[job.project_id])
        except Exception as e:
            print("Problem getting Mission details.", e)
            spinner.stop()
        
        missions_ls = [mission.__dict__ for mission in missions_ls]

        missions_df = pandas.json_normalize(missions_ls)
        missions_df['creation_timestamp'] = pandas.to_datetime(missions_df.creation_timestamp)
        missions_df = missions_df.sort_values(by="creation_timestamp", ascending=False)
        missions_df = missions_df[
            [
                "name",
                "description"
            ]
        ]
        spinner.stop()
        click.echo("\nMission Details")
        click.echo(missions_df.head(1))
        
        spinner = Halo("Retrieving the Mission's file list.", spinner="dot").start()    
        # Find this Mission's files
        try:
            missions_files = galileo.missions.get_mission_files(missions_ls[0]["mission_id"])
        
            missions_files = [thing.__dict__ for thing in missions_files]

            files_df = pandas.json_normalize(missions_files)
            files_df['creation_timestamp'] = pandas.to_datetime(files_df.creation_timestamp)
            files_df = files_df.sort_values(by="creation_timestamp", ascending=False)
            files_df = files_df[
                [
                    "filename",
                    "path",
                    "file_size"
                ]
            ]
            spinner.stop()
            click.echo("\nMission Files:
            click.echo(missions_df.head(1))
        except Exception as e:
            spinner.stop()
            print("Problem getting Mission file listing.", e)
            
        spinner = Halo("Uploading files in working directory.", spinner="dot").start()    
        # Find this Mission's files
        try:
            payload = "/home/galileo"
            success = galileo.missions.upload(missions_ls[0]["mission_id"], payload, verbose=True)
        except Exception as e:
            spinner.stop()
            print("Encountered problem uploading your working directory.", e)
