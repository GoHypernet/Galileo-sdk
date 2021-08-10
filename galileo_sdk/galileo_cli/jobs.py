from requests.models import HTTPError
from galileo_sdk import GalileoSdk
from halo import Halo
import pandas
import click
import datetime


def jobs_cli(main, galileo: GalileoSdk):
    @main.group()
    def jobs():
        """
        See all jobs, manage the state of a job, or download your results.
        """
        pass

    def get_jobs(index, id, receiver, sid, userid, status, page, items,
                 spinner, projectid):
        r = galileo.jobs.list_jobs(job_ids=list(id),
                                   receiver_ids=list(receiver),
                                   station_ids=list(sid),
                                   user_ids=list(userid),
                                   statuses=list(status),
                                   page=page,
                                   items=items,
                                   mission_ids=list(projectid))

        if len(r) == 0:
            spinner.stop()
            click.echo("No job matches that query.")
            return

        if isinstance(index, int):
            jobs_list = r[index]
        else:
            jobs_list = r

        jobs_list = [job.__dict__ for job in jobs_list]
        jobs_df = pandas.json_normalize(jobs_list)
        jobs_df['time_created'] = pandas.to_datetime(jobs_df.time_created,
                                                     unit='s')
        jobs_df['last_updated'] = pandas.to_datetime(jobs_df.last_updated,
                                                     unit='s')
        jobs_df = jobs_df.sort_values(by="last_updated", ascending=False)
        jobs_df.total_runtime = jobs_df.total_runtime.map(lambda x: x / 60)
        jobs_df = jobs_df[[
            "job_id",
            "station_id",
            "receiver_id",
            "name",
            "total_runtime",
            "status",
            "time_created",
            "last_updated",
        ]]

        return jobs_df

    @jobs.command()
    @click.argument("index", type=int, required=False)
    @click.option(
        "-i",
        "--id",
        type=str,
        multiple=True,
        help="Filter by job id, can provide multiple options.",
    )
    @click.option(
        "-r",
        "--receiver",
        type=str,
        multiple=True,
        help="Filter by receiver id, can provide multiple options.",
    )
    @click.option(
        "-s",
        "--sid",
        type=str,
        multiple=True,
        help="Filter by station id, can provide multiple options.",
    )
    @click.option(
        "-u",
        "--user-ids",
        type=str,
        multiple=True,
        help="Filter by user id, can provide multiple options.",
    )
    @click.option(
        "--status",
        type=str,
        multiple=True,
        help="Filter by status, can provide multiple options.",
    )
    @click.option(
        "--page",
        type=int,
        multiple=True,
        help="Filter by page.",
    )
    @click.option(
        "--items",
        type=int,
        multiple=True,
        help="Filter by items per page.",
    )
    @click.option("-n", "--head", type=int, help="Number of items to display.")
    @click.option(
        "-p",
        "--projectid",
        type=str,
        multiple=True,
        help="Filter by status, can provide multiple options.",
    )
    @click.option('--received', is_flag=True)
    @click.option('--sent', is_flag=True)
    def ls(index, id, receiver, sid, user_ids, status, page, items, head,
           received, sent, projectid):
        """
        List all jobs.
        """
        spinner = Halo("Retrieving information", spinner="dots").start()

        #Testing purpose
        my_id = galileo.profiles.self().user_id
        user_ids = list(user_ids) + [my_id]
        receiver_ids = list(receiver) + galileo.lz.list_lz(user_ids=[my_id])
        spinner.stop()

        if not received and not sent:
            received = True
            sent = True

        if sent:
            spinner = Halo("Retrieving jobs sent by you",
                           spinner="dots").start()
            sent_jobs_df = get_jobs(index, id, receiver, sid, user_ids, status,
                                    page, items, spinner, projectid)
            spinner.stop()
            click.echo("SENT JOBS\n=========\n")
            if head:
                click.echo(sent_jobs_df.head(head))
            else:
                click.echo("(Displaying only first 30 items)\n")
                click.echo(sent_jobs_df.head(30))

        if received:
            spinner = Halo("\nRetrieving jobs you received",
                           spinner="dots").start()
            received_jobs_df = get_jobs(index, id, receiver_ids, sid, user_ids,
                                        status, page, items, spinner,
                                        projectid)
            spinner.stop()
            click.echo("\nRECEIVED JOBS\n===========\n")
            if head:
                click.echo(received_jobs_df.head(head))
            else:
                click.echo("(Displaying only first 30 items)\n")
                click.echo(received_jobs_df.head(30))

    @jobs.command()
    @click.option(
        "-j",
        "--jobid",
        type=str,
        prompt="Job ID",
        required=True,
        help="Job id.",
    )
    def request_stop(jobid):
        """
        Request to stop a job.
        """
        jobs_list = [galileo.jobs.request_stop_job(jobid)]
        jobs_list = [job.__dict__ for job in jobs_list]
        jobs_df = pandas.json_normalize(jobs_list)
        jobs_df.time_created = jobs_df.time_created.map(lambda x: x)
        jobs_df.last_updated = jobs_df.last_updated.map(lambda x: x)
        jobs_df = jobs_df[[
            "job_id",
            "station_id",
            "receiver_id",
            "name",
            "total_runtime",
            "status",
            "time_created",
            "last_updated",
        ]]
        click.echo(jobs_df)

    @jobs.command()
    @click.option(
        "-j",
        "--jobid",
        type=str,
        prompt="Job ID",
        required=True,
        help="Job id.",
    )
    def request_pause(jobid):
        """
        Request to pause a job.
        """
        jobs_list = galileo.jobs.request_pause_job(jobid)
        jobs_list = [job.__dict__ for job in jobs_list]
        jobs_df = pandas.json_normalize(jobs_list)
        jobs_df.time_created = jobs_df.time_created.map(
            lambda x: datetime.datetime.fromtimestamp(x))
        jobs_df.last_updated = jobs_df.last_updated.map(
            lambda x: datetime.datetime.fromtimestamp(x))
        jobs_df = jobs_df[[
            "jobid",
            "stationid",
            "receiverid",
            "name",
            "total_runtime",
            "status",
            "time_created",
            "last_updated",
        ]]
        click.echo(jobs_df)

    @jobs.command()
    @click.option(
        "-j",
        "--jobid",
        type=str,
        prompt="Job ID",
        required=True,
        help="Job id.",
    )
    def request_start(jobid):
        """
        Request to start a job.
        """
        try:
            jobs_list = galileo.jobs.request_start_job(jobid)
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 405:
                click.echo("Job cannot be started")
                return
            elif status_code == 500:
                curr_job = galileo.jobs.list_jobs(job_ids=[jobid])
                if not curr_job:
                    click.echo("Job does not exist")
                    return
            raise e
        jobs_list = [job.__dict__ for job in jobs_list]
        jobs_df = pandas.json_normalize(jobs_list)
        jobs_df.time_created = jobs_df.time_created.map(
            lambda x: datetime.datetime.fromtimestamp(x))
        jobs_df.last_updated = jobs_df.last_updated.map(
            lambda x: datetime.datetime.fromtimestamp(x))
        jobs_df = jobs_df[[
            "jobid",
            "stationid",
            "receiverid",
            "name",
            "total_runtime",
            "status",
            "time_created",
            "last_updated",
        ]]
        click.echo(jobs_df)

    @jobs.command()
    @click.option(
        "-j",
        "--jobid",
        type=str,
        prompt="Job ID",
        required=True,
        help="Job id.",
    )
    @click.option(
        "-p",
        "--path",
        type=str,
        prompt="Path (where results will be stored)",
        required=True,
        help="The path where the job results will be downloaded to.",
    )
    def download_results(jobid, path):
        """
        Download results of job when finished.
        """
        r = galileo.jobs.download_job_results(jobid, path)
        if r:
            click.echo(f"Downloading results into directory '{path}' ...")
