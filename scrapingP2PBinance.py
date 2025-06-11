# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from datetime import datetime
#
# # 1. Configuración inicial
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
# }
# url = "https://p2p.binance.com/en/trade/all-payments?fiat=BOB"
#
#
# # 2. Función para hacer scraping
# def scrape_binance_p2p(url):
#     response = requests.get(url, headers=headers)
#     print(response.status_code)
#     soup = BeautifulSoup(response.text, 'lxml')
#     print(soup.select('table'))
#     ads = []
#
#     print('Outside for')
#     for ad in soup.select('table.bn-web-table-row bn-web-table-row-level-0'):  # Actualiza este selector según Binance
#         print('Inside for')
#         print(ad)
#         # try:
#         #     ads.append({
#         #         'Usuario': ad.select_one('.css-1x8dg53').text.strip(),
#         #         'Precio (EUR)': ad.select_one('.css-1m1f8hn').text.strip(),
#         #         'Límite Mín': ad.select_one('.css-vurnku + div').text.strip(),
#         #         'Límite Máx': ad.select_one('.css-vurnku + div + div').text.strip(),
#         #         'Método Pago': ad.select_one('.css-1x8dg53 + div').text.strip(),
#         #         'Fecha Scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         #     })
#         # except Exception as e:
#         #     print(f"Error extrayendo anuncio: {e}")
#         #     continue
#
#     return ads
#
#
# # 3. Ejecutar scraping y guardar en Excel
# ads = scrape_binance_p2p(url)
#
# print(ads)


import requests
import time
import json
from datetime import date

# Function to get binance p2p data
def get_p2p_ads_correct(trade_type, asset, fiat, page=1):
    #url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        #"Referer": f"https://p2p.binance.com/es/trade/{trade_type}/all-payments/{asset}?fiat={fiat}",
        "Referer": f"https://p2p.binance.com/en/trade/all-payments/USDT?fiat=BOB",
        "Origin": "https://p2p.binance.com",
    }

    payload = {
        "page": page,
        "rows": 10,
        "payTypes": [],
        "asset": asset,
        "fiat": fiat,
        "tradeType": trade_type
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx

        data = response.json()
        if data and data['code'] == '000000' and 'data' in data:
            return data['data']  # Esto devuelve la lista de anuncios
        else:
            print(f"Error o respuesta inesperada de la API P2P: {data}")
            return []

    except requests.exceptions.RequestException as e:
        #print(f"Error de red o HTTP: {e}")
        return []
    except ValueError:
        #print(f"Error al decodificar JSON: {response.text}")
        return []


# Fetch binance p2p api to get 10 pages data
ads_list = []
for number_of_pages in range(1, 21):
    ads = get_p2p_ads_correct(trade_type="BUY", asset="USDT", fiat="BOB", page=number_of_pages)
    ads_list += ads
    time.sleep(3)
    print(number_of_pages)


# Save data into json files everyday
current_date = date.today()
month = current_date.month
day = current_date.day
year = current_date.year

with open(f"data/{month}-{day}-{year}-buy-20-test.json", "w") as file:
    json.dump(ads_list, file)


#print(ads_list)

