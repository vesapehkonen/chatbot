from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from tinydb import TinyDB, Query
import bcrypt
from datetime import datetime
from bot.model_loader import load_model, build_prompt, generate_response, summarize_history

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production

load_model()
db = TinyDB('chat_memory.json')
users_table = db.table('users')
messages_table = db.table('messages')

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users_table.get(Query().username == username):
            return "Username already exists."
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        users_table.insert({'username': username, 'password_hash': hash_pw})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_table.get(Query().username == username)
        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def get_recent_history(user, limit=5):
    msgs = messages_table.search((Query().user == user) & (Query().role.one_of(['user', 'bot'])))
    return sorted(msgs, key=lambda m: m['timestamp'])[-limit:]

@app.route('/chat', methods=['POST'])
def chat():
    if 'username' not in session:
        return {'reply': 'Please log in first.'}
    
    data = request.get_json()
    new_user_message = data.get('message')
    user = session['username']

    history = get_recent_history(user)

    messages_table.insert({
        'user': user,
        'role': 'user',
        'message': new_user_message,
        'timestamp': datetime.now().isoformat()
    })

    short_history = summarize_history(history, keep_last_n=1)
    prompt = build_prompt(short_history, new_user_message)

    reply = generate_response(prompt)
    
    messages_table.insert({
        'user': user,
        'role': 'bot',
        'message': reply,
        'timestamp': datetime.now().isoformat()
    })

    return jsonify({'reply': reply})
    
if __name__ == '__main__':
    app.run(debug=True)
