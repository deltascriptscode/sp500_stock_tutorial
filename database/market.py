from pymongo import MongoClient, DESCENDING
import pandas as pd
from datetime import timedelta
from database.abank import ABank

class Market(ABank):
    def __init__(self,database_name):
        super().__init__(database_name)
    
    def retrieve_price_data(self,ticker):
        try:
            db = self.client[self.database_name]
            table = db["prices"]
            data = table.find({"ticker":ticker},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.database_name, "prices data pull",str(e))
            return None