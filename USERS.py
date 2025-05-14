import streamlit as st
import pandas as pd
import time

# Seiten-Layout

from misc.config import *
import misc.util as util
import time
# make all neccesary variables available to session_state
util.setup_session_state()

# Ab hier wird die Seite angezeigt

from misc.config import *
import misc.util as util

# make all neccesary variables available to session_state
util.setup_session_state()

# Ab hier wird die Seite angezeigt

if st.session_state.logged_in:
    st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    st.header("USER")
    st.write("Wir listen alle User auf.")
    util.display_navigation()
    st.divider()

    # Zeige alle User als Dataframe an
    all_users = list(util.user.find({}))
    data = {
            "Vorname": [u["vorname"] for u in all_users],
            "Nachname": [u["name"] for u in all_users],
            "rz-Kennung": [u["rz"] for u in all_users],
            "color": [u["color"] for u in all_users],
        }
    for g in list(util.group.find().sort("name")):
        data[g["name"]] = [(True if (g["_id"] in u["groups"]) else False) for u in all_users]
    df = pd.DataFrame(data).sort_values(by=['Nachname'])

    st.dataframe(df, hide_index=True)
    st.sidebar.button("logout", on_click = util.logout)

else:
    st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

    st.header("USER Login")
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("#### Login")
        kennung = st.text_input("Benutzerkennung")
        password = st.text_input("Passwort", type="password")
        submit = st.form_submit_button("Login")
        st.session_state.username = kennung
        
    if submit:
        if util.authenticate(kennung, password): 
            st.session_state.username = kennung
            if util.can_edit(kennung):
                # If the form is submitted and the email and password are correct,
                # clear the form/container and display a success message
                placeholder.empty()
                st.session_state.logged_in = True
                st.success("Login successful")
                util.logger.info(f"User {st.session_state.user} hat in sich erfolgreich eingeloggt.")
                u = st.session_state.user.find_one({"rz": st.session_state.username})
                st.session_state.username = " ".join([u["vorname"], u["name"]])
                # make all neccesary variables available to session_state
                st.switch_page("pages/01_User.py")
            else:
                st.error("Nicht genügend Rechte, um USERS zu editieren.")
                util.logger.info(f"User {kennung} hatte nicht gebügend Rechte, um sich einzuloggen.")
                time.sleep(2)
                st.rerun()
        else: 
            st.error("Login nicht korrekt, oder RZ-Authentifizierung nicht möglich. (Z.B., falls nicht mit VPN verbunden.)")
            util.logger.info(f"Ein falscher Anmeldeversuch.")
            time.sleep(2)

