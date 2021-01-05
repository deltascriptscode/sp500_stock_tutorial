from pymongo import MongoClient, DESCENDING
import pandas as pd
from datetime import timedelta
from database.abank import ABank
class Sim(ABank):
    def __init__(self,database_name):
        super().__init__(database_name)