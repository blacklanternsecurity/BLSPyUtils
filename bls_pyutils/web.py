import stringcase


def data_formatter(data_dict, form_data):
    for k in data_dict:
        data_dict[k] = form_data.get(stringcase.camelcase(k), data_dict[k])
    return data_dict


def transform_checkbox(checkbox):
    """Transform checkbox return value from JavaScript."""
    if checkbox == 'on':
        return True
    elif checkbox == 'off':
        return False
    else:
        return False


def transform_boolean(bool_value):
    """Transform boolean return value from JavaScript."""
    if bool_value == 'true':
        return True
    elif bool_value == 'false':
        return False
    else:
        return False
