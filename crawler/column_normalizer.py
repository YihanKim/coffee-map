import pandas as pd
import json
from config import \
    Config

column_map = {
    'FARM':        'Farm / CWS',
    'Farm':        'Farm / CWS',
    'FARM/CWS':    'Farm / CWS',
    'FARM / CWS':  'Farm / CWS',
    'Farm / CWS':  'Farm / CWS',

    'FARMER':                    'Farmer / Representative',
    'Farmer':                    'Farmer / Representative',
    'FARMER / REPRESENTATIVE':   'Farmer / Representative',
    'Farmer / Representative':   'Farmer / Representative',
    'FARMER / ORGANIZATION':     'Farmer / Representative',

    'PRODUCER':     'Producer',
    'Producer':     'Producer',
    'OWNER':        'Owner',

    'RANK': 'Rank',
    'Rank': 'Rank',

    'SCORE': 'Score',
    'Score': 'Score',

    'PROCESS': 'Process',
    'Process': 'Process',
    'PROCESSING': 'Process',
    'Processing': 'Process',

    'VARIETY': 'Variety',
    'Variety': 'Variety',

    'REGION': 'Region',
    'Region': 'Region',

    'LOT NO.':           "Size",
    'SIZE':              "Size",
    'SIZE (30KG BOXES)': "Size",
    'Size':              "Size",
    'Size (30kg Boxes)': "Size",
    'WEIGHT (kg)': 'Weight',
    'Weight (kg)': 'Weight',
    'Weight (lbs)': 'Weight',
    'Weight (lbs.)': 'Weight',

    'Woreda': 'Woreda',
    'WOREDA': 'Woreda',
    'Zone': 'Zone',
    'ZONE': 'Zone',

    'farm_link': 'farm_link',
    'country': 'country',
    'year': 'year',
}

def map_column(d):
    # debug purpose
    try:
        new_d = {column_map[k]: v for k, v in d.items()}
    except KeyError as e:
        raise e
    #assert len(d) == len(new_d), (d, new_d)
    return new_d

### Column handler
# the following functions starts with '_handle'
# will mutate the input object.

def _handle_score(d):
    # The first Guatemala CoE (Guatemala 2001) missed the score.
    # this function fill them out, and convert the score type as float.
    if 'Score' not in d:
        d['Score'] = -1.0
    else:
        d['Score'] = float(d['Score'])
    return

def _handle_region(d):
    # Ethiopia started hosting CoE competitions in 2020.
    # They recorded 'Woreda' and 'Zone' columns instead of 'Region'.
    # These have simliar meanings to 'district' and 'region' respectively,
    #     see: https://en.wikipedia.org/wiki/Districts_of_Ethiopia
    # and see: https://en.wikipedia.org/wiki/List_of_zones_of_Ethiopia
    if 'Woreda' in d:
        if 'Region' not in d:   # Ethiopia 2020
            d['Region'] = f"{d['Woreda']}, {d['Zone']}"
            del d['Woreda'], d['Zone']
        else:                   # Ethiopia 2021
            d['Region'] = f"{d['Woreda']}, {d['Zone']}, {d['Region']}"
            del d['Woreda'], d['Zone']
    return

def _handle_representative_as_producer(d):
    # Colombia CoE records 'Producer' instead of 'Farmer / Representative'.
    if 'Producer' in d:
        d['Farmer / Representative'] = d['Producer']
        del d['Producer']
    return

def _handle_representative_as_owner(d):
    # Burundi 2019 records 'Owner' instead of 'Farmer / Representative'.
    if "Owner" in d and "Farmer / Representative" not in d:
        d["Farmer / Representative"] = d['Owner']
        del d['Owner']
    return

def _handle_farm(d):
    # Ethiopia have no farm name on the table.
    if 'Farm / CWS' not in d:
        d['Farm / CWS'] = "N/A"

def normalize_column(d):

    _handle_score(d)
    _handle_region(d)
    _handle_farm(d)
    _handle_representative_as_producer(d)
    _handle_representative_as_owner(d)

    assert 'Rank' in d
    assert 'Region' in d
    assert 'Score' in d
    assert 'Farm / CWS' in d
    assert 'Farmer / Representative' in d

    return d


def normalize_columns(list_of_dict):
    return list(map(
        lambda d: normalize_column(map_column(d)),
        list_of_dict
    ))

def main(test=False):
    with open(Config.coe_json_of_info_filepath, 'r') as f:
        info = json.load(f) # index:int ->> row:dict (str -> str)
    normalized_info = normalize_columns(info)
    with open(Config.coe_normalized_json_of_info_filepath, 'w') as f:
        info = json.dump(normalized_info, f)
    return

if __name__ == "__main__":
    main()
