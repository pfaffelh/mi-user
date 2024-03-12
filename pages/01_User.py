import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
import pymongo
import time
from misc.config import *
from misc.util import *

# make all neccesary variables available to session_state
setup_session_state()

# Seiten-Layout
st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
logo()

def reset_and_confirm(text=None):
    st.session_state.submitted = False 
    st.session_state.expanded = ""
    if text is not None:
        st.success(text)

def delete_confirm_one(x):
    user.delete_one(x)
    reset_and_confirm()
    logger.info(f"User {st.session_state.user} hat User {x['rz']} gelöscht.")
    st.success("Erfolgreich gelöscht!")

def update_confirm(x, x_updated):
    user.update_one(x, {"$set": x_updated })
    reset_and_confirm()
    logger.info(f"User {st.session_state.user} hat User {x['rz']} geändert.")
    st.success("Erfolgreich geändert!")
 
# Ab hier wird die Webseite erzeugt
if st.session_state.logged_in:
    st.header("User der mi-Apps")
 
    submit = False
    y = list(user.find(sort=[("name", pymongo.ASCENDING)]))
    group_ids = [g["_id"] for g in list(group.find(sort = [("name", pymongo.ASCENDING)]))]
    if st.button('Neuen User hinzufügen'):
        x = user.insert_one({"rz": "", "vorname": "", "name": "", "email": "", "groups": [], "kommentar": ""})
        st.session_state.expanded=x.inserted_id
        logging.info(f"User {st.session_state.user} hat einen neuen User hinzugefügt.")
        st.rerun()

    st.write(st.session_state.expanded)
    for x in y:
        with st.expander(f"{x['name']}, {x['vorname']}", expanded = (True if x["_id"] == st.session_state.expanded else False)):
            with st.form(f'ID-{x["_id"]}'):
                st.write("Gruppen")
                cols = st.columns([1 for n in group_ids]) 
                cols_dict = dict(zip(group_ids, cols))
                for group_id in group_ids:
                    with cols_dict[group_id]: 
                        st.checkbox(group.find_one({"_id": group_id})["name"], value = (True if group_id in x["groups"] else False), key=f'ID-{x["_id"]}{group_id}')
                name = st.text_input('Name', x["name"])
                vorname = st.text_input('Vorname', x["vorname"])
                rz = st.text_input('Benutzerkennung', x["rz"])
                email = st.text_input('Email', x["email"])
                kommentar = st.text_input('Kommentar', x["kommentar"])
                x_updated = {"name": name, "vorname": vorname, "rz": rz, "email": email, "groups": [group_id for group_id in group_ids if st.session_state[f'ID-{x["_id"]}{group_id}'] == True], "kommentar": x['kommentar'] }
                col1, col2, col3 = st.columns([1,7,1]) 
                with col1: 
                    submit = st.form_submit_button('Speichern', type="primary", args = (x, x_updated,))
                if submit:
                    update_confirm(x, x_updated, )
                    time.sleep(2)
                    st.rerun()      
                with col3: 
                    deleted = st.form_submit_button("Löschen")
                if deleted:
                    st.session_state.submitted = True
                    st.session_state.expanded = x["_id"]
                    st.rerun()
                if st.session_state.submitted and st.session_state.expanded == x["_id"]:
                    with col1: 
                        st.form_submit_button(label = "Ja", type="primary", on_click = delete_confirm_one, args = (x,))        
                    with col2: 
                        st.warning("Eintrag wirklich löschen?")
                    with col3: 
                        st.form_submit_button(label="Nein", on_click = reset_and_confirm, args=("Nicht gelöscht!",))


#    if submit:
#        st.rerun()

else:
  switch_page("USERS")

st.sidebar.button("logout", on_click = logout)
