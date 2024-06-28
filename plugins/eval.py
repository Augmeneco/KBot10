import plugin as plugins
import traceback

class Eval:
    names = ['eval', 'exec']
    desc = 'Eval питонокода'
    level = 256

    def execute(self, msg):
        try:
            if msg.command == 'eval':
                msg.sendMessage(eval(msg.user_text))

            if msg.command == 'exec':
                exec(msg.user_text)
        except:
            result = traceback.format_exc()
            msg.sendMessage(result)

plugins.init_plugin(Eval)
