'''
Shared Utilities
'''
import os
from pathlib import Path
import json
from flask import Flask
import pandas as pd

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


def loadProfile(appNm):
    '''
    Load profile into os.environ
    '''
    fnProfile = os.path.join(Path.home(),'tracker', f'profile_{appNm}.json')
    print("loadProfile: ", fnProfile)
    
    # Load the profile json
    with open(fnProfile,'r') as fio:
        pDict = json.load(fio)

    return pDict


# Assuming your app and blueprints are defined and registered somewhere
# app = Flask(__name__)
# app.register_blueprint(your_blueprint, url_prefix='/your_prefix')

def routesList(app):
    """
    Prints all routes in the application, including those from blueprints.

    rule: The URL pattern string :: @bp.route(x), (e.g., '/user/<username>' or '/static/<path:filename>').
    endpoint: An opaque string that uniquely identifies the view function associated with the URL rule. 
              By default, Flask uses the name of the view function as the endpoint.
    view_func: Python function that will be called when a request matches the URL rule.
    methods: HTTP methods (e.g., ['GET', 'POST']) that the rule responds to. 
    arguments: Information about variable parts in the URL rule (e.g., <username>). 
               These are converted to the appropriate type (like int, float, or path) before being passed as arguments to the view function.
    host or subdomain: If host matching is enabled, these attributes define the specific host or subdomain this rule applies to. 
    """
    #print("Endpoint | Methods | URL Rule")
    #print("-" * 40)
    # Iterate over all registered URL rules
    rList = []
    print("--- routeList ---- ")
    for r in app.url_map.iter_rules():
        try: f = f"{r.view_func}",
        except: f = "na"
       
        d = dict(rule = f"{r.rule}",
                 endpt = f"{r.endpoint}",
                 viewFunc = f,
                 methods = f"{r.methods}",
                 args=f"{r.arguments}",
                 host_subdom=f"{r.host if r.host else r.subdomain}"
        )
        rList.append(d)

    return pd.DataFrame(rList).to_string()
    
    return [', '.join(sorted(r.methods)) for r in app.url_map.iter_rules()]