# --- tracker/__init__
import os
import importlib
from flask import Flask

from config import Config

"""Initialize Flask app."""

from flask import Flask
#from flask_assets import Environment

def create_app():
    """Create Flask application."""
    print("tracker init start")
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    if False:
        assets = Environment()
        assets.init_app(app)

    with app.app_context():
        # Import parts of our application
        #from .assets import compile_static_assets
        from .Base import app as appBase
        app.register_blueprint(appBase.bp)
        print("Blueprint extension registered: Base")

        from .Auth import app as homeAuth
        app.register_blueprint(homeAuth.bp)
        print("Blueprint extension registered: Auth")

        from .Property import app as homeProperty
        app.register_blueprint(homeProperty.bp)
        print("Blueprint extension registered: Property")
        
        from .Mood import app as homeMood
        app.register_blueprint(homeMood.bp)
        print("Blueprint extension registered: Mood")
        
        from .Food import app as homeFood
        app.register_blueprint(homeFood.bp)
        print("Blueprint extension registered: Food")
        
        from .ToDo import app as homeToDo
        app.register_blueprint(homeToDo.bp)
        print("Blueprint extension registered: ToDo")

        if False:
            # Compile static assets
            compile_static_assets(assets)

        return app