import sqlite3
import requests
import json
import pandas as pd
class Database():
    
    def __init__(self, api):
        """
        Initialize the database
        """
        self.api = api
            
    def update_database(self, database_path, symbol_list, outputsize='compact'):
        """
        Update the database, only appending new rows (no duplicates).
        """
        conn = sqlite3.connect(database_path)
        for symbol in symbol_list:
            symbol_data = self.fetch_symbol_data(symbol, outputsize)
            symbol_df = self.get_symbol_df(symbol_data)
            filtered_symbol_df = self.filter_symbol_df(symbol_df, symbol, conn)
            filtered_symbol_df.to_sql(
                symbol, 
                conn, 
                if_exists='append', 
                index=False
            )
        conn.close()
    
    def build_database(self, database_path, symbol_list, outputsize='compact'):
        """
        Build the database
        """
        for symbol in symbol_list:
            symbol_data =self.fetch_symbol_data(symbol, outputsize)
            symbol_df = self.get_symbol_df(symbol_data)
            symbol_df.to_sql(
                symbol, 
                sqlite3.connect(database_path), 
                if_exists='replace', 
                index=False
            )
    
    def fetch_symbol_data(self, symbol, outputsize):
        """
        Fetch the data from the API
        """
        url = 'https://www.alphavantage.co/query?' +\
            'function=TIME_SERIES_DAILY&' +\
            f'symbol={symbol}&' +\
            f'outputsize={outputsize}&' +\
            f'apikey={self.api}'
        r = requests.get(url)
        data = r.json()
        return data
    
    def filter_symbol_df(self, symbol_df, symbol, conn):
        """
        Filter the symbol dataframe
        """
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{symbol}'"
        if pd.read_sql(query, conn).empty:
            raise ValueError(f"Table {symbol} does not exist in the database.")
        latest_date_query = f"SELECT MAX([index]) as max_date FROM '{symbol}'"
        result = pd.read_sql(latest_date_query, conn)
        latest_date = result['max_date'][0]
        symbol_df = symbol_df[symbol_df['index'] > latest_date]
        if symbol_df.empty:
            raise ValueError(f"No new data found for symbol {symbol} in the database.")
        return symbol_df
        
    def get_symbol_df(self, data):
        """
        Convert the data from the API to a pandas dataframe
        """
        time_series = data.get('Time Series (Daily)', {})
        if not time_series:
            raise ValueError(f"No time series data found for symbol.")
        df = pd.DataFrame(time_series).T
        df.columns = [col.split('. ')[1] for col in df.columns]
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": int})
        df = df.sort_index(ascending=False)
        df.reset_index(inplace=True)
        return df
