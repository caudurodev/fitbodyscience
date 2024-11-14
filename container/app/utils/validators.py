""" This module contains the functions to validate the input data """

from functools import wraps
from typing import List, Optional
from flask import jsonify, request
from ..config.logging import logger


def validate_input(
    required_fields: Optional[List[str]] = None,
    optional_fields: Optional[List[str]] = None,
    required_field_groups: Optional[List[List[str]]] = None,
    payload_key: str = "input",
):
    """
    Decorator to validate request input data

    Args:
        required_fields: List of required field names
        optional_fields: List of optional field names (allowed fields)
        required_field_groups: List of field groups where at least one group must be fully present
        payload_key: Key in the request payload to validate (defaults to "input")
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()

            # If payload_key is empty, validate at root level
            input_data = data if payload_key == "" else data.get(payload_key, {})

            if not input_data:
                message = "Error: no input data provided"
                return jsonify({"message": message}), 400

            # Validate required fields
            if required_fields:
                missing_fields = [
                    field for field in required_fields if field not in input_data
                ]
                if missing_fields:
                    return (
                        jsonify(
                            {
                                "message": (
                                    f"Error: missing required fields: "
                                    f"{', '.join(missing_fields)}"
                                )
                            }
                        ),
                        400,
                    )

            # Validate field groups
            if required_field_groups:
                valid_group_found = False
                for field_group in required_field_groups:
                    if all(field in input_data for field in field_group):
                        valid_group_found = True
                        break

                if not valid_group_found:
                    group_description = " OR ".join(
                        [" AND ".join(group) for group in required_field_groups]
                    )
                    return (
                        jsonify(
                            {
                                "message": (
                                    "Error: must provide one of these field "
                                    f"combinations: {group_description}"
                                )
                            }
                        ),
                        400,
                    )

            # Pass the correct data to the function
            if payload_key == "":
                return f(input_data, *args, **kwargs)
            else:
                kwargs[f"{payload_key}_data"] = input_data
                return f(*args, **kwargs)

        return decorated_function

    return decorator
