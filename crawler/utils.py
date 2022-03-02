import pickle
from bs4 import \
    BeautifulSoup as bs
from urllib.parse import \
    urlsplit, \
    urlunsplit
from config import \
    Config

### URLs

def _normalize_url(
    url,
    origin_url_components
):
    # replace url's origin(scheme + netloc) as url of from_components
    url_components = urlsplit(url)
    url_components = url_components\
        ._replace(scheme = origin_url_components.scheme)\
        ._replace(netloc = origin_url_components.netloc)
    normalized_url = urlunsplit(url_components)
    return normalized_url

def normalize_coe_url(url):
    return _normalize_url(url,
        origin_url_components=Config.coe_website_url_components
    )

def normalize_ace_url(url):
    return _normalize_url(url,
        origin_url_components=Config.ace_website_url_components
    )

def get_country_and_year_from_url(url):
    # return name of a country and competition year from the url

    # To handle brazil-naturals-2015-january
    url = url.replace('2015-january', '2015_january')
    # To handle costa-rica-coe-2017
    url = url.replace('costa-rica-coe', 'costa-rica')

    # extract path from the url (remove origins)
    path = urlsplit(url).path
    # the path contains some slash characters
    # at the beginning and at the end, hence they should be stripped out
    stripped_path = path.strip('/')

    # capitalization
    titled_path = stripped_path.title()

    # To prevent to split costa-rica,only split rightmost one hyphen
    # with replacing all hyphens as blank
    country, year = titled_path.replace("-", ' ').rsplit(' ', 1)

    # Note: Costa rica(north / south), Brazil(naturals / pulped naturals)
    # had multiple CoE competitions by region or coffee processing.
    return (country, year)


### Pickles

def read_bs_container_dict(filename):
    text_to_bs = lambda text: bs(text, 'html.parser')
    with open(filename, 'rb') as f:
        return {k:text_to_bs(v) for k, v in pickle.load(f)}

def write_bs_container_dict(container_dict, filename):
    with open(filename, 'wb') as f:
        pickle.dump([(k, str(v)) for k, v in container_dict.items()], f)
