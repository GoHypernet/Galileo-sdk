import click
import pandas
import os
from pathlib import Path
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
        '-s',
        '--short',
        is_flag=True,
        help=
        "Show less information for each Mission (only id, name, and Public/Private status)."
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
        "--user_id",
        type=str,
        multiple=True,
        help="Filter by userids, can provide multiple options.",
    )
    @click.option("--page", type=int, help="Filter by page number.")
    @click.option(
        "--items",
        type=int,
        help="Filter by number of items in the page.",
    )
    @click.option('-n',
                  '--head',
                  type=int,
                  help="Number of Missions to display.")
    def ls(index, id, short, name, user_id, page, items, head):
        """
        List the Missions in your Galileo profile.
        """
        spinner = Halo("Retrieving information", spinner="dot").start()
        self = galileo.profiles.self()
        spinner.stop()
        spinner = Halo("Retrieving your Mission", spinner="dot").start()
        user_id += (self.user_id, )
        missions = galileo.missions.list_missions(
            mission_ids=list(id),
            names=list(name),
            user_ids=list(user_id),
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
        missions_df['creation_timestamp'] = pandas.to_datetime(
            missions_df.creation_timestamp)
        missions_df = missions_df.sort_values(by="creation_timestamp",
                                              ascending=False)
        if short:
            missions_df = missions_df[[
                "name",
                "mission_id",
                "public",
            ]]
        else:
            missions_df = missions_df[[
                "name",
                "mission_id",
                "source_storage_id",
                "source_path",
                "destination_storage_id",
                "destination_path",
                "description",
                "public",
                "creation_timestamp",
            ]]

        spinner.stop()

        if head:
            click.echo(missions_df.head(head))
        else:
            click.echo("(Displaying only first 30 items)\n")
            click.echo(missions_df.head(30))

    @missions.command()
    @click.option(
        '-e',
        '--everything',
        is_flag=True,
        help=
        "Save all files in this Job's working directory (echo $WORKDIR) to its Galileo Mission (carefull, this could be time-consuming)."
    )
    @click.option(
        "-f",
        "--file",
        type=str,
        multiple=False,
        help="Save a specific file from this Job to your Galileo Mission.",
    )
    def save(file, everything):
        """
        Save files from the current job session to its Galileo Mission. 
        """
        spinner = Halo("Retrieving your job session info.",
                       spinner="dot").start()
        try:
            # container hostnames are set based on their Galileo job id
            jobid = os.environ["HOSTNAME"]
        except:
            print("You are not in an active Galileo job session.")
            spinner.stop()
            return

        # Retrieve the meta-data associated with this job
        jobs = galileo.jobs.list_jobs(job_ids=[jobid])
        spinner.stop()

        if len(jobs) == 0:
            print("You are not in a recognized Galileo job session.")
            return
        elif len(jobs) == 1:
            job = jobs[0]
        else:
            print("The are multiple jobs associated with the session.")
            return

        spinner = Halo("Retrieving the associated Mission.",
                       spinner="dot").start()
        # Find this jobs Mission id
        try:
            missions_ls = galileo.missions.list_missions(
                mission_ids=[job.mission_id])
        except Exception as e:
            print("Problem getting Mission details.", e)
            spinner.stop()

        missions_ls = [mission.__dict__ for mission in missions_ls]

        missions_df = pandas.json_normalize(missions_ls)
        missions_df['creation_timestamp'] = pandas.to_datetime(
            missions_df.creation_timestamp)
        missions_df = missions_df.sort_values(by="creation_timestamp",
                                              ascending=False)
        missions_df = missions_df[["name", "description"]]
        spinner.stop()
        click.echo("\nMission Details")
        click.echo(missions_df.head(1))

        spinner = Halo("Retrieving the Mission's file list.",
                       spinner="dot").start()
        # Find this Mission's files
        try:
            missions_files = galileo.missions.get_mission_files(
                missions_ls[0]["mission_id"])

            missions_files = [thing.__dict__ for thing in missions_files]

            files_df = pandas.json_normalize(missions_files)
            files_df['creation_timestamp'] = pandas.to_datetime(
                files_df.creation_timestamp)
            files_df = files_df.sort_values(by="creation_timestamp",
                                            ascending=False)
            files_df = files_df[["filename", "path", "file_size"]]
            spinner.stop()
            click.echo("\nMission Files:")
            click.echo(files_df)
        except Exception as e:
            spinner.stop()
            print("Problem getting Mission file listing.", e)

        try:
            workdir = os.environ['WORKDIR']
        except Exception as e:
            print(
                "WORKDIR environment variable is not set. You can set this with the workdir command."
            )
            return

        spinner = Halo("Uploading files.", spinner="dot").start()
        # Find this Mission's files
        try:

            rename = None
            if file:

                payload = Path(file)
                if not payload.exists():
                    spinner.stop()
                    print(payload, "does not exist.")
                    return

                # we will rename the file based on it relative location to the Job's WORKDIR
                rename = os.path.relpath(payload.absolute(), workdir)
                print(payload)
            elif everything:
                payload = workdir

            else:
                spinner.stop()
                print("Please tell me what you'd like to save.")
                return

            success = galileo.missions.upload(missions_ls[0]["mission_id"],
                                              os.fspath(payload),
                                              rename=rename,
                                              verbose=True)
            spinner.stop()
        except Exception as e:
            spinner.stop()
            print("Encountered problem uploading your working directory.", e)

    @missions.command()
    @click.option('-p',
                  '--public',
                  is_flag=True,
                  help="Create the Mission as a Publicly searchable Mission.")
    @click.option(
        "-n",
        "--name",
        type=str,
        multiple=False,
        help="The name to assign to the Mission.",
    )
    def create(name, public):
        """
        Create a new Mission in your account.
        """

        if not name:
            print("Please specify a name with the -n or --name flag.")
            return

        spinner = Halo("Uploading files.", spinner="dot").start()
        try:
            mission = galileo.missions.create_mission(name, public=public)
        except Exception as e:
            print("Error:", e)
            spinner.stop()
            return

        spinner.stop()
        print("Created Mission:", mission.name)
        print("Mission ID: ", mission.mission_id)
        print("Public: ", str(bool(public)))

    @missions.command()
    @click.option(
        "-i",
        "--id",
        type=str,
        multiple=False,
        help="UUID of the Mission to update.",
    )
    @click.option(
        "-n",
        "--name",
        type=str,
        multiple=False,
        help="Update the name of a Mission.",
    )
    @click.option(
        "--ssid",
        type=str,
        multiple=False,
        help="Cargo Bay ID for the input data of the Mission.",
    )
    @click.option(
        "--dsid",
        type=str,
        multiple=False,
        help="Cargo Bay ID for the output data of the Mission.",
    )
    @click.option(
        "--spath",
        type=str,
        multiple=False,
        help=
        "Path within the source Cargo Bay to pull the input data of the Mission.",
    )
    @click.option(
        "--dpath",
        type=str,
        multiple=False,
        help=
        "Path within the destination Cargo Bay to put the output data of the Mission.",
    )
    def update(id, name, ssid, dsid, spath, dpath):
        """
        Update the settings of a Mission in your account. 
        """

        if not id:
            print("Please specify a Mission with the -i or --id flag.")
            return

        spinner = Halo("Finding Mission.", spinner="dot").start()
        try:
            mission = galileo.missions.list_missions(mission_ids=[id])
        except Exception as e:
            spinner.stop()
            print("Error:", e)
            return

        spinner.stop()

        if len(mission) != 1:
            print("Couldn't find a Mission with that UUID.")
            return

        spinner = Halo("Updating Mission.", spinner="dot").start()
        try:
            success = galileo.missions.update_mission(
                id,
                name=name,
                source_storage_id=ssid,
                destination_storage_id=dsid,
                source_path=spath,
                destination_path=dpath)
        except Exception as e:
            print("Error:", e)
            spinner.stop()
            return

        spinner.stop()
        print("Mission Updated")

    @missions.command()
    @click.argument(
        "mission_ids",
        nargs=-1,
        type=str,
    )
    def delete(mission_ids):
        """
        Delete Missions in your Galileo account.
        """
        spinner = Halo("Deleting missions", spinner="dot").start()

        for mission in mission_ids:
            try:
                if not galileo.missions.delete_mission_by_id(mission):
                    spinner.stop()
                    click.echo("Deletion of mission {id} unsuccessful".format(
                        id=mission))
                spinner.stop()
                click.echo("Deleted Mission with id: {id}".format(id=mission))
            except Exception as e:
                click.echo("Error: {e}".format(e=e))
        spinner.stop()
