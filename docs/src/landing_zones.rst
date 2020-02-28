.. _lz:

Quickstart for Landing Zones
============================
Installation
------------

If you are using a Windows machine, you can download the executable. However if you are running Linux or MaxOS, you must first `install Docker <https://docs.docker.com/install/>`_. To pull and run the Landing Zone Daemon Docker image, run the command:

.. code-block:: bash

    $ docker run hypernetlabs/landing-zone-daemon

After running this command, the landing zone daemon will give you instructions for registering your machine as a landing zone on Galileo. Once you get a successful connection to the server, you have a machine that others can run jobs on.

To make sure that the container is removed when the Landing Zone exits, run the command:

.. code-block:: bash

    $ docker run --rm hypernetlabs/landing-zone-daemon

To get more options on this command, use:

.. code-block:: bash

    $ docker run --rm hypernetlabs/landing-zone-daemon --help
