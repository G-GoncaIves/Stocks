# Stocks - Alpha Vantage Financial Data Manager

A Python application for fetching, storing, and managing stock market data using the Alpha Vantage API with SQLite database integration.

## Overview

This project provides a streamlined solution for collecting and managing historical stock market data. Built with Python, it leverages the Alpha Vantage API to fetch daily time series data (OHLCV - Open, High, Low, Close, Volume) and stores it efficiently in SQLite databases for further analysis.

## Features

- **API Integration**: Seamless connection to Alpha Vantage's TIME_SERIES_DAILY endpoint
- **Database Management**: Automated SQLite database creation and updating
- **Duplicate Prevention**: Smart filtering to avoid redundant data entries during updates
- **Flexible Data Retrieval**: Support for both compact (100 days) and full (20+ years) historical data
- **Multi-Symbol Support**: Batch processing of multiple stock symbols
- **Data Validation**: Built-in error handling and data quality checks


## Installation

### Prerequisites

- Python 3.7+
- Alpha Vantage API key (free at https://www.alphavantage.co/support/#api-key)

### Required Dependencies

pip install pandas requests sqlite3

## Quick Start

### 1. Setup Your API Key

Replace the placeholder API key in 'main.py':

api = "YOUR_ALPHA_VANTAGE_API_KEY_HERE"


### 2. Basic Usage
## Initialize the database connection

api_key = "YOUR_API_KEY"
stock_db = Database(api_key)

## Define symbols to track
symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]

## Build initial database (creates new tables)
stock_db.build_database("stocks.db", symbols, outputsize='compact')

## Update database with new data (avoids duplicates)
stock_db.update_database("stocks.db", symbols, outputsize='compact')


## Core Functionality

### Database Class Methods

#### `build_database(database_path, symbol_list, outputsize='compact')`
Creates new database tables for specified symbols, replacing any existing data. Ideal for initial setup or complete data refresh.

#### `update_database(database_path, symbol_list, outputsize='compact')`
Adds only new data entries to existing tables, preventing duplicates through intelligent filtering. Perfect for regular data updates.

#### `fetch_symbol_data(symbol, outputsize)`
Retrieves raw JSON data from Alpha Vantage API for a specific stock symbol. Handles API communication and error responses.

#### `get_symbol_df(data)`
Converts API JSON response into a clean pandas DataFrame with properly typed columns. Includes data validation and formatting.

#### `filter_symbol_df(symbol_df, symbol, conn)`
Filters new data against existing database entries to prevent duplicates. Only returns rows newer than the latest database entry.

## Configuration Options

### Output Size Parameters

- **`compact`** (default): Returns latest 100 trading days
- **`full`**: Returns complete historical data (20+ years)

### Data Structure

Each stock symbol creates a table with the following columns:
- `index`: Date (YYYY-MM-DD format)
- `open`: Opening price
- `high`: Highest price of the day  
- `low`: Lowest price of the day
- `close`: Closing price
- `volume`: Trading volume

## API Limitations

- **Free Tier**: 5 API calls per minute, 500 calls per day
- **Premium Plans**: Available for higher usage requirements
- **Data Freshness**: Updates typically available after market close

## Support

For Alpha Vantage API documentation and support, visit: https://www.alphavantage.co/documentation/
