from flask_login import current_user
from functools import wraps
from . import login_manager

def specific_login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return login_manager.unauthorized()
            user = current_user
            if user == None: 
                return login_manager.unauthorized()
            else:
                urole = user.get_utype()
                print(user.get_utype())
                if ( (urole != role) and (role != "ANY")):
                    return login_manager.unauthorized()      
                return fn(*args, **kwargs)
        return decorated_view
    return wrapper