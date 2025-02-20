import requests
import json
from config import keyss
keyss1 =keyss
LIMIT_AMOUNT = 9999999
class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: float) -> float:
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        if amount <= 0:
            raise APIException('Укажите конвертируемую сумму больше 0 ')

        if amount > LIMIT_AMOUNT:
            raise  APIException(f'Укажите конвертируемую сумму которая не превышает лимиты {LIMIT_AMOUNT}')

        try:
            quote_ticker = keyss1[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}, проверьте есть ли валюта "{quote}" в списке /values')

        try:
            base_ticker = keyss1[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}, проверьте есть ли валюта "{base}" в списке /values' )
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keyss1[base]]
        return total_base * amount
