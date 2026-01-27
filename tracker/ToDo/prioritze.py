# ===== app.py (Main Flask Application) =====
"""
Flask App with Blueprints and Popup Dialog for Table Editing
"""

from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Register blueprints
from blueprints.items import items_bp
app.register_blueprint(items_bp, url_prefix='/items')

@app.route('/')
def index():
    return render_template('main.html')

# ===== blueprints/items.py =====
"""
Items Blueprint - Handles all item CRUD operations
"""

from flask import Blueprint, render_template, request, jsonify
import json
import os

items_bp = Blueprint('items', __name__)

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

@items_bp.route('/list', methods=['GET'])
def get_items():
    """Get all items (AJAX endpoint)."""
    items = load_items()
    return jsonify(items)

@items_bp.route('/add', methods=['POST'])
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

@items_bp.route('/update/<int:item_id>', methods=['PUT'])
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

@items_bp.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item (AJAX endpoint)."""
    items = load_items()
    items = [item for item in items if item['id'] != item_id]
    save_items(items)
    
    return jsonify({'success': True})

@items_bp.route('/get/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get single item (AJAX endpoint)."""
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    
    if item:
        return jsonify({'success': True, 'item': item})
    return jsonify({'success': False, 'message': 'Item not found'}), 404


# ===== templates/base.html =====
"""
Base template with navigation
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask Blueprint App{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        th, td {
            padding: 15px;
            text-align: left;
        }
        
        tbody tr {
            border-bottom: 1px solid #e1e8ed;
            transition: background 0.3s;
        }
        
        tbody tr:hover {
            background: #f8f9fa;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-warning {
            background: #ffc107;
            color: #333;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-sm {
            padding: 6px 12px;
            font-size: 12px;
        }
        
        /* Modal/Popup Dialog Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            animation: fadeIn 0.3s;
        }
        
        .modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            animation: slideDown 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideDown {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e1e8ed;
        }
        
        .modal-header h2 {
            color: #667eea;
            margin: 0;
        }
        
        .close {
            font-size: 28px;
            font-weight: bold;
            color: #aaa;
            cursor: pointer;
            transition: color 0.3s;
        }
        
        .close:hover {
            color: #333;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .form-control {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .form-control:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .modal-footer {
            display: flex;
            gap: 10px;
            margin-top: 25px;
        }
        
        .modal-footer .btn {
            flex: 1;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 500;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .actions {
            display: flex;
            gap: 8px;
        }
    </style>
    {% block extra_styles %}{% endblock %}
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
    
    {% block scripts %}{% endblock %}
</body>
</html>


# ===== templates/main.html =====
"""
Main page with table and popup dialogs
"""
{% extends "base.html" %}

{% block title %}Item Manager{% endblock %}

{% block content %}
<div class="header">
    <h1>📦 Item Manager</h1>
    <p>Manage your inventory with popup dialogs</p>
</div>

<div class="card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2>Inventory Items</h2>
        <button class="btn btn-success" onclick="openAddDialog()">+ Add Item</button>
    </div>
    
    <div id="alert-container"></div>
    
    <table id="items-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total Value</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody id="items-tbody">
            <tr>
                <td colspan="7" style="text-align: center; padding: 40px;">
                    Loading items...
                </td>
            </tr>
        </tbody>
    </table>
</div>

<!-- Add Item Modal -->
<div id="addModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Add New Item</h2>
            <span class="close" onclick="closeAddDialog()">&times;</span>
        </div>
        <form id="addForm" onsubmit="addItem(event)">
            <div class="form-group">
                <label for="add-name">Item Name</label>
                <input type="text" id="add-name" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="add-description">Description</label>
                <input type="text" id="add-description" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="add-quantity">Quantity</label>
                <input type="number" id="add-quantity" class="form-control" min="0" required>
            </div>
            <div class="form-group">
                <label for="add-price">Price ($)</label>
                <input type="number" id="add-price" class="form-control" step="0.01" min="0" required>
            </div>
            <div class="modal-footer">
                <button type="submit" class="btn btn-success">Add Item</button>
                <button type="button" class="btn btn-danger" onclick="closeAddDialog()">Cancel</button>
            </div>
        </form>
    </div>
</div>

<!-- Edit Item Modal -->
<div id="editModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Edit Item</h2>
            <span class="close" onclick="closeEditDialog()">&times;</span>
        </div>
        <form id="editForm" onsubmit="updateItem(event)">
            <input type="hidden" id="edit-id">
            <div class="form-group">
                <label for="edit-name">Item Name</label>
                <input type="text" id="edit-name" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="edit-description">Description</label>
                <input type="text" id="edit-description" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="edit-quantity">Quantity</label>
                <input type="number" id="edit-quantity" class="form-control" min="0" required>
            </div>
            <div class="form-group">
                <label for="edit-price">Price ($)</label>
                <input type="number" id="edit-price" class="form-control" step="0.01" min="0" required>
            </div>
            <div class="modal-footer">
                <button type="submit" class="btn btn-primary">Update Item</button>
                <button type="button" class="btn btn-danger" onclick="closeEditDialog()">Cancel</button>
            </div>
        </form>
    </div>
</div>

<!-- Delete Confirmation Modal -->
<div id="deleteModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Confirm Delete</h2>
            <span class="close" onclick="closeDeleteDialog()">&times;</span>
        </div>
        <p style="margin: 20px 0;">Are you sure you want to delete this item?</p>
        <div id="delete-item-info" style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;"></div>
        <div class="modal-footer">
            <button class="btn btn-danger" onclick="confirmDelete()">Yes, Delete</button>
            <button class="btn btn-primary" onclick="closeDeleteDialog()">Cancel</button>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
let currentDeleteId = null;

// Load items on page load
document.addEventListener('DOMContentLoaded', function() {
    loadItems();
});

// Load and display items
function loadItems() {
    fetch('/items/list')
        .then(response => response.json())
        .then(items => {
            const tbody = document.getElementById('items-tbody');
            
            if (items.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="7" style="text-align: center; padding: 40px; color: #666;">
                            No items yet. Click "Add Item" to get started!
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = items.map(item => `
                <tr>
                    <td><strong>#${item.id}</strong></td>
                    <td>${item.name}</td>
                    <td>${item.description}</td>
                    <td>${item.quantity}</td>
                    <td>$${item.price.toFixed(2)}</td>
                    <td><strong>$${(item.quantity * item.price).toFixed(2)}</strong></td>
                    <td>
                        <div class="actions">
                            <button class="btn btn-warning btn-sm" onclick="openEditDialog(${item.id})">Edit</button>
                            <button class="btn btn-danger btn-sm" onclick="openDeleteDialog(${item.id})">Delete</button>
                        </div>
                    </td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading items:', error);
            showAlert('Error loading items', 'danger');
        });
}

// Show alert message
function showAlert(message, type = 'success') {
    const container = document.getElementById('alert-container');
    container.innerHTML = `
        <div class="alert alert-${type}">
            ${message}
        </div>
    `;
    
    setTimeout(() => {
        container.innerHTML = '';
    }, 3000);
}

// Add Item Dialog
function openAddDialog() {
    document.getElementById('addModal').classList.add('show');
    document.getElementById('addForm').reset();
}

function closeAddDialog() {
    document.getElementById('addModal').classList.remove('show');
}

function addItem(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById('add-name').value,
        description: document.getElementById('add-description').value,
        quantity: document.getElementById('add-quantity').value,
        price: document.getElementById('add-price').value
    };
    
    fetch('/items/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            closeAddDialog();
            loadItems();
            showAlert('Item added successfully!', 'success');
        } else {
            showAlert('Error adding item', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error adding item', 'danger');
    });
}

// Edit Item Dialog
function openEditDialog(itemId) {
    fetch(`/items/get/${itemId}`)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const item = result.item;
                document.getElementById('edit-id').value = item.id;
                document.getElementById('edit-name').value = item.name;
                document.getElementById('edit-description').value = item.description;
                document.getElementById('edit-quantity').value = item.quantity;
                document.getElementById('edit-price').value = item.price;
                document.getElementById('editModal').classList.add('show');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error loading item', 'danger');
        });
}

function closeEditDialog() {
    document.getElementById('editModal').classList.remove('show');
}

function updateItem(event) {
    event.preventDefault();
    
    const itemId = document.getElementById('edit-id').value;
    const data = {
        name: document.getElementById('edit-name').value,
        description: document.getElementById('edit-description').value,
        quantity: document.getElementById('edit-quantity').value,
        price: document.getElementById('edit-price').value
    };
    
    fetch(`/items/update/${itemId}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            closeEditDialog();
            loadItems();
            showAlert('Item updated successfully!', 'success');
        } else {
            showAlert('Error updating item', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error updating item', 'danger');
    });
}

// Delete Item Dialog
function openDeleteDialog(itemId) {
    currentDeleteId = itemId;
    
    fetch(`/items/get/${itemId}`)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const item = result.item;
                document.getElementById('delete-item-info').innerHTML = `
                    <strong>${item.name}</strong><br>
                    ${item.description}<br>
                    Quantity: ${item.quantity} | Price: $${item.price.toFixed(2)}
                `;
                document.getElementById('deleteModal').classList.add('show');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error loading item', 'danger');
        });
}

function closeDeleteDialog() {
    document.getElementById('deleteModal').classList.remove('show');
    currentDeleteId = null;
}

function confirmDelete() {
    if (!currentDeleteId) return;
    
    fetch(`/items/delete/${currentDeleteId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            closeDeleteDialog();
            loadItems();
            showAlert('Item deleted successfully!', 'success');
        } else {
            showAlert('Error deleting item', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error deleting item', 'danger');
    });
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
}
</script>
{% endblock %}