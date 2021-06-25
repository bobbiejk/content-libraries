# %%


# packages needed
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium import webdriver
import regex as re


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

service_abbreviations = service_keys.values()

service_url = "" 
for service in service_abbreviations:
    service_url = service_url + service

    if service != "nfx":
        service_url = service_url + ","

url = base_url + location_url + provider_url + service_url

# set up selenium
driver = webdriver.Chrome()

driver.get(url)
sleep(2)
request = driver.page_source.encode("utf-8")

soup = BeautifulSoup(request, "html.parser")

# get the timeline
timeline = soup.find(class_ = "timeline").find_all(class_= re.compile("timeline__provider-block timeline__timeframe--"))

content_library = []

for time_item in timeline:
    
    nr_releases = time_item.get_text().split(" ")[1]
    nr_scrols = int(nr_releases)/8
    date = time_item.attrs["class"][1][21:31]
    service = time_item.find("img").attrs["alt"]
    
    scrolled = 0
    
    while scrolled <= nr_scrols:
        
        titles = time_item.find_all("a")

        for item in titles:
            try:
                item_url = item.attrs["href"]
            except:
                print('Scrolling to the left to collect more titles')
                scroll = driver.find_element_by_class_name("hidden-horizontal-scrollbar__nav")  
                print(scroll)          
                scroll.click()
                scrolled += 1
                break            
        
        content_library.append({"service": service,
                                "date": date,
                                "nr_releases": nr_releases,
                               "url": base_url + item_url})
        
        
        
print(content_library)



# %%
