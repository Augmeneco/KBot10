import plugin as plugins
import subprocess

class Cmd:
    names = ['терм']
    desc = 'Терминал консоли'
    level = 256

    def execute(self, msg):
        output = ''

        try:
            result = subprocess.check_output(msg.user_text, shell=True, stderr=subprocess.STDOUT, timeout=1)
        except subprocess.TimeoutExpired as e:
            output = e.output.decode('utf-8')
        else:
            output = result.decode('utf-8')

        msg.sendMessage(output)

plugins.init_plugin(Cmd)
