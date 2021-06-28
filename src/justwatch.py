# %%


# packages needed
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium import webdriver
import regex as re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

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
print(type(driver))

driver.get(url)
sleep(2)
request = driver.page_source.encode("utf-8")

soup = BeautifulSoup(request, "html.parser")



def collect_all_while_scrolling():

    # get the timeline
    timeline = soup.find(class_ = "timeline").find_all(class_= re.compile("timeline__provider-block timeline__timeframe--"))
    timeline_driver = driver.find_element_by_class_name("timeline")
    time_items_driver = timeline_driver.find_elements_by_class_name("timeline__provider-block")

    content_library = []

    counter = 0

    for time_item in timeline:
        
        nr_releases = time_item.get_text().split(" ")[1]
        nr_scrols = round(int(nr_releases)/8)
        date = time_item.attrs["class"][1][21:31]
        service = time_item.find("img").attrs["alt"]
        print(f"There are {nr_releases} on {date} for service {service}. Need to scroll {nr_scrols} times..")
        
        scrolled = 0
        
        while scrolled <= nr_scrols:
            
            titles = time_item.find_all("a")

            for item in range(len(titles)):

                if item < 8:
                    try:
                        item_url = titles[item].attrs["href"]
                    except:
                        print(f"Didn't work out for {titles[item]}")

                if item > 7:
                        print('Scrolling to the left to collect more titles')
                        element_to_hover_over = time_items_driver[counter]
                        hover = ActionChains(driver).move_to_element(element_to_hover_over)
                        hover.perform()
                        sleep(2)
                        scroll = time_items_driver[counter].find_element_by_class_name("hidden-horizontal-scrollbar__nav")  
        
                        scroll.click()
                        scrolled += 1
                        break    
                
                content_library.append({"service": service,
                                        "date": date,
                                        "nr_releases": nr_releases,
                                        "url": base_url + item_url})

            scrolled += 1 
        
        print(content_library)
        counter += 1 
              
    return(content_library)
# %%
