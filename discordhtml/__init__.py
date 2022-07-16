__title__ = 'discordhtml'
__author__ = 'DistortedPumpkin'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-present DistortedPumpkin'
__version__ = '0.0.5'

from .bot import Bot

def start(filename: str = 'main.html'):
    bot = Bot()
    bot.load_file(filename, True)
    bot.run()