from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.3'
DESCRIPTION = 'Facebook Video Downloading via Python Package'
LONG_DESCRIPTION = 'A package that allows you to download video from Facebook'

# Setting up
setup(
    name="FVD",
    version=VERSION,
    author="Razi Ahmed Iqbal",
    author_email="<raziahmediqbal@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_data={'fbd': ['webdrivers/*']},
    install_requires=['beautifulsoup4', 'selenium'],
    keywords=['python', 'facebook', 'video', 'downloader', 'facebook video downloader', 'downlaod facebook videos'],
)
