.. _quickstart:

Quickstart for SDK and Command Line Interface
==============================================
Installation
------------

Install via pip:

.. code-block:: bash

    $ pip install galileo-sdk

or if you have the code checked out locally:

.. code-block:: bash

    $ python setup.py install

Writing your first script
-------------------------
:code:`GalileoSdk` takes in 4 optional parameters.

.. code-block:: python

    from galileo_sdk import GalileoSdk

    # all parameters are optional however, the user must provide either an auth and refresh token
    # OR a username and password
    galileo = GalileoSdk(
        auth_token="AUTH_TOKEN", # optional, must also provide refresh token
        refresh_token="REFRESH_TOKEN",
        username="user@galileoapp.io", # optional, must also provide a password
        password="*****",
    )

Alternatively, you can set the environment variables instead of passing in the parameters:
 - :code:`GALILEO_TOKEN`
 - :code:`GALILEO_REFRESH_TOKEN`
 - :code:`GALILEO_USER`
 - :code:`GALILEO_PASSWORD`

An example of exporting your environment variable on MacOS:

.. code-block:: bash

    $ export GALILEO_USER=user@galileoapp.io

The most convenient and secure method for authentication is to use our AuthSdk helper class. 

.. code-block:: python
    
	# On your first time using the sdk, this will open a web browser and ask you to sign in,
    # or if you are in a headless environment, it will print an activation link to visit.
    from galileo_sdk import GalileoSdk, AuthSdk

    myauth = AuthSdk()
    access_token, refresh_token, expiry_time = myauth.initialize()
    galileo = GalileoSdk(auth_token=access_token, refresh_token=refresh_token)

:code:`GalileoSdk` exposes the Jobs, Machines, Profiles, Projects, and Stations APIs

Examples of using each of the APIs:

.. code-block:: python

    from galileo_sdk import GalileoSdk

    galileo  = GalileoSdk()
    jobs     = galileo.jobs.list_jobs()
    stations = galileo.stations.list_stations()
    users    = galileo.profiles.list_users()
    machines = galileo.lz.list_lz()
    missions = galileo.missions.list_missions()

You can also write callbacks that will execute upon events. The example below is a script that allows an admin of stations to automatically accept all requests to join a station:


.. code-block:: python

    from galileo_sdk import GalileoSdk

    galileo = GalileoSdk()

    # An event of type StationAdminRequestReceivedEvent is passed in to your
    # callback upon the trigger of a "on_station_admin_request_received" event.
    # This allows you to know who requested to join and what station they requested to join.
    def on_request_received(event: StationAdminRequestReceivedEvent):
        stationid = event["stationid"]
        userid = event["userid"]
        approve_request_to_join(stationid, [userid])

    galileo.stations.on_station_admin_request_received(on_request_received)


Before you end your script, you must disconnect the Galileo object via:

.. code-block:: python

    galileo.disconnect()


.. Using the Galileo Command Line Interface
-------------------------------------------
The Galileo CLI is an application that utilizes the Galileo SDK to view jobs without a GUI.

.. Install via pip:

.. .. code-block:: bash

    $ pip install galileo-cli

.. Provide a username and password combination or authorization token and refresh token combination. One way of providing a username is to set environment variables GALILEO_USER and GALILEO_PASSWORD.

.. .. code-block:: bash

..    $ export GALILEO_USER=user@galileoapp.io
..    $ export GALILEO_PASSWORD=password
..    $ galileo-cli

.. Another way to login is to provide your username on the command line, where you will be prompted for your password:

.. .. code-block:: bash

..    $ galileo-cli -u user@galileoapp.io
..    $ Password:
