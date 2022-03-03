
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
from utils import \
    _get_ancestor_tag


def _get_description_from_farm_directory_soup(soup):
    # get description as a string
    try:
        description_title = soup.find('h5', text='Description')
        description_box = _get_ancestor_tag(description_title, 3)
    except AttributeError:
        description = ""
    else:
        body = description_box.find('div', 'pf-body')
        description = body.text
    finally:
        return description

def _get_farm_information_from_farm_directory_soup(soup):
    # get farm information as a dictionary
    try:
        farm_information_title = soup.find('h5', text='Farm Information')
        farm_information_box = _get_ancestor_tag(farm_information_title, 3)
    except AttributeError:
        farm_info = dict()
    else:
        farm_details = farm_information_box.findAll('li')
        farm_attrs = map(
            lambda li: li.find('div', 'item-attr').text.strip(),
            farm_details
        )
        farm_props = map(
            lambda li: li.find('div', 'item-property').text.strip(),
            farm_details
        )
        farm_info = {k: v for k, v in zip(farm_attrs, farm_props)}
    finally:
        try:
            assert "Farm Name" in farm_info
            assert "Farmer" in farm_info
            assert "Altitude" in farm_info
            assert "Farm Size" in farm_info
        except AssertionError:
            print(farm_info)
        return farm_info

def _get_lot_information_from_farm_directory_soup(soup):
    # get lot information as a dictionary
    # (both codes for lot info. and farm info. are identical)
    try:
        lot_information_title = soup.find('h5', text='Lot Information')
        lot_information_box = _get_ancestor_tag(lot_information_title, 3)
    except AttributeError:
        lot_info = dict()
    else:
        lot_details = lot_information_box.findAll('li')
        lot_attrs = map(
            lambda li: li.find('div', 'item-attr').text.strip(),
            lot_details
        )
        lot_props = map(
            lambda li: li.find('div', 'item-property').text.strip(),
            lot_details
        )
        lot_info = {k: v for k, v in zip(lot_attrs, lot_props)}
    finally:
        try:
            assert "Year"               in lot_info
            assert "Processing System"  in lot_info
            assert "Variety"            in lot_info
            assert "Overall"            in lot_info
            assert "Aroma / Flavor"     in lot_info
            assert "Acidity"            in lot_info
        except AssertionError:
            print(lot_info)
        return lot_info

def _get_gallery_from_farm_directory_soup(soup):
    # get gallery as a list of image urls
    # Some farm pages do not contain any images
    try:
        gallery_title = soup.find('h5', text="Gallery")
        gallery_box = _get_ancestor_tag(gallery_title, 3)
    except AttributeError:
        image_urls = []
    else:
        image_links = gallery_box.findAll('a', 'gallery-item')
        image_urls = list(map(lambda a: a['href'], image_links))
    finally:
        return image_urls

def _get_location_from_farm_directory_soup(soup):
    # get location as dict. of latitude, longitude
    try:
        location_title = soup.find('h5', text='Location')
        location_box = _get_ancestor_tag(location_title, 3)
    except:
        position = {
            'latitude': None,
            'longitude': None,
        }
    else:
        map_box = location_box.find('div', 'map')
        map_options = json.loads(map_box['data-options'])
        location = map_options['locations'][0] # multiple locations can be set
        latitude = float(location['marker_lat'])
        longitude = float(location['marker_lng'])
        position = {
            'latitude': latitude,
            'longitude': longitude,
        }
    finally:
        return position

def request_farm_directory_url(url):
    # requests from FarmConfig.farm_directory_url
    # returns dict
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        
        return {
            "description": \
                _get_description_from_farm_directory_soup(soup),
            "details": dict(
                _get_farm_information_from_farm_directory_soup(soup).items() | \
                _get_lot_information_from_farm_directory_soup(soup).items()
            ),
            "image_urls": \
                _get_gallery_from_farm_directory_soup(soup),
            "location": \
                _get_location_from_farm_directory_soup(soup),
        }
    else:
        print(response.status_code)
        return []


def _get_images_from_coe_soup(soup):
    try:
        image_box = soup.find('div', 'listing-images') or \
            soup.find('div', id='listing-images')
        image_links = image_box.findAll('a')
    except AttributeError:
        image_urls = []
    else:
        image_urls = list(map(lambda a: a['href'], image_links))
    finally:
        return image_urls

def _get_description_from_coe_soup(soup):
    description_box = soup.find('div', 'listing-description') or \
        soup.find('div', id='listing-description')
    return description_box.text

def _get_details_from_coe_soup(soup):
    details_box = soup.find('div', 'listing-details') or \
        soup.find('div', id='listing-details')
    details_attrs = map(lambda th: th.text.strip(), details_box.findAll('th'))
    details_props = map(lambda td: td.text.strip(), details_box.findAll('td'))
    return {k: v for k, v in zip(details_attrs, details_props)}

def request_coe_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        return {
            "image_urls":   _get_images_from_coe_soup(soup),
            "description":  _get_description_from_coe_soup(soup),
            "details":      _get_details_from_coe_soup(soup),
            "location": {
                'latitude': None,
                'longitude': None,
            }
        }
    else:
        print(response.status_code)
        return []


def _check_url_integrity(url):
    if url == None: return False
    # check url have no query or fragment
    url_components = urlsplit(url)
    if url_components.fragment or url_components.query:
        return False
    return True

def _get_url_origin(url):
    # find origin from the url
    url_components = urlsplit(url)
    clean_url_components = url_components \
        ._replace(path="/") \
        ._replace(scheme="https")   # handles 'http'
    return urlunsplit(clean_url_components)


def _normalize_request_url(url):
    url_components = urlsplit(url)
    if url_components.netloc == "dev.cupofexcellence.org":
        url_components = url_components\
            ._replace(netloc="cupofexcellence.org")
    if "farm-directory-2" in url_components.path:
        url_components = url_components\
            ._replace(path=url_components.path.replace(
                'farm-directory-2', 'farm-directory'
            ))
    return urlunsplit(url_components)


def crawl_farm_info_by_url(url):
    # return dict
    origin = _get_url_origin(url)

    if origin == FarmConfig.farm_directory_url:
        return request_farm_directory_url(url)

    elif origin == FarmConfig.dev_coe_url or \
        origin == FarmConfig.coe_url:
        return request_coe_url(url)
    else:
        if origin == "https://allianceforcoffeeexcellence.org/":
            return # wrong url
        raise NotImplementedError(f'Crawler for {origin} not exists')


def main():
    with open(Config.coe_normalized_json_of_info_filepath, 'r') as f:
        info = json.load(f)
    farm_info = []
    for row_dict in info:
        farm_url = row_dict['farm_link']
        print(farm_url)
        if not _check_url_integrity(farm_url): continue
        url = _normalize_request_url(farm_url)
        new_row = dict(row_dict, **crawl_farm_info_by_url(url))
        farm_info.append(new_row)
    with open(Config.coe_farm_extended_info_filepath, 'w') as f:
        json.dump(farm_info, f)
    return

if __name__ == "__main__":
    main()
