import plugin as plugins
from config import config

class Help:
    names = ['помощь', 'help', 'хелп']
    desc = 'Помощь по командам бота'
    level = 1

    def execute(self, msg):
        out = '[ Помощь ]\n'
        
        for plugin in plugins.plugins_list:
            if msg.user.level >= plugin.level:
                out += f'• {config.names[0]} {plugin.names[0]} - {plugin.desc}\n'

        msg.sendMessage(out) 

plugins.init_plugin(Help)