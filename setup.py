try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import json
import logging

#import dependencies
#import packages

with open('README.md') as readme_file:
    README = readme_file.read()

#with open('HISTORY.md') as history_file:
#    HISTORY = history_file.read()
setup_args = dict(
    name='qgate_graph',
    version='1.1',
    description='Generate graphs based on outputs from Quality Gate',
    long_description_content_type="text/markdown",
    long_description=README, # + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Jiri Steuer',
    author_email='steuer.jiri@gmail.com',
    keywords=['Quality', 'QualityGate'],
    url='https://github.com/ncthuc/gategraph',
    download_url='https://pypi.org/project/qgate_graph/'
)

install_requires = [
    'matplotlib~=3.7',
    'click~=8.1'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)