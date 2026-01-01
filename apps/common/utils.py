# apps/common/utils.py
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    Custom exception handler to ensure standard error response format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        response.data = {
            "status": "error",
            "message": data.get("detail", "An error occurred"),
            "data": data
        }
    return response
    