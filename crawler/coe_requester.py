from collections import \
    defaultdict
from bs4 import \
    BeautifulSoup as bs
import requests
from config import \
    Config
from utils import \
    normalize_coe_url, \
    normalize_ace_url, \
    get_country_and_year_from_url, \
    read_bs_container_dict, \
    write_bs_container_dict

### Link requests

def get_coe_competition_links():
    # Requests CoE competition result page
    # and returns list of competition urls

    request_url = Config.coe_results_url
    response = requests.get(request_url)
    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        menu = soup.find('ul', id='menu-coe-country-programs-menu')
        links = list(filter(
            lambda li: 'menu-item-has-children' not in li['class'],
            menu.findAll('li', 'menu-item')
        ))
        return list(map(lambda li: normalize_coe_url(li.a['href']), links))
    else:
        print(response.status_code)
        return []

def get_ace_auction_links():
    # Requests ACE Auction result page
    # and returns list of competition urls
    # TODO: rid 'farm-directory'

    request_url = Config.ace_results_url
    response = requests.get(request_url)
    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        menu = soup.find('ul', id='menu-coe-country-programs-menu')
        links = list(filter(
            lambda li: 'menu-item-has-children' not in li['class'],
            menu.findAll('li', 'menu-item')
        ))
        return list(map(lambda li: normalize_ace_url(li.a['href']), links))
    else:
        print(response.status_code)
        return []

### Containers

##### request

def _request_containers_from_url(url):
    # return table container div from html of given url
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        container = soup.find('div', 'vc_tta-container')
        return container
    else:
        print(response.status_code)
        return

def _request_containers_from_urls(urls, write_f=None, log=True):
    # multiple web requests with logging
    container_dict = dict()
    for url in urls:
        country, year = get_country_and_year_from_url(url)
        container_dict[(country, year)] = _request_containers_from_url(url)
        if log: print(url)
    if write_f: write_f(container_dict)
    return container_dict

def request_coe_containers():
    return _request_containers_from_urls(
        get_coe_competition_links(),
        lambda container_dict: write_bs_container_dict(
            container_dict,
            Config.coe_dict_of_containers_filepath,
        )
    )

def request_ace_containers():
    return _request_containers_from_urls(
        get_ace_competition_links(),
        lambda container_dict: write_bs_container_dict(
            container_dict,
            Config.ace_dict_of_containers_filepath,
        )
    )

##### read-or-request

def _read_or_request_containers(filename, request_f):
    try: D = read_bs_container_dict(filename)
    except FileNotFoundError as e:
         D = request_f()
    return D

def read_or_request_coe_containers():
    return _read_or_request_containers(
        Config.coe_dict_of_containers_filepath,
        request_coe_containers
    )

def read_or_request_ace_containers():
    return _read_or_request_containers(
        Config.ace_dict_of_containers_filepath,
        request_ace_containers
    )

### Tests

def _test_get_competition_and_auction_links():
    def _default_link_dict():
        return {"competition_url": None, "auction_url": None}
    D = defaultdict(_default_link_dict)
    for competition_url in get_coe_competition_links():
        key = get_country_and_year_from_url(competition_url)
        D[key]["competition_url"] = competition_url
    for auction_url in get_ace_auction_links():
        key = get_country_and_year_from_url(auction_url)
        D[key]["auction_url"] = auction_url
    for ((country, year), url_dict) in D.items():
        competition_url = url_dict["competition_url"]
        auction_url = url_dict["auction_url"]
        print(f"CoE of {country} at {year}: {competition_url}, {auction_url}")
    return

def _test_all():
    _test_get_competition_and_auction_links()


### main

def main(test=False):
    if test:
        _test_all()
    else:
        D = read_or_request_coe_containers()
        # D = get_competition_table_dict_from_containers(D)
        # info = get_competition_dict_from_tables_dict(D)
        # flattened_info = sum(info.values(), [])
        # # index:int ->> row:dict (str -> str)
        # with open(Config.coe_json_of_info_filepath, 'w') as f:
        #     json.dump(flattened_info, f)
        return

if __name__ == "__main__":
    main()
