from tracker.extensions.Property import bp

@bp.route(f'/{ext.oID}/test')
def _test():
    {"message": f'{ext.oID}.routes name:{__name__} Blueprint',
    "ext.ui.config": ext.ui.config}
    
