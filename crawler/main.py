import os
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
    if not os.path.exists(Config.coe_normalized_json_of_info_filepath):
        prepare()
    # run API server here
    return

if __name__ == "__main__":
    main()
