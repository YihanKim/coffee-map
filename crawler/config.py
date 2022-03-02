import os
from urllib.parse import \
    urljoin, \
    urlsplit

### Configurations

basedir = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(basedir, 'data')

class Config():
    ace_website_url = 'https://allianceforcoffeeexcellence.org/'
    coe_website_url = 'https://cupofexcellence.org/'
    ace_website_url_components = urlsplit(ace_website_url)
    coe_website_url_components = urlsplit(coe_website_url)
    coe_results_url = urljoin(coe_website_url, "/competition-auction-results/")
    ace_results_url = urljoin(ace_website_url, "/competition-auction-results/")
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
