import plugin
from config import config

from deep_translator import GoogleTranslator
from io import BytesIO

import g4f
from g4f.client import Client
from g4f.cookies import get_cookies
from g4f.Provider.GeminiPro import GeminiPro

class StableDiffusion:
    names = ['что', 'ч']
    desc = 'Определение что на картинке'
    level = 1

    client = Client(
        api_key = config.google_api,
        provider=GeminiPro,
        proxies = 'http://localhost:25343'
    )

    def execute(self, msg):
        image = None

        prompt = 'Ты бот который определяет содержимое изображений.\n'

        if msg.reply_msg != None:
            if msg.reply_msg.attachments:
                if msg.reply_msg.attachments[0]['type'] == 'photo':
                    image = msg.reply_msg.attachments[0]['stream'].content

        if msg.attachments:
            if msg.attachments[0]['type'] == 'photo':
                image = msg.attachments[0]['stream'].content

        if not image:
            msg.sendMessage("Ты даун?")
            return

        if msg.user_text != '':
            prompt += f'От себя добавлю: {msg.user_text}'

        try:
            response = self.client.chat.completions.create(
                model='gemini-pro-vision',
                messages=[{'role': 'user', 'content': prompt}],
                image = image
            )
            text = response.choices[0].message.content

            msg.sendMessage(text)
        except KeyError:
            msg.sendMessage("Гуголь не смог определить (или зассал)")

plugin.init_plugin(StableDiffusion)


