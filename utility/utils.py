from graphql_jwt.decorators import user_passes_test, context
from functools import wraps


''' 25mb'''
file_size = 10485760 * 2.5


def file_size_check(file_name, exc=Exception("File Size Excedded")):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if context.FILES[file_name].size < file_size:
                return f(*args, **kwargs)
            raise exc

        return wrapper

    return decorator
