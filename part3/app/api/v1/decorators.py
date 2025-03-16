from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import jsonify

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("is_admin"):
                return fn(*args, **kwargs)
            else:
                return {"error": "Admin privileges required"}, 403
        return decorator
    return wrapper
