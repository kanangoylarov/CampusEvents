"""
JWT Token management utilities.
The JWT manager is initialized in app.extensions and the Flask app factory.
This module provides utility functions for JWT operations if needed.
"""

from flask_jwt_extended import create_access_token, get_jwt_identity


def create_user_token(user_id):
    """
    Create a JWT access token for a user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        A JWT access token string
    """
    return create_access_token(identity=user_id)

