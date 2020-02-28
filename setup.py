from setuptools import setup

setup(
    name="galileo_sdk",
    version="0.0.14",
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
    package_data={"galileo_sdk": ["sdk/**", "business/**/*", "config/**/*", "data/**/*"]},
    python_requires=">=3.6.7",
    install_requires=["requests>=2.21.0", "python-socketio"],
    extras_require={"docs": ["sphinx>=2.2.0", "sphinx-material"]},
    setup_requires=["pytest-runner", "black", "isort"],
    tests_require=["pytest", "unittest", "mock"],
)
