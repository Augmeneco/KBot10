import plugin as plugins
from config import config

class Help:
    names = ['тест']
    desc = 'тест'
    level = 256

    def execute(self, msg):
        msg.sendMessage(
            "```python\n"+\
            open('plugins/help.py','r').read()+'```',
            parse_mode = "MarkdownV2"
        ) 

plugins.init_plugin(Help)