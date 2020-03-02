.. _lz:

Quickstart for Landing Zones
============================
Installation
------------

If you are using a Windows machine, you can download the executable.

However if you are running Linux or MacOS, you must run the Landing Zone in a Docker container.

First install Docker Compose via pip:

.. code-block:: bash

    $ pip install docker-compose

To map a local Unix socket to the Docker container's socket, write the following in a .yml file `(download, right-click and save) <docker-compose.yml>`_:

.. code-block:: yaml

    version: "3.3"
    services:
      landing-zone:
        image: hypernetlabs/landing-zone-daemon
        volumes:
          - /var/run/docker.sock:/var/run/docker.sock
          - /home/{YOUR-USERNAME}/.docker/config.json:/root/.docker/config.json # Put your home directory here
        container_name: landing-zone-daemon
        # Your machine id and machine name are arbitrary, you can id/name your machine anything
        command: --username 'youremail@email.com' --password 'yourpassword' --backend 'https://api.galileoapp.io' --machine-id 'yourmachineid' --machine-name 'yourmachinename'
        environment:
          DOCKER_HOST: unix:///var/run/docker.sock

*Change the variables in the .yml file before usage. In addition, you can mount a TCP socket instead of a Unix socket if you wish to do so.*

**Warning:** If you are using MacOS and you are having trouble, check your :code:`~/.docker/config.json` and delete :code:`"credsStore" : "osxkeychain"`.

Running the Landing Zone
-------------------------

In the same folder as the .yml file, pull the Landing Zone image and run it using the commands:

.. code-block:: bash

    $ docker-compose pull
    $ docker-compose up -d

Once you get a successful connection to the server, you can confirm if you have a machine by checking under Machines in the Galileo Web App or in the Galileo command line interface.


Alternative to Docker Compose
-----------------------------
If you do not want to use Docker Compose, you can do the following:

Make sure you have `installed Docker <https://docs.docker.com/install/>`_. To pull and run the Landing Zone Daemon Docker image, run the command:

.. code-block:: bash

    $  docker run -d -v /var/run/docker.sock:/var/run/docker.sock -v ~/.docker/config.json:/root/.docker/config.json hypernetlabs/landing-zone-daemon'

Take a look at the docker logs by:

.. code-block:: bash

    $ docker container <container-id>

The landing zone daemon will give you instructions for registering your machine as a landing zone on Galileo.
