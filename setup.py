import os
import sys
import codecs
from setuptools import setup

import versioneer


try:
    # Python 3
    from os import dirname
except ImportError:
    # Python 2
    from os.path import dirname

here = os.path.abspath(dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

if sys.argv[-1] == "publish":
    from awsjar import __version__

    os.system("python setup.py sdist")
    os.system(
        f"python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/awsjar-{__version__}.tar.gz"
    )
    sys.exit()


setup(
    name="awsjar",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Jar make it easy to store the state of your AWS Lambda functions.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["awsjar"],
    url="https://github.com/ysawa0/awsjar",
    license="Apache 2.0",
    author="Yuki Sawa",
    author_email="yukisawa@gmail.com",
    install_requires=["boto3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
