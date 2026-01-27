# ===== blueprints/items.py =====
"""
Items Blueprint - Handles all item CRUD operations
"""

from flask import Blueprint, render_template, request, jsonify
import json
import os

bp = Blueprint('items', __name__, template_folder="templates", static_folder="static")

# Simulated database (in production, use a real database)
ITEMS_FILE = 'data/items.json'

def load_items():
    """Load items from JSON file."""
    os.makedirs('data', exist_ok=True)
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_items(items):
    """Save items to JSON file."""
    os.makedirs('data', exist_ok=True)
    with open(ITEMS_FILE, 'w') as f:
        json.dump(items, f, indent=2)

@bp.route('/list', methods=['GET'])
def get_items():
    """Get all items (AJAX endpoint)."""
    items = load_items()
    return jsonify(items)

@bp.route('/add', methods=['POST'])
def add_item():
    """Add new item (AJAX endpoint)."""
    data = request.json
    items = load_items()
    
    new_item = {
        'id': max([item['id'] for item in items], default=0) + 1,
        'name': data.get('name', ''),
        'description': data.get('description', ''),
        'quantity': int(data.get('quantity', 0)),
        'price': float(data.get('price', 0))
    }
    
    items.append(new_item)
    save_items(items)
    
    return jsonify({'success': True, 'item': new_item})

@bp.route('/update/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update existing item (AJAX endpoint)."""
    data = request.json
    items = load_items()
    
    for item in items:
        if item['id'] == item_id:
            item['name'] = data.get('name', item['name'])
            item['description'] = data.get('description', item['description'])
            item['quantity'] = int(data.get('quantity', item['quantity']))
            item['price'] = float(data.get('price', item['price']))
            save_items(items)
            return jsonify({'success': True, 'item': item})
    
    return jsonify({'success': False, 'message': 'Item not found'}), 404

@bp.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item (AJAX endpoint)."""
    items = load_items()
    items = [item for item in items if item['id'] != item_id]
    save_items(items)
    
    return jsonify({'success': True})

@bp.route('/get/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get single item (AJAX endpoint)."""
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    
    if item:
        return jsonify({'success': True, 'item': item})
    return jsonify({'success': False, 'message': 'Item not found'}), 404

