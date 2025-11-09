import sqlite3
import hashlib
from datetime import datetime


DB_PATH = "auth.db"

# --- Fonction pour créer la base et la table users ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            is_admin INTEGER DEFAULT 0,
            is_validated INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


# --- Fonction pour hasher les mots de passe ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# --- Ajouter un utilisateur (ou admin) ---
def add_user(username, password, name="", is_admin=0, is_validated=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        c.execute(
            "INSERT INTO users (username, password, name, is_admin, is_validated) VALUES (?, ?, ?, ?, ?)",
            (username, hashed_pw, name, is_admin, is_validated)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"[WARN] L'utilisateur '{username}' existe déjà.")
    conn.close()


# --- Vérifier un utilisateur et son mot de passe ---
def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed_pw = hash_password(password)
    c.execute("SELECT id, is_admin, is_validated FROM users WHERE username=? AND password=?", (username, hashed_pw))
    user = c.fetchone()
    conn.close()
    if user:
        user_id, is_admin, is_validated = user
        return {"id": user_id, "is_admin": bool(is_admin), "is_validated": bool(is_validated)}
    return None


# --- Obtenir la liste de tous les utilisateurs ---
def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, name, is_admin, is_validated, created_at FROM users")
    users = c.fetchall()
    conn.close()
    return users


# --- Mettre à jour les droits ou la validation ---
def update_user_status(user_id, is_admin=None, is_validated=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if is_admin is not None:
        c.execute("UPDATE users SET is_admin=? WHERE id=?", (is_admin, user_id))
    if is_validated is not None:
        c.execute("UPDATE users SET is_validated=? WHERE id=?", (is_validated, user_id))
    conn.commit()
    conn.close()
