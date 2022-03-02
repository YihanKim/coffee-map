
import json
import requests
from bs4 import \
    BeautifulSoup as bs
from urllib.parse import \
    urlsplit, \
    urlunsplit
from config import \
    Config, \
    FarmConfig

def request_farm_directory_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        # description
        # farm information
        # score
        # lot information
        # gallery
        # location
        return None
    else:
        print(response.status_code)
        return []

def request_dev_coe_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        # images
        # description
        # details
        return None
    else:
        print(response.status_code)
        return []

def request_coe_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        # images
        # description
        # details
        # NOTE: two origins (coe_url and dev_coe_url) serve identical.
        return None
    else:
        print(response.status_code)
        return []

def _check_url_integrity(url):
    # check url have no query or fragment
    url_components = urlsplit(url)
    if url_components.fragment or url_components.query:
        return False
    return True

def _get_url_origin(url):
    # normalize url (scheme and path)
    url_components = urlsplit(url)
    clean_url_components = url_components \
        ._replace(path="/") \
        ._replace(scheme="https")   # handles 'http'
    return urlunsplit(clean_url_components)


def crawl_farm_info_by_url(url):
    origin = _get_url_origin(url)
    if origin == FarmConfig.farm_directory_url:
        #print(url)
        #return request_farm_directory_url(url)
        pass
    elif origin == FarmConfig.dev_coe_url:
        #print(url)
        #return request_dev_coe_url(url)
        pass
    elif origin == FarmConfig.coe_url:
        print(url)
        return request_coe_url(url)
    else:
        if origin == "https://allianceforcoffeeexcellence.org/":
            return
        raise NotImplementedError(f'Not Implemented: {origin}')


def main():
    with open(Config.coe_normalized_json_of_info_filepath, 'r') as f:
        info = json.load(f)

    for row_dict in info:
        farm_url = row_dict['farm_link']
        if farm_url and _check_url_integrity(farm_url):
            crawl_farm_info_by_url(farm_url)

    return

if __name__ == "__main__":
    main()
