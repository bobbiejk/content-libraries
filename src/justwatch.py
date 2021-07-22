# packages needed
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium import webdriver
import regex as re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def scroll():

    scrolled = 0
    
    while True:

        print(f'Preparing to scroll..')
        element_to_hover_over = time_items_driver[counter].find_element_by_class_name("hidden-horizontal-scrollbar")
        hover = ActionChains(driver).move_to_element(element_to_hover_over)
        hover.perform()
        print(f'Hovering over element..')
        try:
            scroll = time_items_driver[counter].find_element_by_class_name("hidden-horizontal-scrollbar__nav--right") 
            scroll.click()
            print(f'Succesfully scrolled to the left for the {scrolled+1}th time..') 
        except:
            print("End of the list reached, no need to scroll further..")
            return

        sleep(2)

        scrolled = scrolled + 1

    return 

def collect_titles(time_item, time_items_driver, timeline):

    content_library = []
    
    # number of releases on that day
    nr_releases = time_item.get_text().split(" ")[1]

    date = time_item.attrs["class"][1][21:31]
    service = time_item.find("img").attrs["alt"]
    print(f'On {date}, {service} released {nr_releases} titles..')

    collected_titles = 0

    while collected_titles != int(nr_releases):

        print("woo")

        scroll()

        request = driver.page_source.encode("utf-8")
        soup = BeautifulSoup(request, "html.parser")
        timeline = soup.find(class_ = "timeline").find_all(class_= re.compile("timeline__provider-block timeline__timeframe--"))
        timeline_driver = driver.find_element_by_class_name("timeline")
        time_items_driver = timeline_driver.find_elements_by_class_name("timeline__provider-block")
            
        titles = time_items_driver[counter].find_elements_by_class_name("horizontal-title-list__item") 
        collected_titles = len(titles)
    

    for title in titles:
        print(title.get_attribute("href"))

    for item in range(int(nr_releases)):

        print(item)

        item_url = titles[item].get_attribute("href")
            
        content_library.append({"service": service,
                                "date": date,
                                "nr_releases": nr_releases,
                                "url": base_url + item_url})
 
              
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
    driver.maximize_window()
    driver.get(url)
    sleep(10)
    request = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(request, "html.parser")

    #scroll_page()
    #request = driver.page_source.encode('utf-8')
    #soup = BeautifulSoup(request, "html.parser")

    # get the timeline
    timeline = soup.find(class_ = "timeline").find_all(class_= re.compile("timeline__provider-block timeline__timeframe--"))
    timeline_driver = driver.find_element_by_class_name("timeline")
    time_items_driver = timeline_driver.find_elements_by_class_name("timeline__provider-block")

    counter = 0

    for time_item in timeline:
        
        content_library = collect_titles(time_item, time_items_driver, timeline)
        append_csv(content_library)
        counter += 1 

    driver.quit()

