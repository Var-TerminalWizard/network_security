import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
MONGO_URL = os.getenv("MONGO_DB_URL")
print(f"MongoDB URL: {MONGO_URL}")

ca = certifi.where()

# Custom Imports
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtractor():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def csv_to_json(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            
            # FIX 1: Convert directly to a list of dicts instead of character strings
            json_data = df.to_dict(orient='records')
            return json_data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def push_data_to_mongodb(self, json_data, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.json_data = json_data
            
            self.client = pymongo.MongoClient(MONGO_URL, tlsCAFile=ca)
            self.database = self.client[self.database]
            self.collection = self.database[self.collection]
            
            self.collection.insert_many(self.json_data)
            return len(self.json_data)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    try:
        FILE_PATH = os.path.join("Network_Data", "phisingData.csv") # Safer cross-platform pathing
        DATABASE = "NetworkSecurity"
        Collection = "NetworkData"
        
        net_obj = NetworkDataExtractor()
        json_data = net_obj.csv_to_json(FILE_PATH)
        
        no_of_records = net_obj.push_data_to_mongodb(json_data, DATABASE, Collection)
        print(f"Number of records inserted: {no_of_records}")
        
    except Exception as e:
        # FIX 2: Used 'logging' matching your import name
        logging.error(f"An error occurred: {e}")