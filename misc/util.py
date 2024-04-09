import streamlit as st
from misc.config import *
import ldap
from streamlit_extras.app_logo import add_logo
import pymongo

# Initialize logging
import logging
from misc.config import log_file

@st.cache_resource
def configure_logging(file_path, level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - MI-USER - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = configure_logging(log_file)

def logo():
    add_logo("misc/ufr.png", height=600)

def login():
    st.session_state.logged_in = True
    st.success("Login erfolgreich.")
    logger.info(f"User {st.session_state.user} hat sich eingeloggt.")

def logout():
    st.session_state.logged_in = False
    logger.info(f"User {st.session_state.user} hat sich ausgeloggt.")

# Sprache zwischen Deutsch und Englisch hin- und herwechseln
def change_lang():
    st.session_state.lang = ("de" if st.session_state.lang == "en" else "en")

def setup_session_state():
    # lang ist die Sprache (de, en)
    if "lang" not in st.session_state:
        st.session_state.lang = "de"
    # submitted wird benötigt, um nachzufragen ob etwas wirklich gelöscht werden soll
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    # expanded zeigt an, welches Element ausgeklappt sein soll
    if "expanded" not in st.session_state:
        st.session_state.expanded = ""
    # Name of the user
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

# Diese Funktion löschen, wenn die Verbindung sicher ist.
def authenticate2(username, password):
    return True if password == "0761" else False

# Die Authentifizierung gegen den Uni-LDAP-Server
def authenticate(username, password):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    user_dn = "uid={},{}".format(username, base_dn)
    try:
        l = ldap.initialize(server)
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(user_dn, password)
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as error:
        logger.warning(f"LDAP-Error: {error}")
        return False

def can_edit(username):
    u = user.find_one({"rz": username})
    admin_id = group.find_one({"name": app_name})["_id"]
    return (True if admin_id in u["groups"] else False)

# Das ist die mongodb; 
# QA-Paar ist ein Frage-Antwort-Paar aus dem FAQ.
# category enthält alle Kategorien von QA-Paaren. "invisible" muss es geben!
# qa enthält alle Frage-Antwort-Paare.
# user ist aus dem Cluster users und wird nur bei der Authentifizierung benötigt
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db = cluster["user"]
    user = mongo_db["user"]
    group = mongo_db["group"]
    logger.debug("Connected to MongoDB")
    logger.debug("Database contains collections: ")
    logger.debug(str(mongo_db.list_collection_names()))
except: 
    logger.error("Verbindung zur Datenbank nicht möglich!")
    st.write("**Verbindung zur Datenbank nicht möglich!**  \nKontaktieren Sie den Administrator.")
