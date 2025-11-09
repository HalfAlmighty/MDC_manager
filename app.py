import streamlit as st
from auth_db import init_db, add_user, verify_user, get_all_users, update_user_status

# --- Initialisation de la base ---
init_db()

# --- Configuration de la page ---
st.set_page_config(page_title="Connexion / Inscription", layout="centered")

# --- Initialisation session ---
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None


# --- Page de connexion ---
def login_page():
    st.title("🔐 Connexion")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        user = verify_user(username, password)
        if user:
            if not user["is_validated"]:
                st.warning("🕓 Votre compte est en attente de validation par un administrateur.")
            else:
                st.session_state.user = username
                if user["is_admin"]:
                    st.session_state.page = "admin"
                else:
                    st.session_state.page = "user"
                st.rerun()

        else:
            st.error("❌ Identifiants incorrects.")

    if st.button("Créer un compte"):
        st.session_state.page = "register"
        st.rerun()



# --- Page d'inscription ---
def register_page():
    st.title("📝 Créer un compte")

    name = st.text_input("Nom complet")
    username = st.text_input("Nom d'utilisateur souhaité")
    password = st.text_input("Mot de passe", type="password")

    if st.button("S'inscrire"):
        add_user(username, password, name, is_admin=0, is_validated=0)
        st.success("✅ Compte créé ! En attente de validation par un administrateur.")
        st.session_state.page = "login"
        st.rerun()


    if st.button("Retour à la connexion"):
        st.session_state.page = "login"
        st.rerun()



# --- Page admin ---
def admin_page():
    st.title("👑 Espace Administrateur")
    st.write(f"Connecté en tant que : {st.session_state.user}")

    users = get_all_users()
    for u in users:
        uid, uname, name, is_admin, is_validated, created = u
        st.markdown(f"**{uname}** ({name}) — Admin: {bool(is_admin)} — Validé: {bool(is_validated)} — Créé le {created}")

        col1, col2 = st.columns(2)
        if col1.button(f"Valider {uname}", key=f"val_{uid}"):
            update_user_status(uid, is_validated=1)
            st.rerun()
        if col2.button(f"Donner droits admin à {uname}", key=f"adm_{uid}"):
            update_user_status(uid, is_admin=1)
            st.rerun()

    if st.button("Se déconnecter"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()


# --- Page utilisateur ---
def user_page():
    st.title("👤 Espace Utilisateur")
    st.write(f"Bienvenue {st.session_state.user} !")
    if st.button("Se déconnecter"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()



# --- ROUTEUR ---
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "admin":
    admin_page()
elif st.session_state.page == "user":
    user_page()
