from config import config

import telegram
import database
import plugin

import json
import requests
import re

class Msg:
    text: str = ""
    user_text: str
    chat_id: int
    msg_id: int
    from_id: int
    user: database.User
    username: str = None
    reply_id: int = None
    reply_msg = None
    attachments: list
    real_name: str
    skip: bool = False
    command: str = ""
    argv: list
    is_command: bool = False
    has_prefix: bool = False

    is_cmd_regex = re.compile(f'^/?\s?(?P<bot_name>{"|".join(config.names)})?\s?', re.IGNORECASE)
    
    def sendPhoto(self, data, **parameters):
        result = telegram.sendPhoto(self.chat_id, self.msg_id, data, **parameters)
        return result

    def sendPhotos(self, data, **parameters):
        reply_params = {
            'message_id': self.msg_id,
            'allow_sending_without_reply': True
        }
        #if 'caption' in parameters:
        #    reply_params['quote'] = str(parameters['caption'])
        #    del parameters['caption']
        parameters['reply_parameters'] = json.dumps(reply_params)

        result = telegram.sendPhotos(self.chat_id, data, **parameters)
        return result
    
    def sendAudio(self, data, **parameters):
        result = telegram.sendAudio(self.chat_id, self.msg_id, data, **parameters)
        return result
    
    def sendMessage(self, text, chat_id = None, **parameters):
        #chat_id = self.chat_id if 'chat_id' not in parameters else parameters['chat_id']
        if chat_id == None: chat_id = self.chat_id
        result = telegram.sendMessage(text, chat_id, self.msg_id, self.attachments, **parameters)
        return result

    def parse_msg(self, update: dict):
        chat_obj = update['chat']
        #if chat_obj['type'] not in ['group', 'supergroup']:
        #    self.skip = True
        #    return
        
        if 'text' in update: self.text = update['text']
        if 'caption' in update: self.text = update['caption']

        self.msg_id = update['message_id']
        
        from_obj = update['from']
        self.from_id = from_obj['id']
        if 'username' in from_obj: 
            self.username = from_obj['username']   
        self.real_name = from_obj['first_name']
        if 'last_name' in from_obj: self.real_name += f" {from_obj['last_name']}"
        self.user = database.users.get(self.from_id)

        self.chat_id = chat_obj['id']

        if 'reply_to_message' in update:
            reply_msg = update['reply_to_message']
            self.reply_id = reply_msg['message_id']

            msg = Msg()
            msg.parse_msg(reply_msg)
            self.reply_msg = msg

        self.attachments = []
        if 'photo' in update:
            photo = telegram.getPhoto(update['photo'])
            self.attachments.append({'type':'photo', 'stream':photo})

        if 'audio' in update:
            update['audio']['type'] = 'audio'
            update['audio']['stream'] = telegram.getFile(update['audio']['file_id'])
            self.attachments.append(update['audio'])

    def parse_command(self):
        self.is_cmd_regex = re.compile(f'^/?\s?(?P<bot_name>{"|".join(config.names)})?\s?', re.IGNORECASE)

        if '@'+config.bot_prefix in self.text:
            self.text = self.text.replace('@'+config.bot_prefix, '')

        if self.is_cmd_regex.search(self.text).group(0) == '': return
        self.has_prefix = True
        
        argv = []
        argv = self.is_cmd_regex.sub('', self.text).split(' ')
        command = argv[0].lower()

        if command not in plugin.plugins_map:
            self.argv = argv
            self.user_text = ' '.join(argv)
            return
        del argv[0]

        self.command = command
        self.is_command = True
        self.argv = argv
        self.user_text = ' '.join(argv)

    def escape_markdown(self, text):
        escape_chars = r"\_*[]()~`>#+-=|{}.!"
        text = re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

        text = text.replace('\*\*', '*')\
                   .replace('\`\`\`', '```')

        return text



telegram = telegram.Telegram()
