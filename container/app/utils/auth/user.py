""" This module contains the functions to check if the user exists """

from functools import wraps
from flask import jsonify, request
from ...store.user import get_user_by_id
from ...config.logging import logger


def is_user_exists(user_id: str):
    """Check if the user exists"""
    user = get_user_by_id(user_id)
    return user is not None


def is_request_allowed(data: dict):
    """Check if the request is allowed"""
    user_id = data.get("session_variables", {}).get("x-hasura-user-id", None)
    if user_id is None:
        return False
    return is_user_exists(user_id)


def require_auth(f):
    """Decorator to require authentication for the endpoint"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Get the full request data
            data = request.get_json() or {}

            # Look for session variables in both root and input
            session_vars = data.get("session_variables")
            if not session_vars and "input" in data:
                session_vars = data["input"].get("session_variables")

            user_id = session_vars.get("x-hasura-user-id") if session_vars else None

            if not user_id or not is_user_exists(user_id):
                return jsonify({"message": "Error: user not found"}), 404

            # Just proceed with the original function call without adding extra kwargs
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({"message": "Error: invalid request"}), 400

    return decorated_function


def require_role(role):
    """Decorator to require a specific role for the endpoint"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            session_vars = data.get("session_variables")
            if not session_vars and "input" in data:
                session_vars = data["input"].get("session_variables")

            user_role = session_vars.get("x-hasura-role") if session_vars else None

            if user_role != role:
                return (
                    jsonify({"message": f"Error: requires {role} role"}),
                    403,
                )

            return f(*args, **kwargs)
        return decorated_function
    return decorator
