def pop_form_kwarg(name, kwargs):
    try:
        item = kwargs.pop(name)
    except (IndexError, KeyError):
        return None, kwargs
    else:
        return item, kwargs
