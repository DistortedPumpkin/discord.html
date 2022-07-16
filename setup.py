from setuptools import setup
import re


version = ''
with open('discordhtml/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md') as f:
    readme = f.read()

if not version:
    raise RuntimeError('version is not set')

setup(
    name='discord.html',
    version=version,
    description='A package to interact with the Discord API by writing HTML',
    long_description=readme,
    author='DistortedPumpkin',
    install_requires=['discord.py==2.0.0a', 'bs4'],
    dependency_links=['git+https://github.com/Rapptz/discord.py.git@c7e589033df300d0b305ca43ff7f1de361c9c4af', 'bs4'],
    python_requires='>=3.8.0',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ]
)