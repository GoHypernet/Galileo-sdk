.. _introduction:

.. title:: Galileo Docs

.. image:: images/galileo_pres.png

Introduction
==============

Galileo is a hub for modeling, simulations, and data analysis that functions as an intuitive, easy-to-use portal to cloud and traditional, on-premises resources.  Galileo streamlines the utilization of computing infrastructure for all scientific computing applications, saving engineers and researchers the time and frustration involved in setting up an adequate simulation or analysis pipeline.  The `Missions <missions.html>`_ and `Stations <stations.html>`_ features in Galileo allow teams to collaborate efficiently on complex modeling and simulation projects by sharing input files and data as well as computational resources in a simple, easy-to-understand fashion. Additionally, Galileo lets users flexibly control roles and permissions, and easily track result histories of previous calculations.

The Galileo `Landing Zone <landing_zones.html>`_ (LZ) deamon is a containerized daemon process that allows Galileo resource administrators to quickly and securely connect any computational resource with an internet connection to their Galileo account. Once the Galileo LZ daemon is authenticated against a user's account, a user must add the LZ to a Galileo Station. Here, they can then invite collaborators who can then deploy jobs to the LZ with no additional configuration. 

The Galileo `SDK <galileo_sdk.html>`_ allows users to interact with the Galileo service using a Python script (both python2 and python3 are supported) instead of the web-based graphical interface.  Use the SDK to automate processes such as scheduling and deploying jobs, as well as to integrate Galileo into external applications.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
    
	Stations Guide <stations.rst>
	Missions Guide <missions.rst>
    Quickstart for Landing Zones <landing_zones.rst>
    Quickstart for Python SDK <galileo_sdk.rst>
    SDK References <references/index.rst>