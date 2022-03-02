#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
from coe_requester import \
    read_or_request_coe_containers
from coe_parser import \
    get_competition_table_dict_from_containers, \
    get_competition_dict_from_tables_dict
from column_normalizer import \
    normalize_columns
from config import \
    Config

def prepare():
    D = read_or_request_coe_containers()
    D = get_competition_table_dict_from_containers(D)
    info = get_competition_dict_from_tables_dict(D)
    flattened_info = sum(info.values(), [])
    normalized_info = normalize_columns(flattened_info)
    with open(Config.coe_normalized_json_of_info_filepath, 'w') as f:
        info = json.dump(normalized_info, f)
    return

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    if not os.path.exists(Config.coe_normalized_json_of_info_filepath):
        prepare()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    return

if __name__ == "__main__":
    main()
