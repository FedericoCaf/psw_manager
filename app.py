import os
import uuid
import datetime
from functools import wraps
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from cryptography.fernet import Fernet
import jwt
import bcrypt
from db_connection import connect_db
from validation_utils import is_valid_email, is_valid_username, is_valid_password

app = Flask(__name__)
CORS(app)

file_path = os.path.join(app.root_path, '.env')
if not os.path.exists(file_path):
    open(file_path, 'w').close()

app.secret_key = os.environ.get('SECRET_KEY')
crypto_key = os.environ.get('CRYPTO_KEY')

if app.secret_key is None:
    app.secret_key = uuid.uuid4().hex
    with open('.env', 'a') as env_file:
        env_file.write(f'export SECRET_KEY="{app.secret_key}"\n')

if crypto_key is None:
    crypto_key = Fernet.generate_key().decode()
    with open('.env', 'a') as env_file:
        env_file.write(f'export CRYPTO_KEY="{crypto_key}"\n')

db = 'psw_manager_db.db'
cipher_suite = Fernet(crypto_key)

#home
@app.route("/")
def index():
    # users = connect_db(db).execute('SELECT * FROM users').fetchall()
    # connect_db(db).close
    return jsonify({'message': 'Home page'})

#registrazione utente
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
     
        data = request.get_json()
        print(data['username'])
        username_body = data['username']
        email_body = data['email']
        password_body = data['password']
        
        if not is_valid_email(email_body):
            return jsonify({'message': 'Invalid email format'}), 400

        if not is_valid_username(username_body):
            return jsonify({'message': 'Invalid username format, (letters, numbers and underscore accepted)'}), 400

        if not is_valid_password(password_body):
            return jsonify({'message': 'Invalid password format (minimum 8 characters)'}), 400

        hashed_password = bcrypt.hashpw(password_body.encode('utf-8'), bcrypt.gensalt())

        user_by_email = connect_db(db).execute(f"SELECT * FROM users WHERE email = '{email_body}'").fetchone()
        if user_by_email:
            return jsonify({'message': 'Email address already registered'}), 400
        user_by_username = connect_db(db).execute(f"SELECT * FROM users WHERE username = '{username_body}'").fetchone()
        if user_by_username or user_by_email:
            return jsonify({'message': 'Username already taken'}), 400
        conn = connect_db(db)
        cursor = conn.cursor()
        current_datetime = datetime.datetime.now()
        cursor.execute("INSERT INTO users (username, email, password, data_iscrizione) VALUES (?, ?, ?, ?)", (username_body, email_body, hashed_password, current_datetime))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    if request.method == 'GET':
        return jsonify({'message': 'Eventuali dati per pagina di registrazione'})

#check token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

#login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return jsonify({'message': 'Username and password are required'}), 400
        
        user_body = data['username']
        user_db_row = connect_db(db).execute(f"SELECT * FROM users WHERE username = '{user_body}'").fetchone()
        
        password_body = data['password']

        if user_db_row and bcrypt.checkpw(password_body.encode('utf-8'), user_db_row['password']):
            user_db = dict(user_db_row)  # Converti la riga in un dizionario
            del user_db['password']  # Rimuovi la password dal dizionario dell'utente
            token = jwt.encode({
                'user': user_db,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, app.secret_key, algorithm='HS256')

            session['token'] = token

            return jsonify({'token': token})
        return jsonify({'message': 'Invalid credentials'}), 401
    if request.method == 'GET':
        return jsonify({'message': 'Eventuali dati per pagina di login'})

#aggiungi password contesto
@app.route('/add-password', methods=['POST'])
@token_required
def add_password():
   
    data = request.get_json()
    if not data['context'] or not data['username'] or not data['password']:
        return jsonify({'message': 'Mandatory data missing'}), 400

    token = session.get('token')

    if token:
        try:
            payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
            user_info = payload['user']     
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
    context_body = data['context']
    username_body = data['username']
    password_body = data['password']
    encrypted_password = cipher_suite.encrypt(password_body.encode())

    conn = connect_db(db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (user_id, context, username, password) VALUES (?, ?, ?, ?)", (user_info['id'], context_body, username_body, encrypted_password))
    conn.commit()
    return jsonify({'message': 'Password added correctly.'})

#ottieni tutte le password dell'utente corrente
@app.route('/all-contexts', methods=['GET'])
@token_required
def get_all_contexts():
   
    token = session.get('token')

    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        user_info = payload['user']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token is invalid!'}), 401
    
    conn = connect_db(db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM passwords WHERE user_id = '{user_info['id']}'")
    rows = cursor.fetchall()
    if len(rows):
        passwords_list = []
        for row in rows:
            password_obj = {
                'id': row[0],
                'user_id': row[1],
                'context': row[2],
                'username': row[3],
               #'password': row[4],
             }
            passwords_list.append(password_obj)
            return passwords_list
    return jsonify({'message': 'Nessun contesto salvato per l\'utente corrente'}), 400

#ottieni la password tramite id (richiede esplicitamente la password di autenticazione)
@app.route('/password/<int:id>', methods=['POST'])
@token_required
def get_password(id):

    data = request.get_json()
    if not data['password']:
        return jsonify({'message': 'Authentication password required'}), 400

    token = session.get('token')
    password_body = data['password']
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        user_info = payload['user']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token is invalid!'}), 401
    
    user_db_row = connect_db(db).execute(f"SELECT * FROM users WHERE username = '{user_info['username']}'").fetchone()
    
    if user_db_row:
        if bcrypt.checkpw(password_body.encode('utf-8'), user_db_row['password']):
            conn = connect_db(db)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM passwords WHERE id = ? and user_id = ?', (id, user_info['id']))
            row = cursor.fetchone()
            if row:
                decrypted_password = cipher_suite.decrypt(row[4]).decode()
                password_obj = {
                    'password': decrypted_password,
                    }
                conn.close()
                return password_obj
            return jsonify({'message': 'Password not found for current user'}), 400
        return jsonify({'message': 'Wrong password'}), 400
    return jsonify({'message': 'User not found!'}), 400


#ottieni il singolo contesto e visualizza la password per l'edit (richiede esplicitamente la password di autenticazione)
@app.route('/context/<int:id>', methods=['POST'])
@token_required
def get_context(id):

    data = request.get_json()
    if not data['password']:
        return jsonify({'message': 'Authentication password required'}), 400

    token = session.get('token')
    password_body = data['password']
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        user_info = payload['user']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token is invalid!'}), 401
    
    user_db_row = connect_db(db).execute(f"SELECT * FROM users WHERE username = '{user_info['username']}'").fetchone()
    
    if user_db_row:
        if bcrypt.checkpw(password_body.encode('utf-8'), user_db_row['password']):
            conn = connect_db(db)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM passwords WHERE id = ? and user_id = ?', (id, user_info['id']))
            row = cursor.fetchone()
            if row:
                decrypted_password = cipher_suite.decrypt(row[4]).decode()
                context_obj = {
                    'id': row[0],
                    'user_id': row[1],
                    'context': row[2],
                    'username': row[3],
                    'password': decrypted_password
                    }
                conn.close()
                return context_obj
            return jsonify({'message': 'Context not found for current user'}), 400
        return jsonify({'message': 'Wrong password'}), 400
    return jsonify({'message': 'User not found!'}), 400

#modifica il contesto
@app.route('/edit-context/<int:id>', methods=['PUT'])
@token_required
def edit_context(id):

    data = request.get_json()
    if not data['context'] or not data['username'] or not data['password']:
        return jsonify({'message': 'Mandatory data missing'}), 400
            
    context_body = data['context']
    username_body = data['username']
    password_body = data['password']
    encrypted_password = cipher_suite.encrypt(password_body.encode())

    conn = connect_db(db)
    cursor = conn.cursor()
    query = "UPDATE passwords SET context = ?, username = ?, password = ? WHERE id = ?"
    data = (context_body, username_body, encrypted_password, id, )
    
    cursor.execute(query, data)
    conn.commit()
    return jsonify({'message': 'Context updated correctly.'})


#logout
@app.route('/logout', methods=['GET'])
@token_required
def logout():
    session.pop('token', None)
    return jsonify({'message': 'Logged out successfully'})


if __name__ == '__main__':
    app.run(debug=True)
