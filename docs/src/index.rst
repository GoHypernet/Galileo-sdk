.. _introduction:

.. title:: Galileo Docs

.. image:: images/galileo_pres.png

Introduction
==============

Galileo is a hub for modeling, simulation, and data analysis that functions as an intuitive, easy-to-use portal to cloud and traditional, on-premises resources.  Galileo streamlines the utilization of computing infrastructure for `scientific computing applications <https://hypernetlabs.io/gettingstarted/#tutorials>`_ (like data science, machine learning, and simulation engineering), saving engineers and researchers (as well as IT teams) of all knowledge levels the time and frustration involved in setting up an adequate simulation or analysis pipeline.  The `Missions <missions.html>`_ feature in Galileo allows teams to collaborate efficiently on complex modeling and simulation projects by sharing input files and configuration parameters. `Stations <stations.html>`_ make it simple to administer computational resources by setting resource limits and quotas and have a built in queueing system. `Cargo Bays <cargobays.html>`_ allow users to deploy from and receive result directly to their own storage solution, like `Dropbox <https://www.dropbox.com/>`_ or `Tardigrade <https://tardigrade.io/>`_. Additionally, Galileo lets users flexibly control roles and permissions, and easily track result histories of previous computational jobs.

The Galileo :ref:`Landing Zone <landing_zone_main>` (LZ) daemon is a containerized daemon process that allows Galileo Station administrators to quickly and securely connect nearly any computational resource with an internet connection to their Galileo account. Once the LZ daemon is authenticated against a user's account, it must be attached to a Galileo Station for it to be utilized. The LZ daemon makes it simple to administer distributed computational resources used by distributed teams without the hassle of acquiring a public IP address or setting up a VPN. 

The Galileo `SDK <galileo_sdk.html>`_ allows users to interact with the Galileo service using a Python script (both python2 and python3 are supported) instead of the web-based graphical interface.  Use the SDK to automate processes such as scheduling and deploying jobs, as well as to integrate Galileo into external applications.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

    Security Overview <security.rst>
	Universes Guide <universes.rst>
    Stations Guide <stations.rst>
    Missions Guide <missions.rst>
	Cargo Bay Guide <cargobays.rst>
    Quickstart for Landing Zones <landing_zone_main.rst>
    Quickstart for Python SDK <galileo_sdk.rst>
    SDK References <references/index.rst>
