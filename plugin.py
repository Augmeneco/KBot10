plugins_map = {}
plugins_list = []

def init_plugin(plugin):
    plugins_list.append(plugin)
    
    for name in plugin.names:
        if name not in plugins_map:
            plugins_map[name] = plugin

    print(f'Init plugin {plugin.names[0]}')

from plugins import *

import plugins.status
import plugins.help