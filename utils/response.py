def success(data=None):
    return {
        'success': True,
        'data': data
    }


def error(message):
    return {
        'success': False,
        'message': message
    }
