# packages needed
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium import webdriver
import regex as re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import os
import csv
import math

os.chdir("S:/content-libraries")

try:
    os.makedirs("data")
    print("Directory has been created")
except FileExistsError:
    print("Directory already exists")

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

def scroll_page():

    scroll_pause  = 0.5

    # get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            # try to remove the error of the max entries 
            break

        sleep(scroll_pause)

        # calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_pause = scroll_pause + 0.1
        print(scroll_pause)

    return("Scrolled to end..")

def collect_titles():

    content_library = []
        
    nr_releases = time_item.get_text().split(" ")[1]
    nr_scrols = math.ceil((int(nr_releases)/8))
    date = time_item.attrs["class"][1][21:31]
    service = time_item.find("img").attrs["alt"]

    if nr_scrols > 1:
        print(f"There are {nr_releases} on {date} for service {service}. Need to scroll {nr_scrols-1} times..")
    
    scrolled = 0
    
    while scrolled < nr_scrols:
        
        titles = time_item.find_all(class_="horizontal-title-list__item") 

        if len(titles) > 8:
            range_len = 9
        else:
            range_len = len(titles)

        for item in range(range_len):

            if item < 8:
                try:
                    print(f"Collecting title {item+scrolled*8+1}...")
                    item_url = titles[item].attrs["href"]
                except:
                    print(f"Didn't work out for {titles[item]}")

            if item > 7:
                print(f'Preparing to scroll..')
                element_to_hover_over = time_items_driver[counter].find_element_by_class_name("hidden-horizontal-scrollbar")
                hover = ActionChains(driver).move_to_element(element_to_hover_over)
                hover.perform()
                print(f'Hovering over element..')
                scroll = time_items_driver[counter].find_element_by_class_name("hidden-horizontal-scrollbar__nav--right") 
                print(scroll) 
                scroll.click()
                print(f'Succesfully scrolled to the left for the {scrolled+1}th time..') 

                scrolled += 1
                sleep(2)
            
            content_library.append({"service": service,
                                    "date": date,
                                    "nr_releases": nr_releases,
                                    "url": base_url + item_url})

        scrolled += 1 
              
    return(content_library)

def append_csv(content_library):

    if os.path.isfile("data/content_library.csv") == False:
        with open("data/content_library.csv", "a", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["service", "date", "nr_releases", "url"])
    
    with open("data/content_library.csv", "a", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for content in content_library:
            writer.writerow([content["service"], content["date"], content['nr_releases'], content['url']])

    return

service_abbreviations = service_keys.values()

for service in service_abbreviations:

    url = base_url + location_url + provider_url + service

    # set up selenium
    driver = webdriver.Chrome()

    driver.get(url)
    sleep(10)
    request = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(request, "html.parser")

    scroll_page()
    request = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(request, "html.parser")

    # get the timeline
    timeline = soup.find(class_ = "timeline").find_all(class_= re.compile("timeline__provider-block timeline__timeframe--"))
    timeline_driver = driver.find_element_by_class_name("timeline")
    time_items_driver = timeline_driver.find_elements_by_class_name("timeline__provider-block")

    counter = 0

    for time_item in timeline:
        
        content_library = collect_titles()
        append_csv(content_library)
        counter += 1 

    driver.quit()

