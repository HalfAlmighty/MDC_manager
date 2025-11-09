from auth_db import init_db, add_user

print("=== Initialisation du compte admin ===")
username = input("Nom d'utilisateur admin : ")
password = input("Mot de passe admin : ")
name = input("Nom complet (facultatif) : ")

init_db()
add_user(username, password, name, is_admin=1, is_validated=1)
print(f"✅ Compte admin '{username}' créé avec succès !")
