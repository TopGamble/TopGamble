import requests
import time
from colorama import Fore, Style, init

# Инициализация colorama для цветного вывода
init(autoreset=True)

# Ваш API-ключ PolygonScan, добавьте его
API_KEY = ''
# Адрес кошелька отправителя (ваш адрес)
SENDER_ADDRESS = '0x71E1f1e847293b96731d867425F3fdAC0E8a3E21'
# Контракт NFT (Season 4 Alpha Pass)
CONTRACT_ADDRESS = '0xcC2b3af01361194f269f887528498A9f5E30d928'

# Функция для получения данных о последних NFT транзакциях
def get_nft_transfers():
    url = f'https://api.polygonscan.com/api?module=account&action=tokennfttx&address={SENDER_ADDRESS}&startblock=0&endblock=999999999&sort=desc&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    # Проверяем, что запрос успешен и возвращает данные
    if data['status'] == '1' and data['message'] == 'OK':
        return data['result']
    else:
        return []

# Функция для фильтрации транзакций по контракту и времени
def filter_season_4_pass(transfers): 
    current_time = int(time.time())
    filtered_transactions = []
    
    for tx in transfers:
        contract = tx['contractAddress'].lower()
        timestamp = int(tx['timeStamp'])
        
        # Фильтруем транзакции по контракту и по времени (последние 5000 секунд)
        if contract == CONTRACT_ADDRESS.lower() and (current_time - timestamp <= 15000):
            filtered_transactions.append(tx)
    
    return filtered_transactions

# Функция для отправки уведомления (вывод в консоль)
def send_notification(count):
    if count >= 3:
        print(Fore.GREEN + Style.BRIGHT + f"ALERT! Found {count} 'Season 4 Alpha Pass' transactions in the last 5,000 seconds.")
    else:
        print(Fore.RED + Style.BRIGHT + "Less than 3 'Season 4 Alpha Pass' transactions found in the last 5,000 seconds.")

# Основной цикл для отслеживания транзакций
def track_transactions():
    while True: 
        # Получаем новые трансферы
        transfers = get_nft_transfers()
        
        # Фильтруем по контракту и времени
        season_4_pass_transfers = filter_season_4_pass(transfers)
        
        # Подсчитываем количество транзакций
        transaction_count = len(season_4_pass_transfers)
        
        # Отправляем уведомление
        send_notification(transaction_count)
        
        # Ожидаем перед следующим запросом 20 секунд
        time.sleep(50)

if __name__ == '__main__':
    track_transactions()
