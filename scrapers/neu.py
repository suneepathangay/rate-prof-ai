from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
import sys
from pathlib import Path
from util import set_json
from bs4 import BeautifulSoup
import requests
import time

sys.path.append(str(Path(__file__).resolve().parent.parent))
from customexecptions.customs import FailedSoupInit,ElementNotFound, PageNotFound


class SchoolScraper:
    
    def __init__(self) -> None:
        
        self.url="https://catalog.northeastern.edu/general-information/faculty/#a6511813"
        self.teach_card_tags=set_json("classtags.json")["teacher_card"]
        
        self.domain_name="https://www.ratemyprofessors.com"
        
        
        

    #gets html
    def get_html(self):
        
        html=requests.get(self.url).text
        return html
    
    #scrapes to find the name of all the profs at northeastern    
    def scrape_prof_names(self):
        
        html=self.get_html()
        
        soup = BeautifulSoup(html, 'html.parser')
        
        prof_tag_arr=soup.find_all(class_="keeptogether")
        
        prof_names=[]
        
        for tag in prof_tag_arr:
            name=tag.strong.get_text(strip=True)
            prof_names.append(name)
        
        return prof_names
    
    
    #takes all the prof names and generates rate my prof search query
    def get_prof_page_links(self,prof_names):
        
        queries=[]
        
        for name in prof_names:
            name=name.split(" ")
            
            first_name=name[0]
            last_name=name[-1]
            
            
            query=f"https://www.ratemyprofessors.com/search/professors/696?q={first_name}%20{last_name}"
            queries.append(query)
        return queries
                
    
    ##takes a url from list above and generates a rate my professor page link
    def scrape_prof_link(self,url):
        
        test="https://www.ratemyprofessors.com/search/professors/696?q=Hongyang%20Zhang"
        
        response=requests.get(url)
        
        if response.status_code==200:
            
            soup=BeautifulSoup(response.text,"html.parser")

            currNode=None
            
            list_index=len(self.teach_card_tags)-1
            
            for i in range(len(self.teach_card_tags)-1):
                name=self.teach_card_tags[i]["name"]
                types=self.teach_card_tags[i]["type"]
                
                if types=="class":
                    if not currNode:
                        currNode=soup.find(class_=name)
                    else:
                        currNode=currNode.find(class_=name)

                else:
                    if not currNode:
                        currNode=soup.find(id=name)
                    else:
                        currNode=currNode.find(id=name)
            
            final_tag_name=self.teach_card_tags[list_index]["name"]
            final_tag_type=self.teach_card_tags[list_index]["type"]
            
            if final_tag_type=="class":
                if len(currNode.find_all(class_=final_tag_name)) > 0:
                    return currNode.find_all(class_=final_tag_name)[0].get("href")
                else:
                    raise ElementNotFound
            else:
                if len(currNode.find_all(class_=final_tag_name)) > 0:
                    return currNode.find_all(id=final_tag_name)[0].get("href")
                else: 
                    raise ElementNotFound
        else:
            raise PageNotFound 
    
    #takes rate my professor page links and then scrapes for the ratings        
    def scrape_prof_links(self,prof_page_links):
        
        prof_rate_links=[]
        
        for prof_link in prof_page_links:
            try:
                prof_href=self.scrape_prof_link(prof_link)
                prof_rate_links.append(self.domain_name+prof_href)
                
                time.sleep(3) ##avoid spamming with requests
            
            except Exception as e:
                print(str(e))
        
        return prof_rate_links
    
    
    
        
    
        
        
        
        
        
        
            
school_scraper=SchoolScraper()

prof_names=school_scraper.scrape_prof_names()

prof_links=school_scraper.get_prof_page_links(prof_names)



    
            
        
        
        
        
        
    