import requests
import json
import threading
import traceback

import utils
import plugin
from config import config
import plugins.ai_chat_handler as ai_chat_handler

class Telegram:
    token: str
    bot_id: int
    update_id: int = -1

    def __init__(self):
        self.token = config.telegram_token
        self.bot_id = self.sendMethod('getMe')['result']['id']


    def start_thread(self):
        telegram = utils.telegram

        while True:
            try:
                for update in telegram.getUpdates():
                    msg = utils.Msg()
                    msg.parse_msg(update)
                    msg.parse_command()
                    
                    if msg.skip: continue
                    if msg.is_command:
                        if msg.user.level < plugin.plugins_map[msg.command].level:
                            msg.sendMessage("У вас не достаточно прав для этой команды")
                            continue
                        
                        thread = threading.Thread(
                            target=plugin.plugins_map[msg.command]().execute,
                            args=(msg,)
                        )
                        thread.start()

                    else:
                        if msg.reply_msg and msg.reply_msg.from_id == self.bot_id:
                            if msg.text == '': continue

                            msg.user_text = msg.text

                            context = ai_chat_handler.get_context(msg.reply_msg.msg_id)

                            if context: model = context['model']
                            else: model = 'gemini'

                            threading.Thread(
                                target=plugin.plugins_map[model]().execute,
                                args=(msg,)
                            ).start()

            except ValueError:
                print(traceback.format_exc())
                pass
    
    def getUpdates(self):
        result = requests.post(
            'https://api.telegram.org/'+self.token+'/getUpdates',
            data = {'offset':self.update_id}
        ).json()['result']

        for update in result:
            self.update_id = update['update_id']+1
            if 'message' not in update: continue
            yield update['message']

    def getFile(self, file_id):
        file_path = self.sendMethod("getFile", file_id = file_id)['result']['file_path']
        url = f'https://api.telegram.org/file/{self.token}/{file_path}'
        response = requests.get(url, stream=True)

        return response

    def getPhoto(self, photo_list):
        return self.getFile(self.getMaxPhoto(photo_list))

    def getMaxPhoto(self, photo_list):
        max = 0
        max_photo = None

        for photo in photo_list:
            if photo['file_size'] > max:
                max = photo['file_size']
                max_photo = photo['file_id']
        
        return max_photo
        
    def sendPhotos(self, chat_id, data, **parameters):
        parameters['chat_id'] = chat_id

        media_group = []
        files = {}

        for media in data:
            if type(media) == bytes:
                file_name = f'photo{len(files)}'
                #files.append(('photo', (file_name, media, 'multipart/form-data')))
                files[file_name] = media
                media_group.append({
                    'type': 'photo',
                    'media': f'attach://{file_name}'
                })
            if type(media) == str:
                media_group.append({
                    'type': 'photo',
                    'media': media
                })
        if len(media_group) > 0:
            media_group[0]['caption'] = parameters['caption']
        del parameters['caption']

        parameters['media'] = json.dumps(media_group)

        result = requests.post(f'https://api.telegram.org/{self.token}/sendMediaGroup', data=parameters, files=files).json()
        return result

    def sendPhoto(self, chat_id: int, reply_id: int, data, **parameters):
        parameters['chat_id'] = chat_id
        files = None
        photo = None

        if type(data) == bytes:
            files = {'photo':('photo', data, 'multipart/form-data')}
        if type(data) == str:
            parameters['photo'] = photo

        if reply_id != None:
            parameters['reply_to_message_id'] = reply_id
            parameters['allow_sending_without_reply'] = True

        result = requests.post(f'https://api.telegram.org/{self.token}/sendPhoto', params=parameters, files=files).json()
        return result
    
    def sendAudio(self, chat_id: int, reply_id: int, data, **parameters):
        parameters['chat_id'] = chat_id
        files = None
        photo = None

        if type(data) == bytes:
            files = {'audio':(parameters['name'], data, 'multipart/form-data')}
        if type(data) == str:
            parameters['audio'] = photo

        if reply_id != None:
            parameters['reply_to_message_id'] = reply_id
            parameters['allow_sending_without_reply'] = True

        result = requests.post(f'https://api.telegram.org/{self.token}/sendAudio', params=parameters, files=files).json()
        return result

    def sendMessage(self, text: str, chat_id: int, reply_id: int, attachments: list, **parameters):
        parameters['chat_id'] = chat_id
        if text == '': text = ' '
        parameters['text'] = text

        if reply_id != None:
            parameters['reply_to_message_id'] = reply_id
            parameters['allow_sending_without_reply'] = True

        result = self.sendMethod("sendMessage", **parameters)
        return result

    def sendMethod(self, method, **parameters):
        result = requests.post(f'https://api.telegram.org/{self.token}/{method}', params=parameters).json()
        if 'error_code' in result:
            print(result)
            #sendMessage("Ошибка: ${result.getInt("error_code")}\n${result.getString("description")}", chatId)
        return result
