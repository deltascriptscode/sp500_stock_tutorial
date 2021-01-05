from pymongo import MongoClient, DESCENDING
import pandas as pd
from datetime import timedelta
from database.abank import ABank

class SEC(ABank):
    def __init__(self):
        super().__init__("sec")

    def retrieve_sub_cik(self):
        try:
            db = self.client[self.database_name]
            table = db["subs"]
            data = table.find({},{"cik":1,"adsh":1,"filed":1},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.database_name,"cik data pull",str(e))
            return None

    def retrieve_num_data(self,adsh):
        try:
            db = self.client[self.database_name]
            table = db["nums"]
            data = table.find({"adsh":adsh},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.database_name,"num data pull",str(e))
            return None
    
    def retrieve_filing_data(self,cik):
        try:
            db = self.client[self.database_name]
            table = db["filings"]
            data = table.find({"cik":cik},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.database_name, "filing data pull",str(e))
            return None
    