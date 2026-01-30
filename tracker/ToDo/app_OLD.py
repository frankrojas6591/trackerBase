from flask import Blueprint
from flask import current_app as app
from flask import render_template, request, redirect, url_for
import json

from tracker.util.util import routesList

#---------------
# app object
#---------------

from .ToDo import ToDo

ext = ToDo()

def create_ext(app):
    return ext

#---------------
# declare blue print 
#---------------
# Blueprint Configuration
bp = Blueprint(ext.oID, __name__, url_prefix=f'/{ext.oID}/api', template_folder="templates", static_folder="static")


#---------------
# routes
#---------------
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
    msg += f"<p>----- List All routesn ---"
    msg += rStr
    return msg


@bp.route('/')
def home():
    #print("---- ToDo.home route", flush=True)
    return render_template('taskList.html', taskList=ext.taskList)

@bp.route('/add', methods=['POST'])
def add_todo():
    taskDict = request.form
    ext.add(taskDict)
    return redirect(url_for('.home'))

@bp.route('/tasks')
def tasks():
    # Pass the data to the Jinja2 template
    return render_template('table.html', items=ext.taskList) #ext.taskList)

@bp.route('/taskAtion', methods=['POST'])
def taskAction():
    # Receive the selected row ID from the JavaScript AJAX request
    item_id = request.form.get('item_id')
    # Perform backend logic (e.g., fetch more details from a database)
    selected_item = next((item for item in data_rows if item['id'] == int(item_id)), None)
    
    if selected_item:
        # Return a JSON response with the action details
        return jsonify({
            'status': 'success',
            'message': f"Action performed for {selected_item['name']}. Description: {selected_item['description']}",
            'item_name': selected_item['name']
        })
    else:
        return jsonify({'status': 'error', 'message': 'Item not found'})

@bp.route('/taskAtion2', methods=['POST'])
def taskAction2():
    # Receive the selected row ID from the JavaScript AJAX request
    item_id = request.form.get('item_id')
    # Perform backend logic (e.g., fetch more details from a database)
    selected_item = next((item for item in data_rows if item['id'] == int(item_id)), None)
    
    if selected_item:
        # Return a JSON response with the action details
        return jsonify({
            'status': 'success',
            'message': f"Action performed for {selected_item['name']}. Description: {selected_item['description']}",
            'item_name': selected_item['name']
        })
    else:
        return jsonify({'status': 'error', 'message': 'Item not found'})

@bp.route('/about')
def about():
    return render_template('about.html')



