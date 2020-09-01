.. _missions:

Missions Guide
==============================================

Missions are a feature of Galileo that allow users to easily configure complex simulators and scripting environements to run repeatibly and reliably on any `LZ <landing_zones.html>`_ that they have lauch access to. Missions also allow for collaboration and sharing of simulation results through permissioned roles. 

Creating a New Mission 
-----------------------

To create a new Mission in Galileo, go to the Missions tab on the left side of the UI. 

.. image:: images/missions_tab.png

There are two ways to create a new mission. You can drag and drop a folder from your local hard-drive to the area on the UI that says "Add a Mission" (which will automatically upload the contents of that folder once the configuration step is complete), or you can start a new empty Mission by clicking the "Create a custom mission" button in the upper right.

.. image:: images/missions_create.png

This will launch the Mission configuration wizard which is covered in the next subsection. 

Configuring Your Mission Type
-------------------------------

Galileo supports many scripting languages (such as R, Python, Julia, and Stata) and simulators (Gromacs, HECRAS, AmberTools, etc.) right out-of-the-box. The first step in configuring you mission is to select your target framework from the drop-down list. 

.. image:: images/missions_select_framework.png

After you made your selection, follow the prompt to completion. 
 

Wormholes: Tunneled Sessions (beta)
-------------------------------------

