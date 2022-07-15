from .bot import Bot

def start(filename: str = 'main.html'):
    bot = Bot()
    bot.load_file(filename, True)
    bot.run()