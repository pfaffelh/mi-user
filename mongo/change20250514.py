from pymongo import MongoClient

cluster = MongoClient("mongodb://127.0.0.1:27017")
mongo_db = cluster["user"]

group = mongo_db["group"]
user = mongo_db["user"]
users = mongo_db["users"]
users.drop()

# Diesem Schema soll die Datenbank am Ende der Änderung folgen
import schema20250514
mongo_db.command('collMod','user', validator=schema20250514.user_validator, validationLevel='off')
mongo_db.command('collMod','group', validator=schema20250514.group_validator, validationLevel='off')

# Ab hier wird die Datenbank verändert
print("Ab hier wird verändert")

# This introduces colors

faq = group.find_one({"name" : "faq"})
user.insert_one({"rz" : "dekan", "vorname" : "", "name" : "Dekan:in", "kommentar" : "", "groups" : [faq["_id"]], "email" : ""})
user.insert_one({"rz" : "studiendekan", "vorname" : "", "name" : "Studiendekan:in", "kommentar" : "", "groups" : [faq["_id"]], "email" : ""})

user.update_many({}, {"$set": {"color": "#FFFFFF", "bearbeitet" : "Zuletzt bearbeitet von Peter Pfaffelhuber am 14.05.2025."}})

# Ab hier wird das Schema gecheckt
print("Check schema")
mongo_db.command("collMod", "user", validator = schema20250514.user_validator, validationLevel='moderate')

