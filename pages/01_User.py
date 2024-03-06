import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
import pymongo
from misc.config import *
from misc.util import *

# make all neccesary variables available to session_state
setup_session_state()

def reset_and_confirm(text=None):
    st.session_state.submitted = False 
    st.session_state.expanded = ""
    if text is not None:
        st.success(text)

def delete_confirm_one(x):
    user.delete_one(x)
    reset_and_confirm()
    st.success("Erfolgreich gelöscht!")

def update_confirm(x, x_updated):
    user.update_one(x, {"$set": x_updated })
    st.success("Erfolgreich geändert!")
    #  reset_and_confirm()

# Seiten-Layout
st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"/>', unsafe_allow_html=True)
logo()

# Ab hier wird die Webseite erzeugt
if st.session_state.logged_in:
    st.header("User der mi-Apps")
 
    submit = False
    y = list(user.find(sort=[("name", pymongo.ASCENDING)]))
    group_names = [g["name"] for g in list(group.find(sort = [("name", pymongo.ASCENDING)]))]
    if st.button('Neuen User hinzufügen'):
        x = user.insert_one({"rz": "", "vorname": "", "name": "", "email": "", "groups": [], "kommentar": ""})
        st.session_state.expanded=x.inserted_id
        st.rerun()

    for x in y:
        with st.expander(f"{x['name']}, {x['vorname']}", expanded = (True if x["_id"] == st.session_state.expanded else False)):
            with st.form(f'ID-{x["_id"]}'):
                st.write("Gruppen")
                cols = st.columns([1 for n in group_names]) 
                cols_dict = dict(zip(group_names, cols))
                for group_name in group_names:
                    with cols_dict[group_name]: 
                        st.checkbox(group_name, value = (True if group_name in x["groups"] else False), key=f'ID-{x["_id"]}{group_name}')
                name = st.text_input('Name', x["name"])
                vorname = st.text_input('Vorname', x["vorname"])
                email = st.text_input('Email', x["email"])
                kommentar = st.text_input('Kommentar', x["kommentar"])
                x_updated = {"name": name, "vorname": vorname, "email": email, "groups": [group_name for group_name in group_names if st.session_state[f'ID-{x["_id"]}{group_name}'] == True], "kommentar": x['kommentar'] }
                col1, col2, col3 = st.columns([1,2,1]) 
                with col1: 
                    submit = st.form_submit_button('Speichern', on_click = update_confirm, args = (x, x_updated,))
                with col3: 
                    deleted = st.form_submit_button("Löschen")
                    if deleted:
                        st.session_state.submitted = True
                        st.session_state.expanded = x["_id"]
                if st.session_state.submitted:
                    col1, col2, col3 = st.columns([1,2,1]) 
                    with col1: 
                        st.form_submit_button(label = "Ja", on_click = delete_confirm_one, args = (x,))        
                    with col2: 
                        st.warning("Eintrag wirklich löschen?")
                    with col3: 
                        st.form_submit_button(label="Nein", on_click = reset_and_confirm, args=("Nicht gelöscht!",))

    if submit:
        st.rerun()

else:
  switch_page("FAQ")

st.sidebar.button("logout", on_click = logout)
