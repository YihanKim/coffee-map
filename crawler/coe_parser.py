from urllib.parse import \
    urlsplit
import itertools
from config import \
    Config

### Tables

def get_competition_table_from_container(container):
    # return table as bs4 from the container
    ul = container.find('ul', 'vc_tta-tabs-list')
    table_names = list(map(lambda li: li.string, ul.findAll('li')))
    tables = container.findAll('table')

    coe_competition_table_name = \
        list(Config.coe_competition_table_names & set(table_names))[0]
    coe_competition_table_index = \
        table_names.index(coe_competition_table_name)
    return tables[coe_competition_table_index]


def get_competition_table_dict_from_containers(containers_dict):
    # run multiple (get_competition_table_from_container)
    # based on (containers_dict)
    d = dict()
    for key in containers_dict:
        container = containers_dict[key]
        coe_table = get_competition_table_from_container(container)
        d[key] = coe_table
    return d

##### Table extraction - head, body, farm links

def _contains_thead(table):
    return table.findAll('th') != []

def _map_string_to_row(row):
    return list(map(lambda td: td.text.strip(), row))

def _filter_empty_row(tbody):
    # Due to some ugly column exists on the tbody,
    # we filter out those using some expense;
    # see Rwanda 2018: https://cupofexcellence.org/rwanda-2018/
    # see Mexico 2018: https://cupofexcellence.org/mexico-2018/
    is_nonempty_row = lambda row: all(_map_string_to_row(row))
    return list(filter(is_nonempty_row, tbody))

def _get_raw_thead_from_table(table):
    # extract first column of the table
    # returns (list of bs4 element)
    if _contains_thead(table):
        thead = table.findAll('th')
    else: # returns all tds in first tr
        thead = table.find('tr').findAll('td')
    return thead

def _get_raw_tbody_from_table(table):
    # extract non-first columns of the table
    # returns (list of (list of bs4 element))
    tbody = table.find('tbody')
    if _contains_thead(table):
        tbody = tbody.findAll('tr')
    else: # returns trs without the first
        tbody = tbody.findAll('tr')[1:]
    tbody = list(map(lambda tr: tr.findAll('td'), tbody))
    return _filter_empty_row(tbody)

def get_thead_from_raw_thead(raw_thead):
    return list(map(lambda th: th.text, raw_thead))

def get_tbody_from_raw_tbody(raw_tbody):
    return list(map(_map_string_to_row, raw_tbody))

def get_farm_links_from_raw_tbody(raw_tbody):
    farm_links = []
    for row in raw_tbody:
        links = list(map(
            lambda td: td.find('a')['href'],
            filter(lambda td: td.find('a'), row)
        ))
        # No links:
        # El Salvador 2008
        # Guatemala 2008, 2006, 2002
        # Mexico 2013, 2012
        if len(links) > 0:
            link = links[0]
            farm_links.append(link)
        else:
            farm_links.append(None)
    return farm_links


def get_competition_dict_from_tables_dict(tables_dict):
    info = dict()
    # info:
    # (country, year):2-tuple-of-str
    #   ->> index:int
    #   ->> row:dict (str -> str)
    for key, table in tables_dict.items():
        raw_thead = _get_raw_thead_from_table(table)
        raw_tbody = _get_raw_tbody_from_table(table)
        thead = get_thead_from_raw_thead(raw_thead)
        tbody = get_tbody_from_raw_tbody(raw_tbody)
        farm_links = get_farm_links_from_raw_tbody(raw_tbody)
        assert len(tbody) == len(farm_links)
        coe_competition_results = []
        for row, farm_link in zip(tbody, farm_links):
            d = {k: v for k, v in zip(thead, row)}
            d['farm_link'] = farm_link
            d['country'], d['year'] = key
            coe_competition_results.append(d)
        info[key] = coe_competition_results
    return info

def main():
    from coe_requester import \
        read_or_request_coe_containers
    D = read_or_request_coe_containers()
    D = get_competition_table_dict_from_containers(D)
    info = get_competition_dict_from_tables_dict(D)
    flattened_info = sum(info.values(), [])
    # index:int ->> row:dict (str -> str)
    with open(Config.coe_json_of_info_filepath, 'w') as f:
        json.dump(flattened_info, f)

if __name__ == "__main__":
    main()
