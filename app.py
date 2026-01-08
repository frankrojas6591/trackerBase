# ===== app.py (Main Flask Application) =====
"""
Expense Tracker - Complete Flask App with Microservices
For PythonAnywhere deployment
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from datetime import datetime
import json
import os

from UserService import UserService
from ExpenseService import ExpenseService

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# ===== DATA STORAGE (Simulated Database) =====
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
EXPENSES_FILE = os.path.join(DATA_DIR, 'expenses.json')

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filename):
    """Load data from JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_json(filename, data):
    """Save data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# ===== AUTHENTICATION DECORATOR =====
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===== ROUTES =====

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        result = UserService.authenticate(username, password)
        
        if result['success']:
            session['user_id'] = result['user']['id']
            session['username'] = result['user']['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result['message'], 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        result = UserService.create_user(username, password)
        
        if result['success']:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    expenses = ExpenseService.get_all_expenses(user_id)
    stats = ExpenseService.get_statistics(user_id)
    return render_template('dashboard.html', expenses=expenses, stats=stats)

@app.route('/expenses')
@login_required
def list_expenses():
    user_id = session['user_id']
    expenses = ExpenseService.get_all_expenses(user_id)
    return render_template('expenses.html', expenses=expenses)

@app.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount')
        description = request.form.get('description')
        date = request.form.get('date')
        
        result = ExpenseService.create_expense(
            session['user_id'],
            category,
            amount,
            description,
            date
        )
        
        if result['success']:
            flash('Expense added successfully!', 'success')
            return redirect(url_for('list_expenses'))
    
    return render_template('add_expense.html')

@app.route('/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = ExpenseService.get_expense(expense_id)
    
    if not expense or expense['user_id'] != session['user_id']:
        flash('Expense not found', 'danger')
        return redirect(url_for('list_expenses'))
    
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount')
        description = request.form.get('description')
        date = request.form.get('date')
        
        result = ExpenseService.update_expense(
            expense_id,
            category,
            amount,
            description,
            date
        )
        
        if result['success']:
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('list_expenses'))
    
    return render_template('edit_expense.html', expense=expense)

@app.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = ExpenseService.get_expense(expense_id)
    
    if expense and expense['user_id'] == session['user_id']:
        ExpenseService.delete_expense(expense_id)
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Expense not found', 'danger')
    
    return redirect(url_for('list_expenses'))

# ===== API ENDPOINTS (for potential mobile/external access) =====

@app.route('/api/expenses', methods=['GET'])
@login_required
def api_get_expenses():
    user_id = session['user_id']
    expenses = ExpenseService.get_all_expenses(user_id)
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
@login_required
def api_create_expense():
    data = request.json
    result = ExpenseService.create_expense(
        session['user_id'],
        data['category'],
        data['amount'],
        data['description'],
        data['date']
    )
    return jsonify(result)

@app.route('/api/statistics', methods=['GET'])
@login_required
def api_get_statistics():
    user_id = session['user_id']
    stats = ExpenseService.get_statistics(user_id)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
