import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time

st.set_page_config(layout="wide")

st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from **CoinMarketCap**!
""")

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
""")

col1 = st.sidebar
col2, col3 = st.columns((2, 1))

col1.header('Input Options')

currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

@st.cache
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'lxml')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
      coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    marketCapByTotalSupply = []
    percentChange1h = []
    percentChange24h = []
    percentChange7d = []
    price = []
    volume24h = []

    for i in listings:
      coin_name.append(i['slug'])
      coin_symbol.append(i['symbol'])
      price.append(i['quote'][currency_price_unit]['price'])
      percentChange1h.append(i['quote'][currency_price_unit]['percentChange1h'])
      percentChange24h.append(i['quote'][currency_price_unit]['percentChange24h'])
      percentChange7d.append(i['quote'][currency_price_unit]['percentChange7d'])
      marketCapByTotalSupply.append(i['quote'][currency_price_unit]['marketCapByTotalSupply'])
      volume24h.append(i['quote'][currency_price_unit]['volume24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'marketCapByTotalSupply', 'percentChange1h', 'percentChange24h', 'percentChange7d', 'price', 'volume24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percentChange1h'] = percentChange1h
    df['percentChange24h'] = percentChange24h
    df['percentChange7d'] = percentChange7d
    df['marketCapByTotalSupply'] = marketCapByTotalSupply
    df['volume24h'] = volume24h
    return df

df = load_data()

sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[(df['coin_symbol'].isin(selected_coin))]

num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d', '24h', '1h'])
percent_dict = {"7d": 'percentChange7d', "24h": 'percentChange24h', "1h": 'percentChange1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h, df_coins.percentChange7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percentChange1h'] = df_change['percentChange1h'] > 0
df_change['positive_percentChange24h'] = df_change['percentChange24h'] > 0
df_change['positive_percentChange7d'] = df_change['percentChange7d'] > 0
col2.dataframe(df_change)

col3.subheader('Bar plot of % Price Change')

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange7d'])
    col3.write('*7 days period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange7d'].plot(kind='barh', color=df_change.positive_percentChange7d.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange24h'])
    col3.write('*24 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange24h'].plot(kind='barh', color=df_change.positive_percentChange24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange1h'])
    col3.write('*1 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange1h'].plot(kind='barh', color=df_change.positive_percentChange1h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)


