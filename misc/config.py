import pymongo

# This is the ldap-server of the University, which is required for authentication
server="ldaps://ldap.uni-freiburg.de"
base_dn = "ou=people,dc=uni-freiburg,dc=de"

import logging
logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - schema - %(message)s")

# Das ist die mongodb; 
# Das Cluster users enthält User-Daten.
# group enthält alle möglichen Gruppen für die verschiedenen Apps.
# user enthält alle Nutzer.
cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
mongo_db_users = cluster["user"]
user = mongo_db_users["user"]
group = mongo_db_users["group"]

logging.info("Connected to MongoDB")
logging.info("Database contains collections: ")
logging.info(str(mongo_db_users.list_collection_names()))
