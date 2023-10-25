import sys
import project
from unittest.mock import patch
import requests
from bs4 import BeautifulSoup
import re
from requests_file import FileAdapter



def test_get_search_term():
    testargs = ["project.py", "honda", "vfr"]
    with patch.object(sys, "argv", testargs):
        assert project.get_search_term() == "https://www.olx.ro/oferte/q-honda-vfr"


# Use FileAdapte from requests_file in order to be able to use requests on a file from computer
s = requests.Session()
s.mount('file://', FileAdapter())
resp = s.get("file:////workspaces/124591255/project/test_project.html")
soup = BeautifulSoup(resp.content, "html.parser")

def test_olx_get_ad_id():
    assert project.olx_get_ad_id(soup) == 254378874

def test_olx_get_ad_post_date():
    assert project.olx_get_ad_post_date(soup) == "16 octombrie 2023"

def test_olx_get_ad_title():
    assert project.olx_get_ad_title(soup) == "Honda vfr800 vtec 2002"

def test_olx_get_ad_price_and_currency():
    assert project.olx_get_ad_price_and_currency(soup) == ("15912", "lei")

def test_olx_get_ad_seller_info():
    assert project.olx_get_ad_seller_info(soup) == ("marius", "aprilie 2013")

def test_olx_get_ad_description():
    assert project.olx_get_ad_description(soup) == "description"










