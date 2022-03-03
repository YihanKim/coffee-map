import os
from urllib.parse import \
    urljoin, \
    urlsplit

### Configurations

basedir = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(basedir, 'data')

class Config(object):
    # includes configurations with some constants

    # CoE / ACE urls
    ace_website_url = 'https://allianceforcoffeeexcellence.org/'
    coe_website_url = 'https://cupofexcellence.org/'
    coe_results_url = urljoin(coe_website_url, "/competition-auction-results/")
    ace_results_url = urljoin(ace_website_url, "/competition-auction-results/")
    ace_website_url_components = urlsplit(ace_website_url)
    coe_website_url_components = urlsplit(coe_website_url)
    coe_dict_of_containers_filepath = os.path.join(
            datadir,
            "coe_dict_of_containers.pickle"
    )
    ace_dict_of_containers_filepath = os.path.join(
            datadir,
            "ace_dict_of_containers.pickle"
    )
    coe_json_of_info_filepath = os.path.join(
            datadir,
            "coe_competition.json"
    )
    coe_normalized_json_of_info_filepath = os.path.join(
            datadir,
            "coe_normalized_competition.json"
    )
    coe_competition_table_names = {"Winning Farms", "Winning Farms*"}
    image_filedir = os.path.join(datadir, 'images')


class FarmConfig(object):
    # available farm_url origins
    # 'https://cupofexcellence.org/?post=219228&action=edit' - wrong address
    _farm_url_origins = [
        'https://farmdirectory.cupofexcellence.org/',
        'https://dev.cupofexcellence.org/',
        'https://cupofexcellence.org/',
    ]
    farm_directory_url, \
    dev_coe_url, \
    coe_url = _farm_url_origins

class DjangoConfig(object):
    secret_key = 'django-insecure-+e97zysl4td5_ukrmv$polhmzgd)&%(3f48exzkgq_7o@evry2'
