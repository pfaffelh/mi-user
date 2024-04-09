import streamlit as st
from pymongo import ASCENDING
import time
import pandas as pd

# Seiten-Layout
st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

from misc.config import *
import misc.util as util
util.logo()


# make all neccesary variables available to session_state
util.setup_session_state()

# Ab hier wird die Seite angezeigt
st.header("USERS")

if st.session_state.logged_in:
    st.write("Wir listen alle User auf.")
    st.divider()

    # Zeige alle User als Dataframe an
    all_users = list(util.user.find({}))
    data = {
            "Vorname": [u["vorname"] for u in all_users],
            "Nachname": [u["name"] for u in all_users],
            "rz-Kennung": [u["rz"] for u in all_users],
            "email": [u["email"] for u in all_users],
        }
    for g in list(util.group.find().sort("name")):
        data[g["name"]] = [(True if (g["_id"] in u["groups"]) else False) for u in all_users]
    df = pd.DataFrame(data).sort_values(by=['Nachname'])

    st.dataframe(df, hide_index=True)

else:
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("#### Login")
        kennung = st.text_input("Benutzerkennung")
        password = st.text_input("Passwort", type="password")
        submit = st.form_submit_button("Login")
        st.session_state.user = kennung
        
    if submit:
        if util.authenticate(kennung, password): 
            if util.can_edit(kennung):
                # If the form is submitted and the email and password are correct,
                # clear the form/container and display a success message
                st.session_state.logged_in = True
                st.success("Login erfolgreich")
                util.logger.info(f"User {st.session_state.user} hat in sich erfolgreich eingeloggt.")
                # make all neccesary variables available to session_state
                util.setup_session_state()
                time.sleep(2)
                st.rerun()
            else:
                st.error("Nicht genügend Rechte, um VVZ zu editieren.")
                util.logger.info(f"User {kennung} hatte nicht gebügend Rechte, um sich einzuloggen.")
                time.sleep(2)
                st.rerun()
        else: 
            st.error("Login nicht korrekt, oder RZ-Authentifizierung nicht möglich. (Z.B., falls nicht mit VPN verbunden.)")
            util.logger.info(f"Ein falscher Anmeldeversuch.")
            time.sleep(2)
            st.rerun()

st.sidebar.button("logout", on_click = util.logout)
