import plugin as plugins
from config import config
from gradio_client import Client
import subprocess
import os

class RVCAudioVoice:
    names = ['скажи']
    desc = f'Говорит текст указанным голосом. Подробнее "{config.names[0]} скажи помощь"'
    level = 1

    pitch = {
        'путин':2,
        'мишенконтрол':2,
        'некоарк':10,
        'зеля':0,
        'пригожин': 0,
        'гриффин': 2,
        'эрнест': 3
    }

    def get_argv(self, msg, name):
        out = None
        for i in range(len(msg.argv)):
            if name == msg.argv[i]:
                if len(msg.argv)-1 < i+1:
                    msg.sendMessage('Ты еблан?')
                    return out
                
                out = msg.argv[i+1]
                del msg.argv[i]
                del msg.argv[i]

                return out

    def execute(self, msg):
        client = None
        try:
            client = Client("http://localhost:7865/")
        except:
            msg.sendMessage("Сервер RVC выключен")
            return

        voices = [i[0].replace('.pth', '') for i in client.predict(api_name="/infer_refresh")[0]['choices']]

        if msg.argv[0] == 'помощь': 
            result = client.predict(api_name="/infer_refresh")
            out = f'Запрос посылается в формате "{config.names[0]} скажи ИМЯГОЛОСА ваш текст"\n\nСписок вариантов имен моделей голосов:\n'
            out += '\n' \
                .join(['• '+i for i in voices])

            msg.sendMessage(out)
            return

        voice = None
        if msg.argv[0] not in voices:
            msg.sendMessage('Такого голоса не существует')
            return
        else:
            voice = msg.argv[0]+'.pth'
            del msg.argv[0]

        client.predict(voice, 0, 0, api_name="/infer_change_voice")
        
        pitch = self.get_argv(msg, 'тон')
        if pitch == None: pitch = self.pitch[voice.replace('.pth','')]
        if type(pitch) != int:
            pitch = int(pitch) if pitch.isdigit() else self.pitch[voice.replace('.pth','')]

        if ' '.join(msg.argv) == '': 
            msg.sendMessage("Ты еблан?")
            return
        
        id = msg.msg_id
        
        tts = subprocess.Popen([
            'edge-tts',
            '--text',
            ' '.join(msg.argv),
            '--voice',
            'ru-RU-DmitryNeural',
            '--write-media',
            f'/tmp/{id}.mp3',
            '--rate=-10%'
        ])
        tts.wait()
        #audio_orig = open(f'/tmp/{id}.mp3', 'rb').read()
        #os.system(f'rm /tmp/{id}.mp3')

        #msg.sendAudio(open(f'/tmp/{id}.mp3', 'rb').read())

        result = client.predict(
            0,
            f'/tmp/{id}.mp3',	# str  in 'Путь к аудиофайлу, который хотите обработать (ниже указан пример пути к файлу):' Textbox component
            pitch,	# int | float  in 'Изменить высоту голоса (укажите количество полутонов; чтобы поднять голос на октаву, выберите 12, понизить на октаву — -12):' Number component
            f'/tmp/{id}.mp3',	# str (filepath on your computer (or URL) of file) in 'Файл дуги F0 (не обязательно). Одна тональность на каждую строчку. Заменяет обычный F0 и модуляцию тональности:' File component
            "rmvpe",	# str  in 'Выберите алгоритм оценки высоты голоса ('pm': работает быстро, но даёт низкое качество речи; 'harvest': басы лучше, но работает очень медленно; 'crepe': лучшее качество, но сильно нагружает GPU; 'rmvpe': лучшее качество и минимальная нагрузка на GPU):' Radio component
            "",	# str  in 'Путь к файлу индекса черт. Оставьте пустым, чтобы использовать выбранный вариант из списка ниже:' Textbox component
            "null",	# str (Option from: []) in 'Автоматически найденные файлы индексов черт (выберите вариант из списка):' Dropdown component
            0,	# int | float (numeric value between 0 and 1) in 'Соотношение поиска черт:' Slider component
            0,	# int | float (numeric value between 0 and 7) in 'Если значение больше 3: применить медианную фильтрацию к вытащенным тональностям. Значение контролирует радиус фильтра и может уменьшить излишнее дыхание.' Slider component
            0,	# int | float (numeric value between 0 and 48000) in 'Изменить частоту дискретизации в выходном файле на финальную. Поставьте 0, чтобы ничего не изменялось:' Slider component
            0,	# int | float (numeric value between 0 and 1) in 'Использовать громкость входного файла для замены или перемешивания с громкостью выходного файла. Чем ближе соотношение к 1, тем больше используется звука из выходного файла:' Slider component
            0,	# int | float (numeric value between 0 and 0.5) in 'Защитить глухие согласные и звуки дыхания для предотвращения артефактов, например, разрывания в электронной музыке. Поставьте на 0.5, чтобы выключить. Уменьшите значение для повышения защиты, но учтите, что при этом может ухудшиться точность индексирования:' Slider component
            api_name="/infer_convert"
        )
        msg.sendAudio(open(result[1], 'rb').read(), name = voice.replace('.pth','')+'.wav')


class RVCAudioRemover:
    names = ['раздели', 'аудио']
    desc = 'Ответьте на аудио сообщение чтобы разделить на слова и музыку'
    level = 1

    def execute(self, msg):
        client = None
        try:
            client = Client("http://localhost:7865/")
        except:
            msg.sendMessage("Сервер RVC выключен")
            return

        if msg.reply_msg == None:
            msg.sendMessage("Отвечать на сообщение надо дебил")
            return
        
        if len(msg.reply_msg.attachments) == 0:
            msg.sendMessage("Да хули ты отвечаешь на сообщение без аттача еблан")
            return

        attach = msg.reply_msg.attachments[0]
        if attach['type'] != 'audio':
            msg.sendMessage("Аудио сообщение надо, долбаеб блять")
            return
        
        open(f'/tmp/{msg.msg_id}_remover.wav', 'wb').write(attach['stream'].content)
        
        result = client.predict(
            "HP2_all_vocals",	# str (Option from: ['HP5_only_main_vocal', 'onnx_dereverb_By_FoxJoy', 'VR-DeEchoDeReverb', 'HP2_all_vocals', 'HP3_all_vocals', 'VR-DeEchoAggressive', 'VR-DeEchoNormal']) in 'Модели' Dropdown component
            "",	# str  in 'Путь к папке с аудиофайлами для обработки:' Textbox component
            "/tmp/",	# str  in 'Путь к папке для сохранения вокала:' Textbox component
            [f'/tmp/{msg.msg_id}_remover.wav'],	# List[str] (List of filepath(s) or URL(s) to files) in 'Можно также импортировать несколько аудиофайлов. Если путь к папке существует, то этот ввод игнорируется.' File component
            "/tmp/",	# str  in 'Путь к папке для сохранения аккомпанемента:' Textbox component
            0,	# int | float (numeric value between 0 and 20) in '人声提取激进程度' Slider component
            "mp3",	# str  in 'Формат выходных файлов' Radio component
            api_name="/uvr_convert"
        )

        vocal = '/tmp/'+subprocess.run(f'ls /tmp/ | grep "vocal_{msg.msg_id}"', shell=True, capture_output=True).stdout.decode().replace("\n","")
        vocal = open(vocal, 'rb').read()

        instrument = '/tmp/'+subprocess.run(f'ls /tmp/ | grep "instrument_{msg.msg_id}"', shell=True, capture_output=True).stdout.decode().replace("\n","")
        instrument = open(instrument, 'rb').read()

        #os.system(f'rm /tmp/instrument_{msg.msg_id}_remover.wav_0.mp3')
        #os.system(f'rm /tmp/vocal_{msg.msg_id}_remover.wav_0.mp3')
        #os.system(f'rm /tmp/{msg.msg_id}_remover.wav')

        for f in subprocess.run('ls /tmp/ | grep "149483"', shell=True, capture_output=True).stdout.decode().split("\n")[:-1]:
            os.system(f'rm /tmp/{f}')

        msg.sendAudio(vocal, name = f'[vocal] {attach["file_name"]}')
        msg.sendAudio(instrument, name = f'[instrument] {attach["file_name"]}')

plugins.init_plugin(RVCAudioVoice)
plugins.init_plugin(RVCAudioRemover)
