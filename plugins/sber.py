import plugins.ai_chat_handler as ai_chat_handler
import plugin as plugins
import requests
import time
import json
import uuid
import base64
from config import config

class SberImage:
    names = ['фаб', 'фб']
    desc = 'Картинки сберовской нейронкой'
    level = 1

    AUTH_HEADERS = {
        'X-Key': f"Key {config.config['fb-key']}",
        'X-Secret': f"Secret {config.config['fb-secret']}",
    }
    url = 'https://api-key.fusionbrain.ai/'

    def execute(self, msg):
        if msg.user_text == '': return
        start_time = time.time()

        #model_id = requests.get(self.url + 'key/api/v1/models', headers = self.AUTH_HEADERS).json()[0]['id']
        params = {
            'type': 'GENERATE',
            'numImages': 1,
            'width': 768,
            'style': 'UHD',
            'height': 1024,
            'generateParams': {
                'query': msg.user_text
            }
        }
        data = {
            'model_id': (None, 4),
            'params': (None, json.dumps(params), 'application/json')
        }
        uuid = requests.post(self.url + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data).json()['uuid']

        attemps = 20
        image = None
        while attemps > 0:
            response = requests.get(self.url + 'key/api/v1/text2image/status/' + uuid, headers=self.AUTH_HEADERS).json()

            if response['status'] == 'DONE':
                image = response['images'][0]
                break

            attemps -= -1
            time.sleep(2)

        image = base64.b64decode(image)
        msg.user_text += f'\nВремя выполнения: {round(time.time()-start_time, 2)} сек'

        msg.sendPhoto(image, caption = msg.user_text,
                    reply_to_message_id = msg.msg_id,
                    allow_sending_without_reply=True)




class Sber:
    names = ['сбер', 'sber']
    desc = 'Сберовский Гигачат'
    level = 1

    auth_code = config.config['sberapi']
    token = None

    contexts = ai_chat_handler.contexts

    def auth(self):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload='scope=GIGACHAT_API_PERS'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid1()),
            'Authorization': f'Basic {self.auth_code}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify='data/russian_trusted_root_ca_pem.crt').json()
        self.token = response['access_token']

    def execute(self, msg):
        if self.token == None: self.auth()

        history = []

        if msg.reply_msg != None:
            for context in self.contexts:
                if msg.reply_msg.msg_id in context['ids']:
                    history = context['history']
                    break

        history.append({"role": "user", "content": msg.user_text})

        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        payload = json.dumps({
            "model": "GigaChat:latest",
            "messages": history,
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 1024,
            "repetition_penalty": 1
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify='data/russian_trusted_root_ca_pem.crt')

        if 'choices' in response.json():
            response = response.json()
            out = response['choices'][0]['message']['content']
            history.append({'role': 'assistant', 'content': out})

            ret = msg.sendMessage(msg.escape_markdown(out), parse_mode = "MarkdownV2")
            msg_id = ret['result']['message_id']

            chat_exists = False
            if msg.reply_msg != None:
                for context in self.contexts:
                    if msg.reply_msg.msg_id in context['ids']:
                        context['history'] = history
                        context['ids'].append(msg_id)
                        chat_exists = True
                        break

            if msg.reply_msg == None or chat_exists == False:
                self.contexts.append({
                    'ids': [msg_id],
                    'history': history,
                    'model': 'sber'
                })
        else:
            print(response.text)

plugins.init_plugin(Sber)
plugins.init_plugin(SberImage)
