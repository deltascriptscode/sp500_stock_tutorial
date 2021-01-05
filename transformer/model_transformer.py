import pandas as pd
from datetime import datetime, timedelta, timezone
import numpy as np

class ModelTransformer(object):    
    def __init__(self,ticker,start,end,reporting_gap,training_years):
        self.ticker = ticker
        self.reporting_gap = reporting_gap
        self.training_years = training_years
        self.start = start
        self.end = end

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
        first_index = funds[(funds["year"] == year - self.training_years) & (funds["quarter"] == quarter)].index.values.tolist()[0]
        last_index = funds[(funds["year"] == year) & (funds["quarter"] == quarter)].index.values.tolist()[0]
        funds = funds.iloc[first_index:last_index]
        first_index = price[(price["year"] == year - self.training_years) & (price["quarter"] == quarter)].index.values.tolist()[0]
        last_index = price[(price["year"] == year) & (price["quarter"] == quarter)].index.values.tolist()[0]
        price = price.iloc[first_index:last_index]
        final = price[["date","year","quarter","adjclose"]].merge(funds,on=["year","quarter"],how="left")
        final.reset_index(inplace=True)
        cleaned = final.drop_duplicates()
        cleaned["date"] = [x.replace(tzinfo=timezone.utc) for x in cleaned["date"]]
        cleaned["filed"] = [x.replace(tzinfo=timezone.utc) for x in cleaned["filed"]]
        cleaned["reporting_gap"] = cleaned["date"] - cleaned["filed"]
        cleaned["reporting_gap"] = [x.days for x in cleaned["reporting_gap"]]
        product = cleaned[ (cleaned["date"] >= datetime.strptime(self.start,"%Y-%m-%d").replace(tzinfo=timezone.utc)) \
                            & (cleaned["date"] <= datetime.strptime(self.end,"%Y-%m-%d").replace(tzinfo=timezone.utc)) \
                            & (cleaned["reporting_gap"] <= self.reporting_gap)
                            ]
        product = product.groupby(by=["year","quarter"]).mean().reset_index().drop(["level_0","index"],axis=1)
        product["ticker"] = self.ticker
        return product
