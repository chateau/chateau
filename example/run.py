import chateau, logging
logging.basicConfig(level=logging.DEBUG)
bot = chateau.bot.Bot({
    'nickname': "MyNick",
    'username': "MyUser",
    'realname': "MyReal",
    'password': "",
    'address': "chat.freenode.net",
    'port': 6667,
    'transport': 'asynchat',
    'use_ssl': False,
    'umodes': '',
    'plugins': []
})
bot.connect()
