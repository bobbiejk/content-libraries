# Scrape content libraries from JustWatch

This repository contains code to collect the titles released on certain dates for pre-specified streaming services from dynamic site JustWatch. The dynamic site allows the scraper to scroll down untill no further data can be obtained.* JustWatch will never allow you to view all titles after ~4years. JustWatch only shows the titles that are still on the streaming services at the time of scraping. Therefore, you do not obtain the entire historical content library of a streaming service.

\* There is a bug in the code that may cause early termination of the data collection process per service. Check your collected data to check whether this is a problem for your wanted timeperiod. 

## Running instructions

1. Alter the streaming services collected

The data collected is for a pre-specified list of streaming services. The default services that are collected are Amazon, Apple, Disney, Discovery, HBO, Hulu and Netflix. In order to change the streaming services collected, go to the script and add or delete services in the service_keys dictionary. The dictionary keys resemble the different streaming services, whereas the dictionary values.

2. Configure Python for web scraping

In order to run the script provided, both ChromeDriver and Selenium are needed to be installed on your computer. For installation instructions, I'd recommend the following links: 
- ChromeDriver installation instructions: [Install ChromeDriver | Tilburg Science Hub](https://tilburgsciencehub.com/building-blocks/configure-your-computer/task-specific-configurations/configuring-python-for-webscraping/)
- Selenium installation instructions: [Install Selenium | Tilburg Science Hub](https://tilburgsciencehub.com/building-blocks/collect-data/webscraping-apis/scrape-dynamic-websites/)

3. Fork this repository 

A fork is a copy of a repository that allows you to freely experiment with changes without affecting the original project. By forking, you can change the script however you'd like to fit your own project needs.

