from flask import Flask, render_template, request, redirect, session, url_for, flash
from blockchain import Blockchain
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# CHANGE THIS TO A LONG, RANDOM STRING FOR PRODUCTION!
# You can generate one with `os.urandom(24).hex()`
app.secret_key = 'your_super_secret_key_here'

# --- Persistence File Paths ---
USERS_FILE = 'users.json'
BLOCKCHAIN_FILE = 'blockchain_data.json'

# --- Functions to Load/Save User Data ---
def load_users():
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {USERS_FILE} is empty or malformed. Starting with default users.")
            # Fallback to default users if file is corrupted
            return {
                "admin": {"password": generate_password_hash("admin123"), "role": "admin"},
                "voter1": {"password": generate_password_hash("voter123"), "role": "voter"},
                "voter2": {"password": generate_password_hash("voter123"), "role": "voter"}
            }
    # Default users if file doesn't exist or is initially empty
    return {
        "admin": {"password": generate_password_hash("admin123"), "role": "admin"},
        "voter1": {"password": generate_password_hash("voter123"), "role": "voter"},
        "voter2": {"password": generate_password_hash("voter123"), "role": "voter"}
    }

def save_users(user_data):
    with open(USERS_FILE, 'w') as f:
        json.dump(user_data, f, indent=4)

# Load users when the app starts
users = load_users()

# --- Blockchain Initialization ---
# The Blockchain class's __init__ method should handle loading from BLOCKCHAIN_FILE
blockchain = Blockchain()

# Hardcoded candidates (could be made persistent if needed)
candidates = ["M. S. Dhoni", "Virat Kohli", "Rohit Sharma", "Sachin Tendulkar"]

# In-memory set to prevent double voting per session (resets on server restart)
# For truly persistent double-voting check, you'd iterate the blockchain on login.
voted_users = set()

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users.get(username)

        if user_data and check_password_hash(user_data['password'], password):
            session['user'] = username
            session['role'] = user_data['role']
            flash(f"Welcome, {username}!", 'success')
            return redirect(url_for('admin_dashboard') if user_data['role'] == 'admin' else url_for('vote'))
        else:
            flash("Invalid Credentials. Please try again.", 'danger')
        return redirect(url_for('login')) # Redirect back to login on failure
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash("Username already exists. Please choose a different one.", 'warning')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        users[username] = {"password": hashed_password, "role": "voter"}
        save_users(users) # Save updated users to file
        flash("Registration successful! Please log in.", 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user' not in session or session['role'] != 'voter':
        flash("Please log in as a voter to cast your vote.", 'info')
        return redirect(url_for('login'))

    if session['user'] in voted_users:
        flash("You have already voted!", 'warning')
        return redirect(url_for('results'))

    if request.method == 'POST':
        candidate = request.form['candidate']
        if candidate not in candidates:
            flash("Invalid candidate selected.", 'danger')
            return redirect(url_for('vote'))

        # Create a new block with this vote transaction
        # In a real system, you might collect multiple transactions before mining a block
        blockchain.new_block(proof=100, voter_id=session['user'], candidate=candidate)
        blockchain.save_chain() # Persist the updated blockchain to file
        voted_users.add(session['user']) # Mark user as voted in this session

        flash("Your vote has been cast successfully!", 'success')
        return redirect(url_for('results'))

    return render_template("vote.html", candidates=candidates)

# New API endpoint for fetching results via AJAX
@app.route('/api/results')
def api_results():
    # Basic authorization check for the API endpoint
    if 'user' not in session:
        return {'error': 'Unauthorized'}, 401
    vote_count = blockchain.get_votes()
    return vote_count # Flask automatically converts dictionary to JSON response

@app.route('/results')
def results():
    if 'user' not in session:
        flash("Please log in to view results.", 'info')
        return redirect(url_for('login'))
    # The actual vote data is fetched via AJAX in results.html, so no data passed here
    return render_template("results.html")

@app.route('/admin')
def admin_dashboard():
    if 'user' not in session or session['role'] != 'admin':
        flash("Unauthorized access. Please log in as an administrator.", 'danger')
        return redirect(url_for('login'))
    # Pass chain and validity directly for rendering in jinja, or fetch via AJAX if preferred
    return render_template("admin_dashboard.html", chain=blockchain.chain, valid=blockchain.is_valid_chain())

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", 'info')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True) # This is for direct `python app.py` execution