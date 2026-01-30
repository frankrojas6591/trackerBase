# ===== blueprints/items.py =====
"""
Items Blueprint - Handles all item CRUD operations
"""

from flask import Blueprint, render_template, request, jsonify
import json
import os

from .ToDo import ToDo

ext = ToDo()

#OLD: bp = Blueprint('ToDo', __name__, template_folder="templates", static_folder="static")
bp = Blueprint(ext.oID, __name__, url_prefix=f'/{ext.oID}/api', template_folder="templates", static_folder="static")


# Simulated database (in production, use a real database)
ITEMS_FILE = 'data/items.json'


def setStatus(item_id, status):
    ext.load()
    tDict = ext.setStatus(item_id, status)
    if tDict : 
        ext.save()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Item not found'}), 404


#import .routes
@bp.route('/test')
def _test():
    rStr = routesList(app)
    print(f"<p>----- List All routesn ---")
    print(rStr)
    msg = f"Extension {ext.oID}.routes"
    msg += f"<br>__name__:{__name__} Blueprint"
    msg += f"<br>app.name: {app.name}"
    msg += f"<br>Status:Active"
    msg += f"<p>{str(ext).replace('\n','<br>')}"
    print("ToDo _test:", msg)
    return msg
    
@bp.route('/')
def index():
    return render_template('ToDo.html')


@bp.route('/list/<view>/<sortBy>', methods=['GET'])
def get_items(view, sortBy):
    """Get all items (AJAX endpoint)."""
    return jsonify(ext.fetch(view, sortBy))
                   
    if view == 'home':  
        # default home view : exclude Done, Del
        dispOrder = ['Prio', 'Active', 'Hidden']
    elif view == 'All':
        dispOrder = ['Prio', 'Active', 'Hidden', 'Done', 'Del']

    # ------ filter view : Merge lists in order of dispOrder
    itemList = ext.fetch()
    dispList = []
    for s in dispOrder:
        dispList += [t for t in itemList if t['status'] == s]
    
    # Add any items not in sOrder
    if view == 'All' :
        dispList += [t for t in itemList if t['status'] not in dispOrder]

    #-------- sort -----
    
        
    return jsonify(dispList)

@bp.route('/status/<item_id>/<st>', methods=['GET'])
def status(item_id,st):
    """Get all items (AJAX endpoint)."""
    setStatus(item_id, st)
    return jsonify({'success': True})

@bp.route('/done/<item_id>', methods=['GET'])
def setDone(item_id):
    """Get all items (AJAX endpoint)."""
    setStatus(item_id, 'Done')
    return jsonify({'success': True})

@bp.route('/delete/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item (AJAX endpoint)."""
    setStatus(item_id, 'Del')
    return jsonify({'success': True})

@bp.route('/add', methods=['POST'])
def add_item():
    """Add new item (AJAX endpoint)."""
    itemDict = request.json
    ext.load()
    new_item = ext.add(itemDict)
    return jsonify({'success': True, 'item': new_item})

@bp.route('/update/<item_id>', methods=['PUT'])
def update_item(item_id):
    """Update existing item (AJAX endpoint)."""
    data = request.json

    ext.load()
    tDict = ext.get(item_id)
    if tDict:
        tDict['category'] = data.get('category', tDict['category'])
        tDict['desc'] = data.get('desc', tDict['desc'])
        ext.save()
        return jsonify({'success': True, 'item': tDict})
    return jsonify({'success': False, 'message': 'Item not found'}), 404


@bp.route('/get/<item_id>', methods=['GET'])
def get_item(item_id):
    """Get single item (AJAX endpoint)."""
    ext.load()
    tDict = ext.get(item_id)
    if tDict:
        return jsonify({'success': True, 'item': tDict})
    return jsonify({'success': False, 'message': 'Item not found'}), 404

