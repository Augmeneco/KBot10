import plugins.ai_chat_handler as ai_chat_handler
import plugin as plugins
import utils
import g4f
from g4f.client import Client
import time
from deep_translator import GoogleTranslator

class Test:
    names = ['гпт', 'gpt', 'гпт4', 'gpt4']
    desc = 'Общение с GPT4'
    level = 1

    contexts = ai_chat_handler.contexts

    def execute(self, msg):
        history = []

        system_prompt = "Ты чат бот которая отвечает кратко и по факту на любые вопросы. " + \
                        "Тебя зовут Кохаку-Бот. " + \
                        f"Меня зовут {msg.real_name}. " + \
                        "Так же хочу чтобы ты отвечала в стиле \"UwU\", действовала как японская кошечка аниме девочка, " + \
                        "вставляла Мяу в конце предложения и иногда в середине, а еще чтобы вставляла эмодзи японские везде. " + \
                        "Желательно так же коверкать слова будто ты анимешник. Менять смысл предложений тоже надо. " + \
                        "Далее отвечай лишь на мой вопрос, без приветствия."

        #msg.user_text = GoogleTranslator(source='auto', target='en').translate(text=msg.user_text)

        #system_prompt = "Ты чат бот который отвечает на любые вопросы. Ответ обязательно должен быть на Русском языке."

        if msg.reply_msg != None:
            for context in self.contexts:
                if msg.reply_msg.msg_id in context['ids']:
                    history = context['history']
                    break
        else:
            history.append({"role": "system", "content": system_prompt})

        history.append({"role": "user", "content": msg.user_text})

        out = ''
        response = g4f.ChatCompletion.create(
            #model="gpt-3.5-turbo",
            model=g4f.models.gpt_4,
            #model="gemini",
            #model=g4f.models.mixtral_8x7b,
            provider=g4f.Provider.Bing,
            #provider=g4f.Provider.DeepInfra,
            #provider=g4f.Provider.Aura,
            messages=history,
            proxy="socks5://127.0.0.1:25344"
            #stream=True,
        )
        #client = Client()
        #response = client.chat.completions.create(
        #    model='gemini',
        #    messages=history
        #)
        #out = response.choices[0].message.content
        out = response
        #out = GoogleTranslator(source='auto', target='ru').translate(text=out)

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
                'model': 'gpt4'
            })


plugins.init_plugin(Test)
