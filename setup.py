from setuptools import setup

setup(
    name="galileo_sdk",
    version="0.0.14",
    license="MIT",
    author="Hypernet Labs",
    author_email="hypernet@hypernetlabs.io",
    url="https://hypernetwork.io/",
    packages=["galileo_sdk"],
    package_data={"galileo_sdk": ["sdk/**", "business/**/*", "config/**/*", "data/**/*"]},
    python_requires=">=3.6.7",
    install_requires=["requests>=2.21.0", "python-socketio"],
    extras_require={"docs": ["sphinx>=2.2.0", "sphinx-material"]},
    setup_requires=["pytest-runner", "black", "isort"],
    tests_require=["pytest", "unittest", "mock"],
)
