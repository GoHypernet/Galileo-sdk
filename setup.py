from setuptools import setup, find_packages

setup(
    name='galileo',
    version='0.0.4',
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
        'python-engineio @ git+ssh://git@github.com/Hyperdyne/python-engineio.git@ef4f74eec7c45690aea6f3d3dab669305b8344ed',
        'python-socketio @ git+ssh://git@github.com/Hyperdyne/python-socketio.git@5f10992c9ce0a9794abc796412b7792825a4641d'
    ],
    extras_require={
        "docs": [
            'sphinx>=2.2.0',
            'sphinx_rtd_theme>=0.4.3'
        ]
    }
)