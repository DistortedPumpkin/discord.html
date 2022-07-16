from pathlib import Path
from setuptools import setup, find_packages
import re


ROOT = Path(__file__).parent

version = ''
with open('discordhtml/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md') as f:
    readme = f.read()

if not version:
    raise RuntimeError('version is not set')

with open(ROOT / 'requirements.txt') as f:
    requirements = f.read()

setup(
    name='discord.html',
    version=version,
    description='A package to interact with the Discord API by writing HTML',
    long_description=readme,
    author='DistortedPumpkin',
    install_requires=['discord.py', 'bs4'],
    dependency_links=['http://github.com/Rapptz/discord.py/tarball/master#egg=discord', 'bs4'],
    python_requires='>=3.8.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ],
    packages=['discordhtml']
)