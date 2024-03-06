import streamlit as st
from misc.config import *
import ldap

from streamlit_extras.app_logo import add_logo

def logo():
    add_logo("misc/ufr.png", height=600)

def logout():
    st.session_state.logged_in = False

def change_lang():
    st.session_state.lang = ("de" if st.session_state.lang == "en" else "en")

def change_expand_all():
    st.session_state.expand_all = (False if st.session_state.expand_all == True else True)

def setup_session_state():
    # lang ist die Sprache (de, en)
    if "lang" not in st.session_state:
        st.session_state.lang = "de"
    # submitted wird benötigt, um nachzufragen ob etwas wirklich gelöscht werden soll
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    # st.session_state.expand_all bestimmt, ob all QA-Paare aufgeklappt dargestellt werden oder nicht
    if "expand_all" not in st.session_state:
        st.session_state.expand_all = False
    # expanded zeigt an, welches Element ausgeklappt sein soll
    if "expanded" not in st.session_state:
        st.session_state.expanded = ""
    # category gibt an, welche category angezeigt wird
    if "category" not in st.session_state:
        st.session_state.category = None
    # Name of the user
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = True

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
        print("Error:", error)
        return False

def can_edit(username):
    u = user.find_one({"rz": username})
    return (True if "faq" in list(u["groups"]) else False)