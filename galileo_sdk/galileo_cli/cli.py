import os
import sys
import signal
from getpass import getpass

import click
from click_shell import shell
from pyfiglet import Figlet
from termcolor import colored
from colorama import init

from galileo_sdk import GalileoSdk, AuthSdk
#from .rain import *
from .jobs import jobs_cli
from .lzs import lzs_cli
from .profiles import profiles_cli
from .missions import missions_cli
from .universes import universes_cli
from .cargobays import cargobays_cli
from .stations import stations_cli

init()


graphic = Figlet(font="slant").renderText("Galileo")
intro = "Welcome to Galileo! (? for help)\n"


def keyboardInterruptHandler(signal, frame):
    print("")
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)

@shell(prompt=colored("galileo$ ", "red"), intro=f"{graphic}\n{intro}")
@click.option(
    "-m",
    "--mode",
    default="production",
    help="Either in 'production' or 'development' mode",
)
def main(mode):

    myauth = AuthSdk()
    access_token, refresh_token, expiry_time = myauth.initialize()
    galileo = GalileoSdk(auth_token=access_token, refresh_token=refresh_token)

    @main.command()
    def exit():
        os._exit(0)

    @main.command()
    def quit():
        os._exit(0)
        
    @main.command()
    def logout():
        token_file = os.path.join(os.path.expanduser("~"), ".galileo")
        if os.path.exists(token_file):
            try:
                os.remove(token_file)
                print("You have been logged out, see you next time")
            except Exception as e:
                print("Could not remove Auth Token file:", e)
        os._exit(0)

    click.echo(f"Connected to {galileo.backend}!")

    @main.command()
    @click.option("-w", "--workdir", type=str, multiple=False, help="Set a path to use as working directory.")
    @click.option('-v', '--view', is_flag=True, help="Print the current working directory for this session." )
    def workdir(workdir, view):
        """
        Set the working directory for this CLI session. Files are uploaded to Missions relative to this path.
        """
        
        if view:
            print("The working directory is currently ", os.environ.get("GALILEO_RESULTS_DIR", "not set"), ".")
        
        if workdir:
            if os.path.exists(workdir):
                os.environ["GALILEO_RESULTS_DIR"] = workdir
                print("Working directory is now ", os.environ["GALILEO_RESULTS_DIR"], ".")
            else:
                print("This directory does not exist.")
        else:
            print("Please provide an existing path to use as this session's working directory.")

    @main.command()
    @click.option('-m', '--message', help="Send a notification with the provided text." )
    def notification(message):
        """
        Provide a string (in quotes if there are spaces) to this command and have it delivered as a notification in Galileo. 
        """

        if message:
            success = galileo.send_notification(message, verbose=True)
        else: 
            print("Please provide a text message to send as a notification.")

    universes_cli(main, galileo)
    cargobays_cli(main, galileo)
    profiles_cli(main, galileo)
    lzs_cli(main, galileo)
    missions_cli(main, galileo)
    stations_cli(main, galileo)
    jobs_cli(main, galileo)
