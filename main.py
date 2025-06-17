# Required imports:
from utils.data import Database
import pandas as pd

api = "YOUR_API_KEY_HERE"
test_database = Database(api)
symbol_list = ["IBM", "GOOG"]
test_database.build_database("test_database.db", symbol_list, outputsize='compact')
