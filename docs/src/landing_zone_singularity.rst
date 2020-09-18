.. _landing_zone_singularity:

Quickstart for Galileo Landing Zones and Singularity
====================================================

The following is a user guide for deploying a Galileo Landing Zone
(LZ) using our official Singularity image.

Prerequisites
-------------

Singularity must be installed on the machine you wish to use as a
Landing Zone. You can find installation instructions `here
<https://sylabs.io/singularity/https://sylabs.io/singularity/>`_.

How It Works
------------

In a nutshell, a Landing Zone receives jobs from users, builds
containers for those jobs, and then manages the execution of those
containers until the job is complete. So it follows that if the LZ
runs inside a container, it must be capable of making containers
inside that container! And that's precisely how it works; the Landing
Zone image for Singularity has a copy of Singularity installed
*inside* it! Job containers are run with the ``--containall``,
``--writable``, and ``--no-home`` flags to maximise isolation and
retain new and modified files.

Using our official Singularity image to run a Landing Zone in a
container is a fantastic way to get started because it's easy to
install, update, manage, and clean up after. However there are a
couple tricky aspects that the following subsections will show you how
to work around. You will find these work arounds referenced throughout
the rest of the documentation.

Building Images and Root Privileges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The immediate problem is that Singularity requires root privileges to
build a container, and in many cases you might want run an LZ in an
environment where you do not have root privileges. Thankfully
Singularity added support for a potential workaround in the `fakeroot
<https://sylabs.io/guides/3.6/user-guide/fakeroot.html>`_ feature
beginning in version 3.3.0. The ``--fakeroot`` flag allows us to mimic
having root privileges, so adding this flag to your Singularity
invocation of the LZ allows the LZ to inherit this characteristic when
building containers for the jobs sent to it,
e.g.

.. code-block:: bash

   singularity --fakeroot ... library://hypernetlabs/default/landing-zone-daemon

Persisting and Accessing Application Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Depending on how you invoke Singularity to run the LZ, this may or may
not be a problem for you. By default, Singularity bind mounts
``/home/$USER``, ``/tmp``, and ``$PWD`` into containers at runtime. If
you allow for these default mounts, then the only difficulties you may
experience will stem from sharing files between host and container
that aren't in those mounted directories (like the global config at
``/etc/galileod.conf``).

If you choose to disable those default bind mounts, then you need to
be aware of the application files you'd like to access while the
container is running, or persist after the container has exited. For
example, if you choose to keep a copy of the authentication token to use
across LZ sessions, then create a specific directory to hold it
(e.g. ``$ mkdir $HOME/lz_token``), mount the directory, and use the
``--token`` flag to tell the LZ to look for it at that mount point:

.. code-block:: bash

   singularity ... --bind $HOME/lz_token:/lz_token ... library://hypernetlabs/default/landing-zone-daemon --token /lz_token/auth.token ...

A convenient way to mount all non-temporary application files would be
to mount a configuration directory and use the ``--config-dir`` flag
to tell the LZ where it is mounted. So if you have a directory at
``$HOME/.galileod`` you might use a command like this:

.. code-block:: bash

   singularity ... --bind $HOME/.galileod:/config_dir ... library://hypernetlabs/default/landing-zone-daemon --config-dir /config_dir

How to Run the Landing Zone Daemon
----------------------------------

Choose the name you’d like this LZ to have when viewed in the Galileo
web interface. We will refer to the LZ name as :code:`$LZ_NAME`. When
you see :code:`$LZ_NAME` referenced, simply substitute your chosen
name in its place.

* The recommended way to invoke the Landing Zone is as a Singularity
  `service
  <https://sylabs.io/guides/3.6/user-guide/running_services.html>`_ so
  that it can run in the background.

.. code-block:: bash

    $ singularity instance start --fakeroot library://hypernetlabs/default/landing-zone-daemon landing-zone-daemon --name "$LZ_NAME"

That command will create an instance named ``landing-zone-daemon``;
you can prove this by running ``singularity instance list``.

* Now that the LZ is running, we must authenticate it against your
  account. Run this command in your terminal

.. code-block:: bash

    $ tail ~/.singularity/instances/logs/"$HOSTNAME"/"$USER"/landing-zone-daemon.out

* This should give you some output that looks like this

.. code-block:: bash

    Pulling updates…
    Already up to date!
    Please visit the following url in your browser and enter the code below
    URL: https://galileoapp.auth0.com/activate
    Code: XXXX-XXXX

* Follow those instructions. Once you have confirmed your code at the
  provided URL you should see your new Landing Zone appear in the
  Galileo Landing Zones tab! In order to submit jobs to your new LZ,
  you must add it to a Station. You can create a new Station by going
  to the Stations tab and clicking the Create Stations button.

* You can stop the LZ at any time with

.. code-block:: bash

    $ singularity instance stop landing-zone-daemon

Singularity will automatically clean up the container used to run the instance.
