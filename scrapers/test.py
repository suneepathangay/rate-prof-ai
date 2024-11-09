from neu import SchoolScraper
from prof import ProfessorScraper
import requests
import json


def main_test():
    school_scraper=SchoolScraper()
    prof_names=school_scraper.scrape_prof_names()[:6]
    
    prof_neu_page_links=school_scraper.get_prof_page_links(prof_names=prof_names)
    
    prof_ratemy_links=school_scraper.scrape_prof_links(prof_page_links=prof_neu_page_links)
    
    ratemy_neu_map=dict()
    
    ##creating the map for links
    for prof_link,page_link in zip(prof_ratemy_links,prof_neu_page_links):
        ratemy_neu_map[prof_link]=page_link
    
    test_review_data=[]

    for link in prof_ratemy_links:
        neu_page_link=ratemy_neu_map[link]
        prof_scraper=ProfessorScraper(link,neu_page_link)
        review_data=prof_scraper.scrape()
        test_review_data.append(review_data)
    print(test_review_data)
    
    with open("data.json", "w") as file:
        json.dump(test_review_data, file, indent=4) 




    
    