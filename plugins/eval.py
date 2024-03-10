import plugin as plugins
import traceback

class Eval:
    names = ['eval']
    desc = 'Eval питонокода'
    level = 256

    def execute(self, msg):
        try:
            result = eval(msg.user_text)
        except:
            result = traceback.format_exc()

        msg.sendMessage(result)

plugins.init_plugin(Eval)
