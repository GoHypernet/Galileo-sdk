def generate_query_str(*args, **kwargs):
    params = args[0]
    param_str = ""
    for key in params:
        if params[key]:
            if isinstance(params[key], list) and len(params[key]) == 0:
                pass
            elif isinstance(params[key], list):
                for list_item in params[key]:
                    param_str += "{key}={list_item}&".format(
                        key=key, list_item=list_item
                    )
            else:
                param_str += "{key}={param}&".format(key=key, param=params[key])

    param_str = param_str[:-1]
    return param_str
