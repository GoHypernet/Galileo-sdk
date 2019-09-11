import platform
from setuptools import setup, find_packages

install_requires = [
    'requests>=2.21.0',
    'galileo-socketio',
]
if platform.system() == 'Windows':
    install_requires.extend([
        'pyreadline',
    ])

setup(
    name='galileo-sdk',
    version='0.0.3',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'galileo-cli = galileo.cli:main',
        ]
    },
    python_requires='>=3.6.7',
    install_requires=install_requires,
    extras_require={
        "docs": [
            'sphinx>=2.2.0',
            'sphinx_rtd_theme>=0.4.3'
        ]
    }
)
