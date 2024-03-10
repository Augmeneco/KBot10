import datetime, requests
import plugin as plugins
from config import config

class Weather:
	level = 1
	names = ['погода','weather']
	desc = 'Погода'

	def execute(self, msg):
		if msg.user_text == '':
			msg.user_text = 'Санкт-Петербург'
		def format_weather(city):
			#proxies = {'http':'socks5h://localhost:9050','https':'socks5h://localhost:9050'}
			weather = requests.get('http://api.openweathermap.org/data/2.5/weather', params={'lang':'ru', 'units': 'metric', 'APPID': 'ef23e5397af13d705cfb244b33d04561', 'q':city}).json()
			#print(weather)
			try:
				out=""
				out+="Погода в " + str(weather['sys']['country']) + "/" + weather['name'] + ":\n"
				out+='&#8195;•Температура: ' + str(weather['main']['temp']) + '°C\n'
				out+='&#8195;•Скорость ветра: ' + str(weather['wind']['speed']) + ' м/с\n'
				out+='&#8195;•Влажность: ' + str(weather['main']['humidity']) + '%\n'
				out+='&#8195;•Состояние: ' + str(weather['weather'][0]['description']) + "\n"
				out+='&#8195;•Давление: ' + ('%0.2f' % (float(weather['main']['pressure'])/1000*750.06))+"\n"
				out+='Время обновления: ' + datetime.datetime.fromtimestamp(weather["dt"]).strftime('%I:%M%p');
				return out
			except AttributeError:
				return None

		def translit(x):
			symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
				u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
			tr = {ord(a):ord(b) for a, b in zip(*symbols)}
			return tounicode(x).translate(tr)

		out = format_weather(msg.user_text)
		if out == None:
			out = format_weather(msg.user_text)
		if out == None:
			msg.sendMessage('Я не нашла населённый пункт '+msg.user_text)
			return
		msg.sendMessage(out, parse_mode='HTML')

plugins.init_plugin(Weather)
