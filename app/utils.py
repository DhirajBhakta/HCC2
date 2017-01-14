from flask_login import current_user
from functools import wraps
from . import login_manager



#utype = {DOCTOR,EMPLOYEE,STUDENT,PHARMA,ADMIN}
#urole  = {PATIENT,STAFF}

def specific_login_required(utype="ANY",urole="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return login_manager.unauthorized()
            user = current_user
            if user == None: 
                return login_manager.unauthorized()
            else:
                type = user.get_utype()
                role = user.get_urole()
                if((urole == role) or (utype==type)):
                    return fn(*args,**kwargs)
                return login_manager.unauthorized()
        return decorated_view
    return wrapper