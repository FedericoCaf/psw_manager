import re

def is_valid_email(email):
    # Utilizza un'espressione regolare per verificare il formato dell'email
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

def is_valid_username(username):
    # Verifica che lo username sia composto solo da lettere, numeri e trattini bassi
    return username.isalnum() or "_" in username

def is_valid_password(password):
    # Aggiungi qui ulteriori regole di validazione per la password
    return len(password) >= 8  # Ad esempio, almeno 8 caratteri