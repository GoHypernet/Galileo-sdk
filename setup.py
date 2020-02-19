from setuptools import find_packages, setup

setup(
    name="galileo_sdk",
    version="0.0.4",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6.7",
    install_requires=["requests>=2.21.0", "python-socketio"],
    extras_require={"docs": ["sphinx>=2.2.0", "sphinx-material"]},
    setup_requires=["pytest-runner", "black", "isort"],
    tests_require=["pytest", "unittest", "mock"],
)
