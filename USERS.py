import streamlit as st
from pymongo import ASCENDING
from misc.config import *
from misc.util import *

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

    col1, col2 = st.columns([1,1]) 
    # Der Sprach-Umschalter
    with col1:
        st.button("en" if st.session_state.lang == "de" else "de", on_click = change_lang)
    # Der Ausklapp-Umschalter
    with col2:
        st.button("Alles einklappen" if st.session_state.expand_all == True else "Alles ausklappen", on_click = change_expand_all)

    # Alle Kategorien. (ASCENDING sortiert sie nach ihrer Anzeige-Reihenfolge.)
    cats = list(category.find(sort=[("rang", pymongo.ASCENDING)]))

    # Nun werden für alle Kategorien all Frage-Antwort-Paare angezeigt
    for cat in cats:
        st.divider()
        st.write(cat["name_de"] if st.session_state.lang == "de" else cat["name_en"])
        y = qa.find({"category": cat["kurzname"]}, sort=[("rang", pymongo.ASCENDING)])
        for x in y:
            with st.expander(x["q_de"] if st.session_state.lang == "de" else x["q_en"], expanded = st.session_state.expand_all):
                stu1 = "Studiengänge" if st.session_state == "de" else "Study programs"
                stu2 = "alle" if st.session_state == "de" else "all"
                stu2 = (stu2 if x['studiengang'] == [] else (', '.join(x['studiengang'])))
                st.write(f"{stu1}: {stu2}")
                st.write("Antwort" if st.session_state == "de" else "Answer")
                st.write(x["a_de"] if st.session_state.lang == "de" else x["a_en"])
                if x["kommentar"] != "":
                    st.write("Kommentar:")
                    st.write(x["kommentar"])

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
