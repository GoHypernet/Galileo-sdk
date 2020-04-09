.. _lz:

Quickstart for Landing Zones
============================
Prerequisites
-------------

Docker must be installed on the machine you wish to use as a landing zone. You can find those instructions here:

* `Mac <https://docs.docker.com/docker-for-mac/install/>`_
* Linux
    * `CentOS <https://docs.docker.com/engine/install/centos/>`_
    * `Debian <https://docs.docker.com/engine/install/debian/>`_
    * `Fedora <https://docs.docker.com/engine/install/fedora/>`_
    * `Ubuntu <https://docs.docker.com/engine/install/ubuntu/>`_

How to Run the Landing Zone Daemon
----------------------------------
* Make sure that Docker is running.
* Open a terminal
    * Mac: Press Cmd+Space to open Spotlight Search, type “terminal”, and press Return.
    * Linux: You can try Ctrl+Alt+T. If that doesn’t work you should find instructions for your distribution.
* This is a good time to `test your Docker installation <https://docs.docker.com/get-started/#test-docker-installation>`_.
* Choose the name you’d like this Landing Zone to have and choose a unique ID Galileo should identify it by. We will refer to these values as :code:`$LZ_NAME` and :code:`$LZ_ID` respectively. When you see those references simply substitute your chosen values in their place.
* Copy the following command, paste it in the terminal, substitute your values, and run the command by pressing Enter or Return and wait for the process to finish.

.. code-block:: bash

    $ docker run -d -v /var/run/docker.sock:/var/run/docker.sock -v “$HOME”/.galileo/tokens:/tokens --name landing-zone-daemon hypernetlabs/landing-zone-daemon --machine-id “$MACHINE_ID” --machine-name “$MACHINE_NAME” --refresh-token-file /tokens/token

* Now that the LZ is running, we must authenticate it. Run this command in your terminal

.. code-block:: bash

    $ docker logs landing-zone-daemon

* This should give you some output that looks like this

.. code-block:: bash

    Pulling updates…
    Already up to date!
    Please visit the following url in your browser and enter the code below
    URL: https://galileoapp.auth0.com/activate
    Code: XXXX-XXXX

* Follow those instructions. Once you have confirmed your code at the provided URL you should see your new Landing Zone appear in Galileo!

Stopping and Restarting the Landing Zone Daemon
-----------------------------------------------
* Open a terminal as you did above
* Run this command to stop the Landing Zone

.. code-block:: bash

    $ docker stop landing-zone-daemon

* Run this command to restart the Landing Zone

.. code-block:: bash

    $ docker start landing-zone-daemon

* You should not have to re-authenticate this time!

Removing and Restarting the Landing Zone Daemon
-----------------------------------------------
* Open a terminal as you did above
* To remove the Landing Zone Daemon container from your Docker installation, first stop the Landing Zone, then run this command

.. code-block:: bash

    $ docker rm landing-zone-daemon

* To install the Landing Zone Daemon again follow the instructions above. You may or may not need to reauthenticate depending on whether you delete or move the automatically generated .galileo folder.

