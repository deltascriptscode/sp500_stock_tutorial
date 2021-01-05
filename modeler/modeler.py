from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
from datetime import datetime
import pickle
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.linear_model import LinearRegression
import warnings
warnings.simplefilter(action='ignore', category=Warning)

import pickle
class Modeler(object):
    def __init__(self,ticker):
        self.ticker = ticker
        self.params = {"booster":["gbtree", "gblinear", "dart"]}

    def model(self,data):
        lr = LinearRegression()
        X_train, X_test, y_train, y_test = train_test_split(data["X"], data["y"],
                                                train_size=0.75, test_size=0.25, random_state=42)
        lr.fit(X_train,y_train)
        confidence = lr.score(X_test,y_test)
        mse = abs(mean_squared_error(lr.predict(X_test),y_test)) * -1
        return {"ticker":self.ticker,"model":pickle.dumps(lr),"score":confidence,"mse":mse}