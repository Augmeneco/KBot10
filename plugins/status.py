import psutil
import plugin
import re
import subprocess
import os

class Status:
	names = ['стат','статус','stat','status']
	desc = 'Информация о сервере'
	level = 1

	def execute(self, msg):
		counter = 1
		text = '[ Статистика ]\nСистема:\n&#8195;Процессор:\n'

		for idx, cpu in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
			if counter == 1:
				text += '&#8195;&#8195;Ядро №'+str(idx+1)+': '+str(round(cpu,1))+'%'
				counter = 2
			elif counter == 2:
				text += ' | Ядро №'+str(idx+1)+': '+str(round(cpu,1))+'%\n'
				counter = 1

		mem = psutil.virtual_memory()
		MB = 1024 * 1024

		vram = subprocess.run('nvidia-smi', shell=True, capture_output=True).stdout.decode()
		vram = re.findall('W\s\/\s.+?W.+?(\d+).+?(\d+)', vram)[0]

		text += '\n&#8195;ОЗУ:\n&#8195;&#8195;Всего: '+str(int(mem.total / MB))+'MB\n'
		text += '&#8195;&#8195;Использовано: '+str(int((mem.total - mem.available) / MB))+'MB\n'
		text += '&#8195;&#8195;Свободно: '+str(int(mem.available / MB))+'MB\n'
		text += '&#8195;&#8195;Использовано ботом: '+str(int(psutil.Process().memory_info().rss / MB))+'MB\n\n'

		if os.path.exists('/usr/bin/nvidia-smi'):
			text += f'&#8195;Видеопамять:\n&#8195;&#8195;Всего: {vram[1]} MB\n'
			text += f'&#8195;&#8195;Использовано: {vram[0]} MB\n'
			text += f'&#8195;&#8195;Свободно: {int(vram[1])-int(vram[0])} MB\n'

		msg.sendMessage(text, parse_mode='HTML')

plugin.init_plugin(Status)
