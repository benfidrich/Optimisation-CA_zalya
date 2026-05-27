from pymongo import MongoClient

# CONNEXION

client = MongoClient("mongodb://localhost:27017/")

# DATABASE

db = client["crm_decisionnel"]