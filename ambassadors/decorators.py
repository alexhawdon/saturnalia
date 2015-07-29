try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper  # Python 2.3, 2.4 fallback.
    
def ambassador_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is a logged
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

