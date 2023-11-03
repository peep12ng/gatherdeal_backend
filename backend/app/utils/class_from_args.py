from dataclasses import fields

def class_from_args(class_name, arg_dict: dict):
    field_set = {f.name for f in fields(class_name) if f.init}
    filtered_arg_dict = {k : v for k, v in arg_dict.items() if k in field_set}
    return class_name(**filtered_arg_dict)