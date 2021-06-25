# packages needed
from bs4 import BeautifulSoup
from time import sleep
import requests
import selenium

# get url to scrape from
base_url = "https://www.justwatch.com" 
location_url = "/us/"
provider_url = "new?providers="

service_keys = {"amazon":"amp",
                "apple":"atp",
                "disney":"dnp",
                "discovery":"dpu",
                "hbo":"hbm",
                "hulu":"hlu",
                "netflix":"nfx"}

service_abbreviations = service_keys.keys()

service_url = "" 
for service in service_abbreviations:
    service_url = service_url + "," + service

url = base_url + location_url + provider_url + service_url

# set up selenium
driver = webdriver.Chrome()

driver.get(url)
sleep(2)
request = driver.page_source.encode("utf-8")
soup = BeautifulSoup(request, "html.parser")

