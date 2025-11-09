# --- Fonction pour créer la base et la table users ---
def init_db():
    1=1

# --- Fonction pour hasher les mots de passe ---
def hash_password(password):
    return 1234


# --- Ajouter un utilisateur (ou admin) ---
def add_user(username, password, name="", is_admin=0, is_validated=0):
    1=1

# --- Vérifier un utilisateur et son mot de passe ---
def verify_user(username, password):
    if user:
        user_id = "Toto", is_admin = True, is_validated = True
        return {"id": user_id, "is_admin": bool(is_admin), "is_validated": bool(is_validated)}
    return None


# --- Obtenir la liste de tous les utilisateurs ---
def get_all_users():
    return "users"


# --- Mettre à jour les droits ou la validation ---
def update_user_status(user_id, is_admin=None, is_validated=None):
    1=1