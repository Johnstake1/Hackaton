import requests
import datetime

api_key = 'T0U2N0S0893JDY1H'
symbol = 'SPY'
function = 'TIME_SERIES_DAILY'
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SPY&apikey=T0U2N0S0893JDY1H'

response = requests.get(url)
data = response.json()

print(data)
