import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
import time
import pymongo
from misc.config import *
from misc.util import *

# make all neccesary variables available to session_state
setup_session_state()

# Seiten-Layout
st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
logo()

# Ab hier wird die Webseite erzeugt
if st.session_state.logged_in:

  st.header("Gruppen")
  st.write("Hier können Gruppen bearbeitet, hinzugefügt und gelöscht werden.")

  # Alles auf Anfang
  def reset_and_confirm(text=None):
    st.session_state.submitted = False 
    st.session_state.expanded = ""
    if text is not None:
      st.success(text)

  def delete_confirm_one(g):
    # delete g["name"] from all user["groups"]
    user.update_many({}, {"$pull": {"groups": g["name"]}})
    # delete g itself
    group.delete_one(g)
    reset_and_confirm()
    logger.info(f"User {st.session_state.user} hat Gruppe {g['name']} gelöscht.")
    st.success(f"Erfolgreich gelöscht! Gruppe {g['name']} bei allen Usern gelöscht.")

  def update_confirm(x, x_updated):
    group.update_one(x, {"$set": x_updated })
    logger.info(f"User {st.session_state.user} hat Gruppe {x['name']} geändert.")
    reset_and_confirm()
    st.success("Erfolgreich geändert!")

  if st.button('Neue Gruppe hinzufügen'):
    x = group.insert_one({"name": "", "kommentar": "Das ist die neue Gruppe"})
    st.session_state.expanded=x.inserted_id
    logger.info(f"User {st.session_state.user} hat eine neue Gruppe angelegt.")
    st.rerun()

  y = list(group.find(sort = [("name", pymongo.ASCENDING)]))

  for x in y:
      with st.expander(x['name'], expanded = (True if x["_id"] == st.session_state.expanded else False)):
          with st.form(f'ID-{x["_id"]}'):
              name=st.text_input('Name', x["name"])
              kommentar=st.text_input('Kommentar', x["kommentar"])
              x_updated = {"name": name, "kommentar": kommentar}
              col1, col2, col3 = st.columns([1,7,1]) 
              with col1: 
                  submit = st.form_submit_button('Speichern', type="primary")
              if submit:
                  update_confirm(x, x_updated)
                  time.sleep(2)
                  st.rerun()      
              with col3: 
                  deleted = st.form_submit_button("Löschen")
              if deleted:
                  st.session_state.submitted = True
                  st.session_state.expanded = x["_id"]
              if st.session_state.submitted and st.session_state.expanded == x["_id"]:
                  with col1: 
                      st.form_submit_button(label = "Ja", type="primary", on_click = delete_confirm_one, args = (x,))        
                  with col2: 
                      st.warning("Eintrag wirklich löschen?")
                  with col3: 
                      st.form_submit_button(label="Nein", on_click = reset_and_confirm, args=("Nicht gelöscht!",))

#  if submit:
#    st.rerun()

else: 
  switch_page("USERS")

st.sidebar.button("logout", on_click = logout)
