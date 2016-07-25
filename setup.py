"""
Package predix.setup
By: Adi Suresh
This module holds the setup parameters fro building an acnaconda package
"""

from setuptools import setup, find_packages

setup(
    name='predix',
    version='0.1.0',
    description='ge python test_data analytics package',
    author='Adi Suresh',
    author_email='aditya.suresh@ge.com',
    url='https://github.build.ge.com/212464591/Predix-Python-SDK',
    keywords=['data', 'ge', 'predix', 'analytics'],
    packages=find_packages(exclude=["tests",
                                    "build",
                                    "projects",
                                    "atmospheric_data_ingestion",
                                    "rotor_model"]),
    include_package_data=False,
    entry_points={},
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'pika',
        'paramiko',
        'requests',
        'redis',
        'boto3',
        'psycopg2'
    ]
)
