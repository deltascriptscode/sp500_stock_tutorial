import pandas as pd
from datetime import datetime, timedelta, timezone
import numpy as np
import pickle
class SimulationTransformer(object):    
    def __init__(self,ticker,start,end,reporting_gap):
        self.start = start
        self.end = end
        self.ticker = ticker
        self.reporting_gap = reporting_gap

    def merge(self,price,funds,year,quarter,price_spaces):
        funds.reset_index(inplace=True)
        funds["filed"] = [datetime.strptime(str(x),"%Y%m%d").replace(tzinfo=timezone.utc) if "-" not in str(x) else \
                            datetime.strptime(str(x).split(" ")[0],"%Y-%m-%d").replace(tzinfo=timezone.utc) for x in funds["filed"]]
        funds["quarter"] = [x.quarter for x in funds["filed"]]
        funds["year"] = [x.year for x in funds["filed"]]
        for col in price.columns:
            price.rename(columns={col:col.lower().replace(price_spaces,"")},inplace=True)
        price["date"] = pd.to_datetime(price["date"],utc=True)
        price["quarter"] = [(x - timedelta(days=self.reporting_gap)).quarter for x in price["date"]]
        price["year"] = [(x - timedelta(days=self.reporting_gap)).year for x in price["date"]]
        funds = funds[(funds["year"] == year) & (funds["quarter"] == quarter)]
        price = price[(price["year"] == year) & (price["quarter"] == quarter)]
        final = price[["date","quarter","year","adjclose"]].merge(funds,on=["quarter","year"],how="left")
        final.drop_duplicates(inplace=True)
        cleaned = final[ (final["date"] >= datetime.strptime(self.start,"%Y-%m-%d").replace(tzinfo=timezone.utc)) \
                    & (final["date"] <= datetime.strptime(self.end,"%Y-%m-%d").replace(tzinfo=timezone.utc))]
        return cleaned