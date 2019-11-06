from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)

    handlers = {
        'NotAuthenticated': _handle_authentication_error,
        'AuthenticationFailed': _handle_authentication_error,
        'PermissionDenied': _handle_permission_error,
        'ValidationError': _handle_validation_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_authentication_error(exc, context, response):
    response.data = {
        'detail': '未登录，请登录'
    }

    return response


def _handle_permission_error(exc, context, response):
    response.data = {
        'detail': '无此权限'
    }

    return response


def _handle_validation_error(exc, context, response):
    response.data = {
        'detail': response.data
    }

    return response
