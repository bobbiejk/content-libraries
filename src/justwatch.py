# packages needed
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium import webdriver
import regex as re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

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

def scroll_page():

    scroll_pause  = 0.5

    # get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(scroll_pause)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_pause = scroll_pause + 0.005

    return("Scrolled to end..")

def collect_titles():

    content_library = []
        
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
              
    return(content_library)

def append_csv(content_library = content_library):

    if os.path.isfile("data/content_library.csv") == False:
        with open("data/content_library.csv", "a", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["service", "date", "nr_releases", "url"])
    
    with open(dirname+filename_csv, "a", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for content in content_library:
            writer.writerow([content["service"], content["date"], content['nr_releases'], content['url']])

    return

# scroll to the end of the page
scroll_page()

# get the timeline
timeline = soup.find(class_ = "timeline").find_all(class_= re.compile("timeline__provider-block timeline__timeframe--"))
timeline_driver = driver.find_element_by_class_name("timeline")
time_items_driver = timeline_driver.find_elements_by_class_name("timeline__provider-block")

counter = 0

for time_item in timeline:
    
    content_library = collect_titles()
    append_csv(content_library)
    counter += 1 
