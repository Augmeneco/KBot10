import plugin as plugins

class Translate:
    names = ['чо']
    desc = 'Чо высрал на не той раскладке'
    level = 1

    def execute(self, msg):
        if msg.reply_msg == None: 
            msg.sendMessage("Ты дебил?")
            return

        layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                        'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                        "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                        'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))

        msg.sendMessage(msg.reply_msg.text.translate(layout))

plugins.init_plugin(Translate)

