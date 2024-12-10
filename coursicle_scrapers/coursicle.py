import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from pynput.keyboard import Key, Controller


class CoursicleScraper:
    
    def __init__(self) -> None:
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=chrome_options)

    
    


    
    
    



scraper=CoursicleScraper()
print(scraper.scrape())
    