import plugin as plugins
from config import config
import utils

class Pred:
    names = ['пред']
    desc = 'Предупреждение челу'
    level = 256

    def execute(self, msg):
        if msg.reply_msg != None:
            if msg.reply_msg.username != None:
                name = f'@{msg.reply_msg.username}'
            else:
                name = msg.reply_msg.real_name

            if 'преды' not in msg.reply_msg.user.data:
                msg.reply_msg.user.data['преды'] = 0

            msg.reply_msg.user.data['преды'] += 1
            if msg.reply_msg.user.data['преды'] >= 3:
                msg.reply_msg.user.data['преды'] = 0

                msg.sendMessage(f'{name} вы были забанены.')
                utils.telegram.sendMethod('banChatMember', chat_id = msg.chat_id, user_id = msg.reply_msg.user.id)
            
            else:
                msg.sendMessage(f'{name} вы получили предупреждение. {msg.reply_msg.user.data["преды"]}/3')

            utils.telegram.sendMethod('deleteMessage', chat_id = msg.chat_id, message_id = msg.reply_msg.msg_id)

            msg.reply_msg.user.update()

plugins.init_plugin(Pred)