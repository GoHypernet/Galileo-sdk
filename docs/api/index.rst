Welcome to Galileo API's documentation!
=======================================

Overview
========
This SDK provides an API and command line interface to interact with Galileo.

Installation
============
1. Create a virtual environment by running the command `python3 -m venv venv`
2. Activate the virtual environment by running the command `source venv/bin/activate`
3. Install all necessary packages/dependencies by running the command `pip install -e .`

Using the command line interface (CLI)
======================================
1. In order to use the CLI, you must have a running instance of the Galileo daemon in a virtual environment.
2. While you're in a second terminal with a virtual environment, invoke the CLI by running the command `galileo-cli`. The CLI must be running on the same host and port as the Galileo daemon. Use the galileo certificate file that has seen generated after running the Galileo daemon for the `--cert` option.

Custom scripts
==============
1. Before running your script, make sure the Galileo daemon is running. The CLI should also be running if you do not use the `API.login()` function in your script.
2. To write your scripts using the Galileo API, put `from galileo.api import API` at the beginning of your script. Examples of scripts are included under the `examples` folder.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

    api <api.rst>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
