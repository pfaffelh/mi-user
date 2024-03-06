import streamlit as st
from pymongo import ASCENDING
from misc.config import *
from misc.util import *
import pandas as pd

# make all neccesary variables available to session_state
setup_session_state()

# Seiten-Layout
st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
logo()

# Ab hier wird die Seite angezeigt
st.header("USERS")

if st.session_state.logged_in:
    st.write("Wir listen alle User auf.")
    st.divider()

    # Zeige alle User als Dataframe an
    all_users = list(user.find({}))
#    st.write([u["email"] for u in all_users])
#    st.write([u["vorname"] for u in all_users])
    data = {
            "Vorname": [u["vorname"] for u in all_users],
            "Nachname": [u["name"] for u in all_users],
            "rz-Kennung": [u["rz"] for u in all_users],
            "email": [u["email"] for u in all_users],
        }
 #   st.write(data)
    for g in list(group.find().sort("name")):
        data[g["name"]] = [(True if (g["name"] in u["groups"]) else False) for u in all_users]
    df = pd.DataFrame(data).sort_values(by=['Nachname'])

    st.dataframe(df, hide_index=True)

else:
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("#### Benutzerkennung")
        kennung = st.text_input("Benutzerkennung")
        password = st.text_input("Passwort", type="password")
        submit = st.form_submit_button("Login")
        st.session_state.user = kennung
        
    if submit and authenticate(kennung, password) and can_edit(st.session_state.user):
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        st.session_state.logged_in = True
        st.success("Login successful")
        st.rerun()
    elif submit:
        st.error("Login failed")
        st.rerun()
    else:
        pass

st.sidebar.button("logout", on_click = logout)
