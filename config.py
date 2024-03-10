import json

class Config:
    telegram_token: str
    vk_token: str
    names: list
    config: dict
    bot_prefix: str

    def __init__(self):
        self.config = json.loads(open('data/config.json', 'r').read())

        self.names = self.config['names']
        self.telegram_token = 'bot'+self.config['telegram_token']
        self.bot_prefix = self.config['bot_prefix']
        self.google_api = self.config['googleapi']

config = Config()
