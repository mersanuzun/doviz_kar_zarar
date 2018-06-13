import requests

assets = [
    {
        'buying_price' : 4.3257,
        'quantity': 1155.87,
        'type': "USD"
    },
    {
        'buying_price': 4.3252,
        'quantity': 14.13,
        'type': "USD"
    },
    {
        'buying_price': 4.7897,
        'quantity': 330,
        'type': "USD"
    },
    {
        'buying_price': 4.4772,
        'quantity': 100,
        'type': "USD"
    },
    {
        'buying_price': 175.1149,
        'quantity': 28.54,
        'type': "GOLD"
    },
    {
        'buying_price': 197.4266,
        'quantity': 1.46,
        'type': "GOLD"
    },
    {
        'buying_price': 190.2179,
        'quantity': 5,
        'type': "GOLD"
    },
]

def calc_total_gain(assets, current_usd = None, current_gold = None):
    gain = 0

    for asset in assets:
        if asset['type'] == "USD" and current_usd is not None:
            each_asset_gain = (current_usd - asset["buying_price"]) * asset['quantity']
        elif asset['type'] == "GOLD" and current_gold is not None:
            each_asset_gain = (current_gold - asset["buying_price"]) * asset['quantity']
        else:
            each_asset_gain = 0
        gain += each_asset_gain

    return gain


gold_api = "https://altin.doviz.com/api/v1/golds/gram-altin/daily"
usd_api = "https://kur.doviz.com/api/v1/currencies/USD/daily"

try:
    usd_response = requests.get(usd_api)
    gold_response = requests.get(gold_api)
    if usd_response.status_code == 200 and gold_response.status_code == 200:
        usd_currencies = usd_response.json()
        golds = gold_response.json()
        usd_selling = usd_currencies[len(usd_currencies) - 1]['selling'] if usd_currencies else None
        gold_selling = golds[len(golds) - 1]['selling'] if golds else None
        total_gain = calc_total_gain(
            assets,
            current_usd=usd_selling,
            current_gold=gold_selling
        )

        print(
            "USD: " + str(usd_selling) + "\n"
            "GOLD: " + str(gold_selling) + "\n"
            "TOTAL GAIN: " + str(total_gain)  + "\n" 
            )
    else:
        print(
            "Response code is not OK.\n" + 
            "USD Response Code: {}\n".format(usd_response.status_code) + 
            "Gold Response Code: {}\n".format(gold_response.status_code)
        )
except Exception as e:
    print(
        "An error occured while fetching. Error: {}".format(e.message)
    )