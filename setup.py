from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='sheepherding',
      version=version,
      description="Sheepherding AI",
      long_description="""\
An AI for simulated sheepherding""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ai',
      author='Sven Schmit',
      author_email='schmit@stanford.edu',
      url='www.stanford.edu/~schmit',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
