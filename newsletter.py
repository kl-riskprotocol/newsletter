import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from coinmetrics.api_client import CoinMetricsClient
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import requests


# Ignore all warnings
warnings.filterwarnings('ignore')


sns.set_theme()
sns.set(rc={'figure.figsize':(16,8)})



api_key = "grlbZNpbW4WL3JhrPRPt"
client = CoinMetricsClient(api_key)

vol_metric_30d = 'volatility_realized_usd_rolling_30d'
vol_metric_7d = 'volatility_realized_usd_rolling_7d'
price_metric = "ReferenceRateUSD"



def last_hour_previous_sunday():
    # Get the current datetime
    now = datetime.now()
    # Calculate how many days to go back to the previous Sunday
    days_to_sunday = now.weekday() + 1  # Monday is 0, Sunday is 6
    # Get the previous Sunday's date
    previous_sunday = now - timedelta(days=days_to_sunday)
    # Get the last hour of Sunday (23:00)
    last_hour_sunday = datetime.combine(previous_sunday, datetime.min.time()) + timedelta(hours=23)
    return last_hour_sunday
 
    
 
def get_crypto_metrics(limit=20):
    """Fetch data and calculate metrics for top cryptocurrencies"""
    
    # Get list of top cryptocurrencies
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        top_cryptos = pd.DataFrame(response.json())
        
        
        return top_cryptos
    except:
        return pd.DataFrame()

all_cryptos = get_crypto_metrics(20)
currencies = list(all_cryptos.symbol)
others_currencies = currencies [-18:]
    
"""-----------""" 
"""   PRICE   """
"""           """
"""-----------"""

#btc and eth


price = client.get_asset_metrics(
        frequency="1h",
        assets= currencies,
        metrics=price_metric, 
        start_time= last_hour_previous_sunday() - timedelta(days=30),
        end_time = last_hour_previous_sunday() 
    ).to_dataframe()




price_btc =price[price.asset=='btc']
price_eth =price[price.asset=='eth']
price_others = price[price.asset.isin(['btc','eth']) == False]

price_btc_7d =price[price.asset=='btc'].tail(168)
price_eth_7d  =price[price.asset=='eth'].tail(168)
price_others_7d  = price[price.asset.isin(['btc','eth']) == False].tail(168)


price.to_csv('cryptos_prices.csv')
price_btc.to_csv('btc_prices.csv')
price_eth.to_csv('eth_prices.csv')
price_others.to_csv('others_prices.csv')

ax = plt.subplot()
for asset, data in price_btc_7d .groupby('asset'):
    sns.lineplot(data=data, y='ReferenceRateUSD', x='time', label=asset.upper())
ax.set_title('\nBTC Price\n', fontsize=20)
plt.setp(ax.get_xticklabels(), rotation=0, )
ax.set_facecolor("white")
plt.grid(color='black', linestyle='--', linewidth=0.2)
ax.set_xlabel("", fontsize=15)
ax.set_ylabel("Price\n",fontsize=15)
plt.legend(title='', frameon=False, bbox_to_anchor=(0.86, 1.13), loc='upper left', fontsize=12)

plt.savefig("btc_price.png", dpi=300, bbox_inches='tight')

plt.show()


ax = plt.subplot()
for asset, data in price_eth_7d .groupby('asset'):
    sns.lineplot(data=data, y='ReferenceRateUSD', x='time', label=asset.upper())
ax.set_title('\nETH Price\n', fontsize=20)
plt.setp(ax.get_xticklabels(), rotation=0, )
ax.set_facecolor("white")
plt.grid(color='black', linestyle='--', linewidth=0.2)
ax.set_xlabel("", fontsize=15)
ax.set_ylabel("Price\n",fontsize=15)
plt.legend(title='', frameon=False, bbox_to_anchor=(0.86, 1.13), loc='upper left', fontsize=12)

plt.savefig("eth_price.png", dpi=300, bbox_inches='tight')

plt.show()







"""-----------""" 
"""   VOLS    """
"""           """
"""-----------"""
vols = pd.DataFrame()
for asset, data in price.groupby('asset'):
    data= data.reset_index(drop = True)
    vols[asset]= data.ReferenceRateUSD.pct_change().rolling(7*24).std() * np.sqrt(24*365)

index= sorted(price.time.unique())
vols.index = index
vols = vols.dropna()


vols.to_csv('cryptos_realized_vols_7days_rolling_for_30days.csv')

vols_btc_eth = vols[['btc', 'eth']]

vols_btc_eth_7d = vols_btc_eth.tail(7*24)

ax = plt.subplot()
for asset in vols_btc_eth_7d.columns:
    data = vols_btc_eth_7d[asset].to_frame()
    data['time'] = data.index
    sns.lineplot(data=data, y=asset, x='time', label=asset.upper())
ax.set_title('\nBTC and ETH Realized Volatility * \n', fontsize=20)
plt.setp(ax.get_xticklabels(), rotation=0, )
ax.set_facecolor("white")
plt.grid(color='black', linestyle='--', linewidth=0.2)
ax.set_xlabel("", fontsize=15)
ax.set_ylabel("Realized Volatility\n",fontsize=15)
plt.legend(title='', frameon=False, bbox_to_anchor=(0.86, 1.13), loc='upper left', fontsize=12)

plt.savefig("btc_eth_realized_vols_7days_rolling_for_30days.png", dpi=300, bbox_inches='tight')

plt.show()




"""-----------""" 
"""   VOLS    """
"""           """
"""-----------"""


vol = client.get_asset_metrics(
    assets = ['btc','eth'],
    metrics = vol_metric_30d,
    frequency = '1h',
    start_time = last_hour_previous_sunday() - timedelta(days=7),
    end_time = last_hour_previous_sunday()
).to_dataframe()

vol.to_csv('cryptos_vols.csv')

ax = plt.subplot()
for asset, data in vol.groupby('asset'):
    sns.lineplot(data=data, y=vol_metric_30d, x='time', label=asset.upper())
ax.set_title('\nBTC and ETH Realized Vol (30D)\n', fontsize=20)
plt.setp(ax.get_xticklabels(), rotation=0, )
ax.set_facecolor("white")
plt.grid(color='black', linestyle='--', linewidth=0.2)
ax.set_xlabel("", fontsize=15)
ax.set_ylabel("Realized Volatility (24h)\n",fontsize=15)
plt.legend(title='', frameon=False, bbox_to_anchor=(0.86, 1.13), loc='upper left', fontsize=12)

plt.savefig("btc_eth_10m_rolling_24h_realized_vols_30d.png", dpi=300, bbox_inches='tight')

plt.show()





vol = client.get_asset_metrics(
    assets = ['btc','eth'],
    metrics = vol_metric_7d,
    frequency = '1h',
    start_time = last_hour_previous_sunday() - timedelta(days=7),
    end_time = last_hour_previous_sunday()
).to_dataframe()

vol.to_csv('cryptos_vols.csv')

ax = plt.subplot()
for asset, data in vol.groupby('asset'):
    sns.lineplot(data=data, y=vol_metric_7d, x='time', label=asset.upper())
ax.set_title('\nBTC and ETH Realized Vol (7D)\n', fontsize=20)
plt.setp(ax.get_xticklabels(), rotation=0, )
ax.set_facecolor("white")
plt.grid(color='black', linestyle='--', linewidth=0.2)
ax.set_xlabel("", fontsize=15)
ax.set_ylabel("Realized Volatility (7h)\n",fontsize=15)
plt.legend(title='', frameon=False, bbox_to_anchor=(0.86, 1.13), loc='upper left', fontsize=12)

plt.savefig("btc_eth_10m_rolling_24h_realized_vols_7d.png", dpi=300, bbox_inches='tight')

plt.show()





"""-----------""" 
"""   UPSIDE, DOWNSIDE    """
"""           """
"""-----------"""






currencies= [
'BTC',
'ETH',
'XRP',
'USDT',
'SOL',
'BNB',
'DOGE',
'USDC',
'ADA',
'STETH',
'TRX',
'LINK',
'AVAX',
'WSTETH',
'WBTC',
'SUI',
'XLM',
'TON',
'HBAR']

price = client.get_asset_metrics(
    assets = currencies,
    metrics = price_metric,
    frequency = '1h',
    start_time = datetime.now() - timedelta(days=30)
   
).to_dataframe()




















