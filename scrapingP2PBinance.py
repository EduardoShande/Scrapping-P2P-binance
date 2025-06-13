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
        "Referer": f"https://p2p.binance.com/en/trade/all-payments/{asset}?fiat=BOB",
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


# Use Binance P2P API to fetch the ads until the algorithm finds an empty list "[]", if so, it returns "[]"
ads_list = []
number_of_pages = 1
trade_type = str(input("Trade type (BUY/SELL): ")).upper().strip()
asset = str(input("Asset (USDT/USDC): ")).upper().strip()
if (trade_type == "BUY" or trade_type == "SELL") and (asset == "USDT" or asset == "USDC"):
    while True:
        ads = get_p2p_ads_correct(trade_type=trade_type, asset=asset, fiat="BOB", page=number_of_pages)
        if ads == []:
            print(ads)
            number_of_pages -= 1
            break
        ads_list += ads
        print(number_of_pages)
        number_of_pages += 1
        time.sleep(2)

    # Save data into json files everyday
    current_date = date.today()
    month = current_date.month
    day = current_date.day
    year = current_date.year

    with open(f"{asset}/{month}-{day}-{year}-{trade_type.lower()}-{number_of_pages}-test.json", "w") as file:
        json.dump(ads_list, file)


#print(ads_list)

