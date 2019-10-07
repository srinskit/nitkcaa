from setuptools import setup
setup(
    name='nitkcaa',
    packages=['nitkcaa'],
    entry_points={
        'console_scripts': [
            'nitkcaa = nitkcaa.main:main',
        ]
    },
    install_requires=[
        'requests',
    ]
)
