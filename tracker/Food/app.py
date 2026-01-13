from flask import Blueprint
from flask import current_app as app
from flask import render_template
import json

#---------------
# app object
#---------------

from tracker.util.appBase import appBase

class Food(appBase):
    pass

ext = Food()

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
    return f"Extension {ext.oID}.routes<br>__name__:{__name__} Blueprint<br>app.name: {app.name}<br>Status:Active<p>{str(ext).replace('\n','<br>')}"
