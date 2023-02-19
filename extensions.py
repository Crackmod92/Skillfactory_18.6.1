import requests
import json
from config import currency

class ConvertException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def currency_convert(origin_cur=str, target_cur=str, amount=int):
        if origin_cur == target_cur:
            raise ConvertException(f'Конвертация {origin_cur} в {target_cur} невозможна.')
        try:
            origin_cur == currency[origin_cur]
        except KeyError:
            raise ConvertException('Эта валюта пока не доступна, либо допущена ошибка в названии.\n'
                                   'Попробуй еще раз.')
        try:
            target_cur == currency[target_cur]
        except KeyError:
            raise ConvertException('Эта валюта пока не доступна, либо допущена ошибка в названии.\n'
                                   'Попробуй еще раз.')
        try:
            amount == int(amount)
        except ValueError:
            raise ConvertException('Сумму необходимо внести целым числом.')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={currency[origin_cur]}&tsyms={currency[target_cur]}')
        currency_rate = json.loads(r.content)[currency[target_cur]]

        return currency_rate