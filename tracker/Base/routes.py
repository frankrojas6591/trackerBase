from tracker.extensions.Base import bp, ext

print("Base Route>", '/Base')
print("Base ext>", ext.ui.config)
@bp.route('/Base')
def get_users():
    return {"message": f'Base.routes name:{__name__} Blueprint'}
    
@bp.route('/BaseFIXME')
def index():
    return f'This is The {__name__} Blueprint: {tracker.appBase.main.__name__}'