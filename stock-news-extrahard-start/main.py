import os

import requests
import datetime as dt
from twilio.rest import Client
from dotenv import load_dotenv

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY  = os.getenv("STOCK_API_KEY")
STOCK_NEWS_API_KEY = os.getenv("STOCK_NEWS_API_KEY")
auth_token = os.getenv("AUTH_TOKEN")
account_sid = os.getenv("ACCOUNT_SID")
sender_number = os.getenv("SENDER_NUMBER")
reciver_number = os.getenv("RECIVER_NUMBER")

STOCK_API_URI = f"https://www.alphavantage.co/query"
STOCK_NEWS_API = "https://newsapi.org/v2/everything"
SEND_MESSAGE = False


stock_params = {
    "function":  "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_API_KEY
}

# STEP 1: Use https://www.alphavantage.co
# TODO 1: When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get(STOCK_API_URI, params= stock_params)
data_dict = response.json()['Time Series (Daily)']
list_data = [data for data in data_dict.items()]
latest_date = list_data[0][0]
date = dt.datetime.strptime(latest_date, "%Y-%m-%d").date()
# print(date)
#day0 = 190.72             # To check if the code works change the value so it will be more than 5%
day0 = float(list_data[0][1]["4. close"])
day1 = float(list_data[1][1]["4. close"])
# print(f"This is the first day closing {day0} and this the second day closing {day1}")
def calculate_percentage_change(perivious_date_price, last_date_price):
     return ((last_date_price - perivious_date_price) / perivious_date_price)*100

percentage_change = calculate_percentage_change(day1,day0)

    # SEND_MESSAGE = True
# print("Get News")
# STEP 2: Use https://newsapi.org
# TODO 2: Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
stock_news_params = {
    "q": COMPANY_NAME,
    "from": date,
    "apikey": STOCK_NEWS_API_KEY

}
# response = requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={date}&apiKey={STOCK_NEWS_API_KEY}")
response = requests.get(STOCK_NEWS_API, params=stock_news_params)
data_news_dict = response.json()["articles"]
titles = []
articles =[]

titles.append(data_news_dict[0]["title"])
articles.append(data_news_dict[0]["description"])

titles.append(data_news_dict[1]["title"])
articles.append(data_news_dict[1]["description"])

titles.append(data_news_dict[2]["title"])
articles.append(data_news_dict[2]["description"])

# print(f"Titles:{titles}\nArticles:{articles}")

# STEP 3: Use https://www.twilio.com
# TODO 3: Send a seperate message with the percentage change and each article's title and description to your phone number.
client = Client(account_sid, auth_token)
if percentage_change > 5:
    for article_num in range(0,3):
        message = client.messages \
            .create(
            body=f"TSLA: 🔺{round(percentage_change)}%\nHeadline:{titles[article_num]}. (TSLA)?.\nBrief:{articles[article_num]}" ,
            from_=sender_number,
            to=reciver_number
        )
        print(message.status)

elif percentage_change < -5  :
    for article_num in range(0, 2):
        message = client.messages \
            .create(
            body=f"TSLA: 🔻{round(percentage_change)}%\nHeadline:{titles[article_num]}. (TSLA)?.\nBrief:{articles[article_num]}",
            from_=sender_number,
            to=reciver_number
        )
        # print(message.status)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

