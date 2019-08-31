from setuptools import setup, find_packages

setup(
    name='galileo-sdk',
    version='0.0.1',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'galileo-cli = galileo.cli:main',
        ]
    },
    python_requires='>=3.6.7',
    install_requires=[
        'requests>=2.21.0',
        'galileo-socketio',
    ],
    extras_require={
        "docs": [
            'sphinx>=2.2.0',
            'sphinx_rtd_theme>=0.4.3'
        ]
    }
)
