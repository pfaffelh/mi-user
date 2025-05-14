import streamlit as st
import pymongo
from datetime import datetime
import time

# Seiten-Layout
st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

from misc.config import *
import misc.util as util

# make all neccesary variables available to session_state
util.setup_session_state()
# Navigation in Sidebar anzeigen
util.display_navigation()

def reset_and_confirm(text=None):
    st.session_state.submitted = False 
    st.session_state.expanded = ""
    if text is not None:
        st.success(text)

def delete_confirm_one(x):
    util.user.delete_one(x)
    reset_and_confirm()
    util.logger.info(f"User {st.session_state.username} hat User {x['rz']} gelöscht.")
    st.success("Erfolgreich gelöscht!")

def update_confirm(x, x_updated):
    util.user.update_one(x, {"$set": x_updated })
    reset_and_confirm()
    util.logger.info(f"User {st.session_state.username} hat User {x['rz']} geändert.")
    st.success("Erfolgreich geändert!")
 
date_format = '%d.%m.%Y um %H:%M:%S.'
bearbeitet = f"Zuletzt bearbeitet von {st.session_state.username} am {datetime.now().strftime(date_format)}"
 
# Ab hier wird die Webseite erzeugt
if st.session_state.logged_in:
    st.header("User der mi-Apps") 
    submit = False
    cols = st.columns([1,20])
    onlycolors = cols[1].toggle("Nur Personen mit Farben anzeigen", False)
    query = {"color" : {"$ne" : "#FFFFFF"}} if onlycolors else {}
    y = list(util.user.find(query, sort=[("name", pymongo.ASCENDING)]))
    group_ids = [g["_id"] for g in list(util.group.find(sort = [("name", pymongo.ASCENDING)]))]
    if cols[1].button('Neuen User hinzufügen'):
        onlycolors = False
        x = util.user.insert_one({"rz": "", "vorname": "", "name": "", "email": "", "color" : "#FFFFFF", "bearbeitet" : "", "groups": [], "kommentar": ""})
        st.session_state.expanded=x.inserted_id
        util.logging.info(f"User {st.session_state.username} hat einen neuen User hinzugefügt.")
        st.rerun()

    for x in y:
        cols = st.columns([1,20])
        with cols[0]:
            st.markdown(
                f"""
                <div style="background-color:{x['color']}; padding: 0px; border-radius: 0px;">
                    <h5 style="color:black;"></h5>
                </div>
                """,
                unsafe_allow_html=True
            )                        
        with cols[1]:
            with st.expander(f"{x['name']}, {x['vorname']}", expanded = (True if x["_id"] == st.session_state.expanded else False)):
                with st.form(f'ID-{x["_id"]}'):
                    st.write(x["bearbeitet"])
                    st.write("Gruppen")
                    cols = st.columns([1 for n in group_ids] + [1]) 
                    cols_dict = dict(zip(group_ids, cols))
                    for group_id in group_ids:
                        with cols_dict[group_id]:
                            st.checkbox(util.group.find_one({"_id": group_id})["name"], value = (True if group_id in x["groups"] else False), key=f'ID-{x["_id"]}{group_id}')
                    
                    name = st.text_input('Name', x["name"])
                    vorname = st.text_input('Vorname', x["vorname"])
                    co = st.columns([1,1])
                    rz = co[0].text_input('Benutzerkennung', x["rz"])
                    color = co[1].color_picker("Farbe auswählen", x["color"])
                    email = st.text_input('Email', x["email"])
                    kommentar = st.text_input('Kommentar', x["kommentar"])
                    x_updated = {"name": name, "vorname": vorname, "rz": rz, "color" : color, "email": email, "groups": [group_id for group_id in group_ids if st.session_state[f'ID-{x["_id"]}{group_id}'] == True], "kommentar": x['kommentar'], "bearbeitet": bearbeitet}
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
  st.switch_page("USERS.py")

st.sidebar.button("logout", on_click = util.logout)
