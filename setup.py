from setuptools import setup, find_packages

setup(
    name='galileo',
    version='0.0.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'galileo-cli = galileo.cli:main',
        ]
    },
    python_requires='>=3.6.7',
    install_requires=[
        'requests>=2.21.0',
        'sphinx>=2.2.0',
        'sphinx_rtd_theme>=0.4.3',
        'python-engineio @ git+ssh://git@github.com/Hyperdyne/python-engineio.git',
        'python-socketio @ git+ssh://git@github.com/Hyperdyne/python-socketio.git'
    ],
)