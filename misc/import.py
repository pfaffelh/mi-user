from pymongo import MongoClient

# This is the mongodb
cluster = MongoClient("mongodb://127.0.0.1:27017")
mongo_db = cluster["user"]
group = mongo_db["group"]
user = mongo_db["user"]

groups = [
     { "name": "admin",
       "kommentar": "darf alles"
      },
      { "name": "faq",
       "kommentar": "Darf FAQs bearbeiten"
      },
      { "name": "vvz",
       "kommentar": "Darf vvz bearbeiten"
      }]

users = [
    {"name": "Pfaffelhuber",
     "vorname": "Peter",
     "rz": "pp131",
     "email": "p.p@stochastik.uni-freiburg.de",
     "groups": ["admin", "faq", "vvz"],
     "kommentar": ""},
    {"name": "Junker",
     "vorname": "Markus",
     "rz": "junker",
     "email": "markus.junker@math.uni-freiburg.de",
     "groups": ["admin", "faq", "vvz"],
     "kommentar": ""},
    {"name": "Rabe",
     "vorname": "Ramona",
     "rz": "rr1067",
     "email": "ramona.rabe@math.uni-freiburg.de",
     "groups": ["faq", "vvz"],
     "kommentar": ""},
    {"name": "Fix",
     "vorname": "Daniel",
     "rz": "df1050",
     "email": "daniel.fix@math.uni-freiburg.de",
     "groups": ["admin", "faq", "vvz"],
     "kommentar": ""},
    {"name": "Christoforidis",
     "vorname": "Ioannis",
     "rz": "ie1011",
     "email": "ioannis.christoforidis@math.uni-freiburg.de",
     "groups": ["admin", "faq", "vvz"],
     "kommentar": ""},
    {"name": "Hofmann",
     "vorname": "Elias",
     "rz": "eh1070",
     "email": "elias.hofmann@math.uni-freiburg.",
     "groups": ["admin", "faq", "vvz"],
     "kommentar": ""},
    {"name": "Caffier",
     "vorname": "Anne",
     "rz": "ac1074",
     "email": "anne.caffier@math.uni-freiburg.de",
     "groups": ["faq", "vvz"],
     "kommentar": ""},
    {"name": "di Nunzio",
     "vorname": "Esther",
     "rz": "ed1034",
     "email": "esther.di.nunzio@math.uni-freiburg.de",
     "groups": ["faq", "vvz"],
     "kommentar": ""}]

print("Dieser Vorgang löscht alle Einträge in user und group!")
print("Wirklch fortfahren? [y/N]")
input = input()
if input == "y":
    group.delete_many({})
    user.delete_many({})
    for x in groups:
        group.insert_one(x)
    for x in users:
        user.insert_one(x)

print([user["email"] for user in list(user.find({}))])
