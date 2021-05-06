# -*- coding: utf-8 -*-
"""Configuration file for the package."""
from setuptools import setup, find_packages

core = [
    'flask-restplus==0.13.0',
    'Flask-Cors==3.0.9'
]

aws = [
    'botocore==1.12.253',
    'boto3==1.9.253',
]

pmml = (core + ['pypmml==0.9.3'])
pickle = (core + ['dill==0.3.1.1'])
s3 = aws

all_deps = (core + pmml + s3 + pickle)

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(name='ml-model-server',
      version='1.0',
      url='https://github.com/dipayan90/ml-model-server',
      author='Dipayan Chattopadhyay',
      author_email='dipayan90@gmail.com',
      description='Cookie cutter online ML model serving solution',
      long_description=LONG_DESCRIPTION,
      packages=find_packages(),
      package_data={
          '': ['setup.py', 'setup.cfg'],
          'ml-model-server': ['*.py']
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      setup_requires=["pytest-runner==4.4"],
      install_requires=core,
      extras_require={
          'all': all_deps,
          's3': s3,
          'pmml': pmml,
          'pickle': pickle
      },
      tests_require=[
        'pytest==4.4.1',
        'pytest-cov==2.6.1',
        'pytest-mock==1.10.4',
        'requests-mock==1.6.0',
        'pytest-bdd==3.1.1',
        'moto==1.3.8',
      ],
      include_package_data=True,
      zip_safe=False)
