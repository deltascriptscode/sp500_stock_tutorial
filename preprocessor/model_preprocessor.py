from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
from datetime import datetime
class ModelPreprocessor(object):
    def __init__(self,ticker):
        self.ticker = ticker
    
    def fundamental_preprocess(self,data):
        drop_columns = ["quarter","year","ticker","adjclose","index","_id","id","date","adsh","cik","filed","level_0","reporting_gap"]
        data.fillna(0,inplace=True)
        num_pipeline = Pipeline([
            ('normalizer',Normalizer())
            ])
        features = data.drop(drop_columns,axis=1,errors="ignore").copy()
        processed = pd.DataFrame(num_pipeline.fit_transform(features),columns=features.columns,index=features.index)
        return {"X":processed,"y":data["adjclose"]}