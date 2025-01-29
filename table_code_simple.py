

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

def calculate_returns(prices):
    """Calculate returns for different time periods"""
    if len(prices) == 0:
        return None, None, None, None
    
    returns = pd.Series(prices).pct_change().dropna()
    
    # Get returns for different periods
    one_day = (prices[-1] / prices[-2] - 1) if len(prices) >= 2 else np.nan
    seven_day = (prices[-1] / prices[-8] - 1) if len(prices) >= 8 else np.nan
    thirty_day =  (prices[-1] / prices[-31] - 1) if len(prices) >= 31 else np.nan
    six_month = (prices[-1] / prices[-180] - 1) if len(prices) >= 180 else np.nan
    one_year = (prices[-1] / prices[-365] - 1) if len(prices) >= 365 else np.nan
    
    return one_day, seven_day,  thirty_day, six_month, one_year

def calculate_volatilities(returns, period):
    """Calculate total, upside, and downside volatilities"""
    if len(returns) < period:
        return np.nan, np.nan, np.nan
    
    # Get the last 'period' returns
    recent_returns = returns[-period:]
    
    # Total volatility (annualized)
    total_vol = np.std(recent_returns) * np.sqrt(365)
    
    # Upside volatility (positive returns only)
    upside_returns = recent_returns[recent_returns > 0]
    upside_vol = np.std(upside_returns) * np.sqrt(365) if len(upside_returns) > 0 else np.nan
    
    # Downside volatility (negative returns only)
    downside_returns = recent_returns[recent_returns < 0]
    downside_vol = np.std(downside_returns) * np.sqrt(365) if len(downside_returns) > 0 else np.nan
    
    return total_vol, upside_vol, downside_vol

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
        top_cryptos = response.json()
        
        # Initialize results dictionary
        results = []
        
        # Get historical data for each crypto
        
        
        list_list =[]
        for k in [0,10,]:
            list_list.append(top_cryptos[k: k+10])
            
        
        
        
        for top_cryptos_l in list_list:
            
            missings= []
        
            for crypto in top_cryptos_l:
                print(f"Processing {crypto['name']}...")
                
                # Get historical prices (daily) for the past year
                hist_url = f"https://api.coingecko.com/api/v3/coins/{crypto['id']}/market_chart"
                hist_params = {
                    'vs_currency': 'usd',
                    'days': 365,
                    'interval': 'hourly'
                }
                
                try:
                    hist_response = requests.get(hist_url, params=hist_params)
                    hist_response.raise_for_status()
                    price_data = hist_response.json()['prices']
                    
                    # Extract prices and calculate daily returns
                    prices = [p[1] for p in price_data]
                    returns = pd.Series(prices).pct_change().dropna()
                    
                    # Calculate returns
                    one_day_ret, seven_day_ret, thirty_day_ret , six_month_ret, one_year_ret = calculate_returns(prices)
                    
                    # Calculate volatilities for different periods
                    seven_day_vol, seven_day_up, seven_day_down = calculate_volatilities(returns, 7)
                    thirty_day_vol, thirty_day_up, thirty_day_down = calculate_volatilities(returns, 30)
                    six_month_vol, six_month_up, six_month_down = calculate_volatilities(returns, 180)
                    one_year_vol, one_year_up, one_year_down = calculate_volatilities(returns, 365)
                    
                    results.append({
                        'Symbol': crypto['symbol'].upper(),
                        'Name': crypto['name'],
                        'Market Cap': crypto['market_cap'],
                        # '1d Return': one_day_ret,
                        # '7d Return': seven_day_ret,
                         '30d Return': thirty_day_ret,
                        # '6m Return': six_month_ret,
                        # '1y Return': one_year_ret,
                        # '7d Volatility': seven_day_vol,
                        '30d Volatility': thirty_day_vol,
                        # '6m Volatility': six_month_vol,
                        # '1y Volatility': one_year_vol,
                        # '7d Upside Vol': seven_day_up,
                        '30d Upside Vol': thirty_day_up,
                        # '6m Upside Vol': six_month_up,
                        # '1y Upside Vol': one_year_up,
                        # '7d Downside Vol': seven_day_down,
                        '30d Downside Vol': thirty_day_down,
                        # '6m Downside Vol': six_month_down,
                        # '1y Downside Vol': one_year_down
                    })
                    
                    # Sleep to avoid hitting API rate limits
                    time.sleep(10)
                

                
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching historical data for {crypto['name']}: {e}")
                    missings.append(crypto)
                    continue
                
            print('pause one minute')   
            time.sleep(61)
            
            

            for crypto in missings:
                print(f"Processing {crypto['name']}...")
                
                # Get historical prices (daily) for the past year
                hist_url = f"https://api.coingecko.com/api/v3/coins/{crypto['id']}/market_chart"
                hist_params = {
                    'vs_currency': 'usd',
                    'days': 365,
                    'interval': 'hourly'
                }
                
                try:
                    hist_response = requests.get(hist_url, params=hist_params)
                    hist_response.raise_for_status()
                    price_data = hist_response.json()['prices']
                    
                    # Extract prices and calculate daily returns
                    prices = [p[1] for p in price_data]
                    returns = pd.Series(prices).pct_change().dropna()
                    
                    # Calculate returns
                    one_day_ret, seven_day_ret, thirty_day_ret , six_month_ret, one_year_ret = calculate_returns(prices)
                    
                    # Calculate volatilities for different periods
                    seven_day_vol, seven_day_up, seven_day_down = calculate_volatilities(returns, 7)
                    thirty_day_vol, thirty_day_up, thirty_day_down = calculate_volatilities(returns, 30)
                    six_month_vol, six_month_up, six_month_down = calculate_volatilities(returns, 180)
                    one_year_vol, one_year_up, one_year_down = calculate_volatilities(returns, 365)
                    
                    results.append({
                        'Symbol': crypto['symbol'].upper(),
                        'Name': crypto['name'],
                        'Market Cap': crypto['market_cap'],
                        # '1d Return': one_day_ret,
                        # '7d Return': seven_day_ret,
                         '30d Return': thirty_day_ret,
                        # '6m Return': six_month_ret,
                        # '1y Return': one_year_ret,
                        # '7d Volatility': seven_day_vol,
                        '30d Volatility': thirty_day_vol,
                        # '6m Volatility': six_month_vol,
                        # '1y Volatility': one_year_vol,
                        # '7d Upside Vol': seven_day_up,
                        '30d Upside Vol': thirty_day_up,
                        # '6m Upside Vol': six_month_up,
                        # '1y Upside Vol': one_year_up,
                        # '7d Downside Vol': seven_day_down,
                        '30d Downside Vol': thirty_day_down,
                        # '6m Downside Vol': six_month_down,
                        # '1y Downside Vol': one_year_down
                    })
                    
                    # Sleep to avoid hitting API rate limits
                    time.sleep(61)
                

                
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching historical data for {crypto['name']}: {e}")
                    missings.append(crypto)
                    continue
                
           

            
            
            
            
        # Create DataFrame
        df = pd.DataFrame(results)
        
        df['U/D Ratio'] = df['30d Upside Vol']  / df['30d Downside Vol']
        
        # Format percentage columns
        pct_columns = [col for col in df.columns if 'Return' in col or 'Vol' in col]
        for col in pct_columns:
            df[col] = df[col].map('{:.2%}'.format)
            
        # Format market cap
        df['Market Cap'] = df['Market Cap'].map('${:,.0f}'.format)
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top cryptocurrencies: {e}")
        return None

if __name__ == "__main__":
    # Get metrics for top 100 cryptocurrencies
    df = get_crypto_metrics(20)
    
    
    
    if df is not None:
        # Display settings
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.float_format', '{:.2%}'.format)
        
        print("\nCryptocurrency Metrics Analysis")
        print(f"Data as of: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("-" * 100)
        print(df)
        
        # Optionally save to CSV
        df.to_csv('crypto_metrics.csv', index=False)
        
        
        html = df.to_html(classes=['sortable'], table_id='myTable')
        
        # Full HTML with sorting functionality
        
       
      
        
        
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
            <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
            <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
            
            
            
            <script>
                $(document).ready(function() {{
                    $('#myTable').DataTable();
                }});
            </script>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Save to file
        with open('table.html', 'w') as f:
            f.write(html_template)
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        