from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, send
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['chat_app']
messages_collection = db['messages']

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('chat'))
    return render_template('login.html')

# Chat route
@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Fetch previous messages from MongoDB
    messages = list(messages_collection.find({}, {'_id': 0}))
    return render_template('chat.html', username=session['username'], messages=messages)

# WebSocket event for messages
@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    # Save message to MongoDB
    message_data = {
        'username': msg['username'],
        'message': msg['message'],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    messages_collection.insert_one(message_data)
    # Broadcast the message to all clients
    send(message_data, broadcast=True)

# WebSocket event for clearing chat
@socketio.on('clear_chat')
def handle_clear_chat():
    print("Clearing chat history")
    messages_collection.delete_many({})  # Delete all messages from MongoDB
    send({'username': 'System', 'message': 'Chat history cleared'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)