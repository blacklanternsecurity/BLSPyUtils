"""
BLS Utilities - Common functionality.
"""

from datetime import datetime, date, timedelta
from configparser import ConfigParser
import os
from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode
import json


def read_config(path):
    """
    Read config file.
    :param path:
    :return:
    """
    config = ConfigParser()
    config.read(path)
    return config


def write_config(path, config, section_dict=None):
    """

    :param path:
    :param config:
    :param section_dict:
    :return:
    """
    # section_dict = {'GRAPES': [{'key': 'LAST', 'value': 'a'}], 'ORANGE': []}
    for section in section_dict:
        for kv_list in section_dict[section]:
            config.set(section, kv_list['key'], kv_list['value'])
    with open(path, 'w') as config_file:
        config.write(config_file)


def get_file_path(input_file, config_file):
    """Good for getting the current path of the python script by using __file__ and then joining a config name to it."""
    return os.path.join(os.path.dirname(os.path.abspath(input_file)), config_file)


def default_json_serializer(obj):
    """Default JSON serializer. Usually fed to default of json.dumps"""
    if isinstance(obj, datetime) or isinstance(obj, date) or isinstance(obj, timedelta):
        return str(obj)
    else:
        return obj


def json_serializer(the_dict):
    """Runs through entire dictionary to serialize."""
    for key in the_dict:
        the_dict[key] = default_json_serializer(the_dict[key])
    return the_dict


def list_to_json_serialize(the_list):
    """List of dicts to serialize"""
    new_list = []
    for the_dict in the_list:
        new_list.append(json_serializer(the_dict))
    return new_list


def datetime_converter(in_datetime: datetime, format_str: str = '%Y-%m-%dT%H:%M:%S') -> str:
    """
    Convert datetime object to str.
    :param in_datetime: datetime object (should be utc/timezone agnostic)
    :param format_str: default format is 2017-05-10T00:00:00
    :return: str in designated format
    """
    return in_datetime.strftime(format_str)


def datestr_converter(in_datestr: str, format_str: str = '%Y-%m-%dT%H:%M:%S') -> datetime:
    """
    Convert datetime str into datetime.
    :param in_datestr: str in designated format
    :param format_str: default format is 2017-05-10T00:00:00
    :return: datetime object (should be utc/timezone agnostic)
    """
    return datetime.strptime(in_datestr, format_str)


def make_token(pkey, payload):
    """

    :param pkey:
    :param payload:
    :return:
    """
    encryption_key = jwk.JWK.from_pem(pkey)
    jwe_token = jwe.JWE(json.dumps(payload),
                        json_encode({'alg': "RSA-OAEP",
                                     'enc': "A128CBC-HS256"}))
    jwe_token.add_recipient(encryption_key)
    jwt_token = jwe_token.serialize()
    return jwt_token


def object_dump(obj_name, obj_inst):
    def dig_deep(prop_value):
        dd_str = prop_value
        if type(prop_value).__str__ is object.__str__ and not isinstance(prop_value, str):
            dd_str = object_dump(prop_value.__class__.__name__, prop_value)
        return str(dd_str)

    obj_vars = sorted([x for x in tuple(set(obj_inst.__dict__)) if not x.startswith('__')])
    return '{}({})'.format(obj_name, ', '.join(['{}={}'.format(var, dig_deep(getattr(obj_inst, var))) for var in obj_vars]))
