import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# File-based database for simplicity and portability
DATA_FILE = os.path.join(os.path.dirname(__file__), 'expenses_data.json')

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"expenses": [], "user": None}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/auth/login', methods=['POST'])
def login():
    req_data = request.get_json() or {}
    identity = req_data.get('identity', '')
    login_type = req_data.get('type', 'email_phone') # 'email_phone' or 'google'
    
    data = load_data()
    data['user'] = {
        'identity': identity if identity else ('google_user@gmail.com' if login_type == 'google' else 'user@example.com'),
        'login_type': login_type,
        'logged_in': True
    }
    save_data(data)
    return jsonify({"status": "success", "user": data['user']})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    data = load_data()
    data['user'] = None
    save_data(data)
    return jsonify({"status": "success"})

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    data = load_data()
    return jsonify({"expenses": data.get('expenses', []), "user": data.get('user')})

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    req_data = request.get_json() or {}
    data = load_data()
    
    new_expense = {
        "id": req_data.get("id"),
        "title": req_data.get("title", "Expense"),
        "amount": float(req_data.get("amount", 0)),
        "category": req_data.get("category", "General"),
        "date": req_data.get("date"),
        "payment_method": req_data.get("payment_method", "Cash"),
        "notes": req_data.get("notes", "")
    }
    
    data["expenses"].insert(0, new_expense)
    save_data(data)
    return jsonify({"status": "success", "expense": new_expense})

@app.route('/api/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    req_data = request.get_json() or {}
    data = load_data()
    
    updated = None
    for i, exp in enumerate(data["expenses"]):
        if str(exp["id"]) == str(expense_id):
            data["expenses"][i] = {
                "id": expense_id,
                "title": req_data.get("title", exp["title"]),
                "amount": float(req_data.get("amount", exp["amount"])),
                "category": req_data.get("category", exp["category"]),
                "date": req_data.get("date", exp["date"]),
                "payment_method": req_data.get("payment_method", exp["payment_method"]),
                "notes": req_data.get("notes", exp["notes"])
            }
            updated = data["expenses"][i]
            break
            
    if updated:
        save_data(data)
        return jsonify({"status": "success", "expense": updated})
    return jsonify({"status": "error", "message": "Expense not found"}), 404

@app.route('/api/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    data = load_data()
    initial_count = len(data["expenses"])
    data["expenses"] = [exp for exp in data["expenses"] if str(exp["id"]) != str(expense_id)]
    
    if len(data["expenses"]) < initial_count:
        save_data(data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Expense not found"}), 404

if __name__ == '__main__':
    print("Starting Expense Tracker server at http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
