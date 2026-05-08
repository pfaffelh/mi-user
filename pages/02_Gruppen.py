import streamlit as st
import pymongo

# Seiten-Layout
st.set_page_config(page_title="User-Verwaltung der mi-Apps", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

from misc.config import *
import misc.util as util

# make all neccesary variables available to session_state
util.setup_session_state()
# Navigation in Sidebar anzeigen
util.display_navigation()

# Ab hier wird die Webseite erzeugt
if st.session_state.logged_in:

  st.header("Gruppen")
  st.write("Hier können Gruppen bearbeitet, hinzugefügt und gelöscht werden.")

  # Alles auf Anfang
  def reset_and_confirm(text=None):
    st.session_state.submitted = False
    st.session_state.expanded = ""
    if text is not None:
      util.flash(text)

  def delete_confirm_one(g):
    # delete g["name"] from all user["groups"]
    util.user.update_many({}, {"$pull": {"groups": g["name"]}})
    # delete g itself
    util.group.delete_one(g)
    util.list_groups.clear()
    reset_and_confirm()
    util.logger.info(f"User {st.session_state.username} hat Gruppe {g['name']} gelöscht.")
    util.flash(f"Erfolgreich gelöscht! Gruppe {g['name']} bei allen Usern gelöscht.")

  def update_confirm(x, x_updated):
    util.group.update_one(x, {"$set": x_updated })
    util.list_groups.clear()
    util.logger.info(f"User {st.session_state.username} hat Gruppe {x['name']} geändert.")
    reset_and_confirm()
    util.flash("Erfolgreich geändert!")

  if st.button('Neue Gruppe hinzufügen'):
    x = util.group.insert_one({"name": "", "kommentar": "Das ist die neue Gruppe"})
    util.list_groups.clear()
    st.session_state.expanded=x.inserted_id
    util.logger.info(f"User {st.session_state.username} hat eine neue Gruppe angelegt.")
    st.rerun()

  y = util.list_groups()

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

else:
  st.switch_page("USERS.py")

st.sidebar.button("logout", on_click = util.logout)
