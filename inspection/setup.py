#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = ('pyPdf')

setup(name='inspection',
      version='1.0',
      description='Return a list of related pages between two pdfs.',
      author='Richard Hart',
      author_email='rich.hart@rice.edu',
      url='https://github.com/openstax/test-automation/tree/master/inspection',
      packages=find_packages(),
      install_requires=install_requires,
      entry_points="""
     [console_scripts]
     ox_inspect = inspection.inspection:main
     """
     )

