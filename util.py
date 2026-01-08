'''
Shared Utilities
'''
import os
import json

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
EXPENSES_FILE = os.path.join(DATA_DIR, 'expenses.json')

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

