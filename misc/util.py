import streamlit as st
from misc.config import *
import ldap
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

def login():
    st.session_state.logged_in = True
    st.success("Login erfolgreich.")
    logger.info(f"User {st.session_state.username} hat sich eingeloggt.")

def logout():
    st.session_state.logged_in = False
    logger.info(f"User {st.session_state.username} hat sich ausgeloggt.")

def setup_session_state():
    # Das ist die mongodb; 
    # user ist aus dem Cluster user und wird nur bei der Authentifizierung benötigt
    try:
        cluster = pymongo.MongoClient(mongo_location)
        mongo_db = cluster["user"]
        st.session_state.user = mongo_db["user"]
        st.session_state.group = mongo_db["group"]
        logger.debug("Connected to MongoDB")
        logger.debug("Database contains collections: ")
        logger.debug(str(mongo_db.list_collection_names()))
    except: 
        logger.error("Verbindung zur Datenbank nicht möglich!")
        st.write("**Verbindung zur Datenbank nicht möglich!**  \nKontaktieren Sie den Administrator.")

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
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

def display_navigation():
    st.markdown("<style>.st-emotion-cache-16txtl3 { padding: 2rem 2rem; }</style>", unsafe_allow_html=True)
    with st.sidebar:
        st.image("static/ufr.png", use_container_width=True)
    st.sidebar.write("<hr style='height:1px;margin:0px;;border:none;color:#333;background-color:#333;' /> ", unsafe_allow_html=True)
    st.sidebar.page_link("USERS.py", label="Überblick")
    st.sidebar.write("<hr style='height:1px;margin:0px;;border:none;color:#333;background-color:#333;' /> ", unsafe_allow_html=True)
    st.sidebar.page_link("pages/01_User.py", label="User")
    st.sidebar.write("<hr style='height:1px;margin:0px;;border:none;color:#333;background-color:#333;' /> ", unsafe_allow_html=True)
    st.sidebar.page_link("pages/02_Gruppen.py", label="Gruppen")
    st.sidebar.write("<hr style='height:1px;margin:0px;;border:none;color:#333;background-color:#333;' /> ", unsafe_allow_html=True)

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

setup_session_state()

group = st.session_state.group
user = st.session_state.user
