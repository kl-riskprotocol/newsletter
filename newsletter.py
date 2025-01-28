import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from coinmetrics.api_client import CoinMetricsClient
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Ignore all warnings
warnings.filterwarnings('ignore')


sns.set_theme()
sns.set(rc={'figure.figsize':(16,8)})



api_key = "grlbZNpbW4WL3JhrPRPt"
client = CoinMetricsClient(api_key)

vol_metric = 'volatility_realized_usd_rolling_30d'
price_metric = "ReferenceRateUSD"

currencies= ['BTC', 'ETH',
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

others_currencies= [
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
 
    
"""-----------""" 
"""   PRICE   """
"""           """
"""-----------"""

#btc and eth


price = client.get_asset_metrics(
        frequency="1h",
        assets= ['btc','eth'],
        metrics=price_metric, 
        start_time= last_hour_previous_sunday() - timedelta(days=7)
    ).to_dataframe()

price.to_csv('cryptos_prices.csv')


price_btc =price[price.asset=='btc']
price_eth =price[price.asset=='eth']

ax = plt.subplot()
for asset, data in price_btc.groupby('asset'):
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
for asset, data in price_eth.groupby('asset'):
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

#others


price_others = client.get_asset_metrics(
        frequency="1h",
        assets= others_currencies,
        metrics=price_metric, 
        start_time= last_hour_previous_sunday() - timedelta(days=7)
    ).to_dataframe()

price_others.to_csv('others_cryptos_prices.csv')











"""-----------""" 
"""   VOLS    """
"""           """
"""-----------"""


vol = client.get_asset_metrics(
    assets = ['btc','eth'],
    metrics = vol_metric,
    frequency = '1h',
    start_time = last_hour_previous_sunday() - timedelta(days=7)
).to_dataframe()

vol.to_csv('cryptos_vols.csv')

ax = plt.subplot()
for asset, data in vol.groupby('asset'):
    sns.lineplot(data=data, y=vol_metric, x='time', label=asset.upper())
ax.set_title('\nBTC and ETH Realized Vol\n', fontsize=20)
plt.setp(ax.get_xticklabels(), rotation=0, )
ax.set_facecolor("white")
plt.grid(color='black', linestyle='--', linewidth=0.2)
ax.set_xlabel("", fontsize=15)
ax.set_ylabel("Realized Volatility (24h)\n",fontsize=15)
plt.legend(title='', frameon=False, bbox_to_anchor=(0.86, 1.13), loc='upper left', fontsize=12)

plt.savefig("btc_eth_10m_rolling_24h_realized_vols.png", dpi=300, bbox_inches='tight')

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

vol = client.get_asset_metrics(
    assets = currencies,
    metrics = 'volatility_realized_usd_rolling_30d',
    frequency = '1h',
    start_time = datetime.now() - timedelta(days=7)
   
).to_dataframe()

ax = plt.subplot()
for asset, data in vol.groupby('asset'):
    sns.lineplot(data=data, y=vol_metric, x='time', label=asset.upper())
ax.set_title('\nBTC and ETH Realized Vol\n', fontsize=20)
plt.setp(ax.get_xticklabels(), rotation=0, )
ax.set_facecolor("white")
plt.grid(color='black', linestyle='--', linewidth=0.2)
ax.set_xlabel("", fontsize=15)
ax.set_ylabel("Realized Volatility (24h)\n",fontsize=15)
plt.legend(title='', frameon=False, bbox_to_anchor=(0.86, 1.13), loc='upper left', fontsize=12)

plt.savefig("20_main_cryptos_rolling_24h_realized_vols.png", dpi=300, bbox_inches='tight')

plt.show()


