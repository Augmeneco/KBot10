import plugin as plugins
from deep_translator import GoogleTranslator

class Translate:
    names = ['тр', 'tr', 'перевод', 'переведи']
    desc = 'Переводчик пересланных сообщений'
    level = 1

    def execute(self, msg):
        if msg.reply_msg == None: 
            msg.sendMessage("Ты дебил?")
            return

        if msg.user_text == '': msg.user_text = 'ru'
        
        text = GoogleTranslator(source='auto', target=msg.user_text).translate(text=msg.reply_msg.text)
        msg.sendMessage(text) 

plugins.init_plugin(Translate)

