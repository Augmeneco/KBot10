import plugin
import requests
import base64
import time
import re
from deep_translator import GoogleTranslator
from io import BytesIO
from PIL import Image

class StableDiffusion:
    names = ['сд', 'стейбл','стейбла','sd','картинка']
    desc = 'Генерация картинок стейблой'
    level = 1

    loras = {
        'страшилка': ['madziowa_p', 'strashilka'],
        'астольфо': ['astolfo', 'astolfo'],
        'птичник': ['', 'pti'],
        'бурила': ['driller_drg', 'driller'],
        'аранара': ['aranara', 'aranara'],
        'комар': ['komaru', 'komaru'],
        'рельсовод': ['', 'relsovod']
    }

    def execute(self, msg):
        try:
            start_time = time.time()
            url = 'http://127.0.0.1:7860'

            loras_add = ''
            lora_tags = re.findall('(?:\w+?:\d.\d)|(?:\w+:\d)|(?:\w+,)|(?:\w+)', msg.user_text)
            for lora_tag in lora_tags:
                lora_split = lora_tag.split(':')
                lora_split[0] = lora_split[0].replace(',','')

                if len(lora_split) != 2:
                    lora_split.append('1')

                if lora_split[0] not in self.loras: continue

                if self.loras[lora_split[0]][0] != '':
                    msg.user_text = msg.user_text.replace(lora_tag, self.loras[lora_split[0]][0])
                else:
                    msg.user_text = msg.user_text.replace(lora_tag, '')

                loras_add += f'<lora:{self.loras[lora_split[0]][1]}:{lora_split[1]}>, '

            if loras_add != '':
                msg.user_text += f', {loras_add}'

            text = GoogleTranslator(source='auto', target='en').translate(text=msg.user_text)

            params = {
                'prompt': f'(high quality, masterpiece), {text}',
                'negative_prompt': 'easynegative, notxt',
                'seed': -1,
                'sampler_name': 'Euler a', #'DPM++ 2M SDE Karras',
                "steps": 20,
                "cfg_scale": 5,
                "width": 512,
                "height": 768,
            }

            if msg.attachments:
                image = Image.open(BytesIO(
                    msg.attachments[0]['stream'].content
                ))
                width, height = image.size

                if width > 512 or height > 512:
                    scaler = width / height
                    if scaler > 1:
                        params['width'] = 512
                        params['height'] = int(512 / scaler)
                    else:
                        params['width'] = int(512 * scaler)
                        params['height'] = 512
                
                image.close()

                method = 'img2img'
                params['init_images'] = [
                    base64.b64encode(msg.attachments[0]['stream'].content).decode()
                ]
                
                tags = requests.post(f'{url}/sdapi/v1/interrogate', json={
                    'model': 'deepdanbooru',
                    'image': params['init_images'][0]
                }).json()['caption']
                
                params['prompt'] += ', '+tags
                msg.user_text += f'\n\nDeepbooru теги: {tags}\n'

            else:
                method = 'txt2img'
            
            image = requests.post(f'{url}/sdapi/v1/{method}', json=params).json()['images'][0]
            image = base64.b64decode(image)
            msg.user_text += f'\nВремя выполнения: {round(time.time()-start_time, 2)} сек'
            
            msg.sendPhoto(image, caption = msg.user_text, 
                        reply_to_message_id = msg.msg_id, 
                        allow_sending_without_reply=True)
        except requests.exceptions.ConnectionError:
            msg.sendMessage("Сервер стейблы отключен")

plugin.init_plugin(StableDiffusion)


