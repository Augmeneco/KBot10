import plugin as plugins
from config import config
import requests
import re

class TF2Rate:
    names = ['курс', 'тф2', 'course']
    desc = 'Курс валют TF2'
    level = 1

    def execute(self, msg):
        url = 'https://backpack.tf/api'
        key = config.config['backpacktf']

        usd_rate_steam = requests.get('https://api.steam-currency.ru/currency').json()['data'][0]['close_price']
        currencies_backpack = requests.get(f'{url}/IGetCurrencies/v1', params={'key':key}).json()['response']['currencies']
        ticket_ref = requests.get(f'{url}/IGetPriceHistory/v1',
            params = {
                'appid': 440,
                'item': 'Tour of Duty Ticket',
                'quality': 6,
                'priceindex': 0,
                'key': key
            }
        ).json()['response']['history'][-1]['value']

        currencies_lavka = requests.get('https://tf2lavka.ru/#product').text
        key_cost_lavka = int(float(re.search('(?:(\d+?\.\d+?)|(\d+?))₽\/шт', currencies_lavka).group(1)) * 1.085)

        key_cost_steam = requests.get('https://steamcommunity.com/market/priceoverview/?country=RU&currency=5&appid=440&market_hash_name=Mann%20Co.%20Supply%20Crate%20Key').json()['lowest_price']
        key_cost_steam = float(key_cost_steam.replace(' pуб.','').replace(',','.'))

        out =  f'Курс стима 1$ = {usd_rate_steam}₽\n\n'

        out += f'1 ключ в стиме: {key_cost_steam}₽\n'
        out += f'1 ключ на тф2лавке: {key_cost_lavka}₽ | {round((key_cost_steam/key_cost_lavka-1)*100, 2)}% выгоды\n'
        out += f'Цена ключа после продажи в стиме: {round(key_cost_steam/1.15, 2)}₽\n\n'

        ar_key_cost_steam = requests.get('https://steamcommunity.com/market/priceoverview/?country=AR&currency=1&appid=440&market_hash_name=Mann%20Co.%20Supply%20Crate%20Key').json()['lowest_price']
        ar_key_cost_steam = float(ar_key_cost_steam.replace('$', '').replace(' USD', ''))
        cis_sell = ar_key_cost_steam * usd_rate_steam
        cis_sell = round(cis_sell/1.15, 2)
        ru_sell = round(key_cost_steam/1.15, 2)

        out += f'Цена ключа после продажи для Аргентины: {round(ar_key_cost_steam/1.15, 2)}$ | {cis_sell}₽\n'
        out += f'Хуже рубля на {round((ru_sell/cis_sell-1)*100,2)}%\n\n'
        
        out += f"1 ключ = {currencies_backpack['keys']['price']['value']} рефов"
        out += f" = {round(currencies_backpack['keys']['price']['value']/ticket_ref, 2)} билетов"

        msg.sendMessage(out)

        
plugins.init_plugin(TF2Rate)
