try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import json
import logging
from qgate_graph.version import __version__
import dependencies
#import packages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qgate-graph-setup")

with open('README.md') as readme_file:
    README = readme_file.read()

#with open('HISTORY.md') as history_file:
#    HISTORY = history_file.read()
setup_args = dict(
    name='qgate_graph',
    version=__version__,
    description='Generate graphs based on outputs from Quality Gate',
    long_description_content_type="text/markdown",
    long_description=README, # + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Jiri Steuer',
    author_email='steuer.jiri@gmail.com',
    keywords=['Quality', 'QualityGate', 'Graph'],
    url='https://github.com/george0st/qgate-graph/',
    download_url='https://pypi.org/project/qgate_graph/'
)

install_requires = dependencies.base_requirements()
tests_require = dependencies.dev_requirements()
extras_require = dependencies.extra_requirements()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Libraries",
]


if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, classifiers=classifiers)