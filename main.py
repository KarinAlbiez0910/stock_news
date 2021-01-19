import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "TQ6XEGDZHL6VHVJY"
STOCK_API_URL = "https://www.alphavantage.co/query"
NEWS_API_KEY = "472e9b13f33c4b5bbaf491fd03d73b0f"
NEWS_API_URL = "https://newsapi.org/v2/everything"


#Twilio data
api_key = os.environ.get('OWM_API_KEY')
phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
my_phone_number = os.environ.get("MY_PHONE_NUMBER")


# get the TESLA stock close price for the two most recent days


stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY

}
response = requests.get(STOCK_API_URL, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()

my_stock_list = [value for key, value in stock_data['Time Series (Daily)'].items()]

close_most_current = float(my_stock_list[0]['4. close'])
print(close_most_current)

close_day_earlier = float(my_stock_list[1]['4. close'])


difference_in_price = abs(close_most_current-close_day_earlier)
difference_in_percentage = difference_in_price/(close_most_current/100)
difference_in_percentage = round(difference_in_percentage,2)

def evaluate_price_difference():
    if close_most_current > close_day_earlier:
        return f'{STOCK}:🔺{difference_in_percentage}'
    else:
        return f'{STOCK}:🔻{difference_in_percentage}'

# get the first three news pieces for the company name "Tesla"

news_parameters = {
    'q': 'Tesla',
    'apiKey': NEWS_API_KEY
}

news_response = requests.get(NEWS_API_URL, params=news_parameters)

news_response.raise_for_status()

news_data = news_response.json()

news_list_recreated = []
for news_dict in news_data['articles'][:3]:
    news_dict_recreated= {'Headline': news_dict['title'],
                             'Brief': news_dict['description']}
    news_list_recreated.append(news_dict_recreated)

print(news_list_recreated)

brief = news_list_recreated[2]['Brief']
print(brief)
brief_list = brief.split('.')
brief_list = brief_list[:-1]
print(".".join(brief_list))


# Send a message via Twilio containing the difference in stock price (in percentage)
# and the heading and description of the three first news pieces

for item in news_list_recreated:
   stock_movement = evaluate_price_difference()
   brief_list = item['Brief'].split('.')
   brief_list = brief_list[:-1]
   brief_reformatted = ".".join(brief_list)
   headline = f"Headline: {item['Headline']}"
   brief = f"Brief: {brief_reformatted}"
   client = Client(account_sid, auth_token)
   message = client.messages \
       .create(
      body=f'{stock_movement}\n{headline}\n{brief}',
      from_=phone_number,
      to=my_phone_number
    )

   print(message.status)


