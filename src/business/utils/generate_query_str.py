def generate_query_str(*args, **kwargs):
    params = args[0]
    param_str = ""

    for key in params:
        if params[key] is not None:
            if isinstance(params[key], list):
                for list_item in params[key]:
                    param_str += f"{key}={list_item}&"
            else:
                param_str += f"{key}={params[key]}&"

    param_str = param_str[:-1]
    return param_str
