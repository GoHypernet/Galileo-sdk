import os
import sys

from setuptools import setup
from setuptools.command.install import install

VERSION = "0.0.24"

_ver = sys.version_info

is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)

if is_py3:
    install_requires = ["requests>=2.21.0", "python-socketio[client]==4.3.1", "python-engineio==3.9.0"]
else:
    install_requires = ["enum34"]


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="galileo_sdk",
    version=VERSION,
    license="MIT",
    author="Hypernet Labs",
    author_email="hypernet@hypernetlabs.io",
    long_description="Galileo is a hub for modeling, simulations, and data analysis that functions as a quick and "
    "easy portal to cloud resources.  The application streamlines computing infrastructure, "
    "saving engineers and researchers weeks of cloud setup time.  Team and station features allow "
    "teams to collaborate efficiently by sharing projects and results, flexibly controlling "
    "permissions, and easily tracking their model version histories.\n The Galileo SDK is an API "
    "that allows users to interact with Galileo using a Python script instead of a graphical "
    "interface.  Use the SDK to automate processes such as scheduling jobs, automatically deploying "
    "jobs, accepting jobs, and accepting members.",
    url="https://hypernetwork.io/",
    packages=["galileo_sdk"],
    package_data={
        "galileo_sdk": [
            "sdk/**",
            "business/**/*",
            "business/__init__.py",
            "config/**/*",
            "config/__init__.py",
            "data/**/*",
            "data/__init__.py",
        ]
    },
    python_requires=">=2.7",
    install_requires=install_requires,
    extras_require={"docs": ["sphinx>=2.2.0", "sphinx-material"]},
    tests_require=["pytest-runner", "pytest", "mock"],
    cmdclass={"verify": VerifyVersionCommand,},
)
