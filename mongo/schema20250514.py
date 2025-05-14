from pymongo import MongoClient

# This is the mongodb
cluster = MongoClient("mongodb://127.0.0.1:27017")
mongo_db = cluster["user"]

# collections sind:

# group
# user

# Here are the details

# category: Beschreibung einer Kategorie von Fragen
group_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Beschreibung einer Gruppe von Usern (z.B. vvz für alle, die die Apps bearbeiten dürfen).",
        "required": ["name", "kommentar"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Der Name der Gruppe"
            },
            "kommentar": {
                "bsonType": "string",
                "description": "Kommentar zur Gruppe"
            }
        }
    }
}

# user: Ein User
user_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Ein User.",
        "required": ["name", "vorname", "rz", "email", "groups", "color", "bearbeitet", "kommentar"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Der Nachname des Users."
            },
            "vorname": {
                "bsonType": "string",
                "description": "Der Vorname des Users."
            },
            "rz": {
                "bsonType": "string",
                "description": "Die Benutzerkennung des Users."
            },
            "email": {
                "bsonType": "string",
                "description": "Die Email-Adresse des Users."
            },
            "groups": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId",
                    "description": "Eine _id einer Gruppe."
                },
            },
            "kommentar": {
                "bsonType": "string",
                "description": "Ein Kommentar für einen User."
            },
            "color": {
                "bsonType": "string",
                "description": "Ein Hex Code für eine Farbe."
            },
            "bearbeitet": {
                "bsonType": "string",
                "description": "Gibt an, wann der User von wem zuletzt bearbeitet wurde."
            }
        }
    }
}

