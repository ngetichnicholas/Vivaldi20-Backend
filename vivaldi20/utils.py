from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Check for authentication errors
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        response.data = {
            "message": "Unauthenticated."
        }
    
    return response