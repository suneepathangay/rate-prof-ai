from neu import SchoolScraper
from prof import ProfessorScraper
from collections import defaultdict
import os
import json
import time

def main_test():
    
    BATCH_SIZE=10
    
    school_scraper=SchoolScraper()
    prof_names=school_scraper.scrape_prof_names()
    
    batch_map=create_batch_map(BATCH_SIZE,prof_names)
    
    #list of failed keys that we can take a closer look at
    failed_keys=[]
   
    for key in batch_map:
        try:
            prof_names=batch_map[key]
            process(prof_names=prof_names,school_scraper=school_scraper,key=key)
            time.sleep(30)
        except Exception as e:
            print(e)
            failed_keys.append(key)
            
            

def create_batch_map(batch_size,rate_prof_list):
    print(len(rate_prof_list))
    
    map_batch_num_links=defaultdict(set)
    
    prev=0
    batch_num=0
    for i in range(0,len(rate_prof_list),batch_size):
        for j in range(prev,i):
            map_batch_num_links[batch_num].add(rate_prof_list[j])
        batch_num+=1
        prev=i

    return map_batch_num_links
            
        
def process(prof_names:list,school_scraper:SchoolScraper,key):
    
    prof_neu_page_links=school_scraper.get_prof_page_links(prof_names=prof_names)
    
    prof_ratemy_links=school_scraper.scrape_prof_links(prof_page_links=prof_neu_page_links)
    
    ratemy_neu_map=dict()
    
    for prof_link,page_link in zip(prof_ratemy_links,prof_neu_page_links):
        ratemy_neu_map[prof_link]=page_link
    
    test_review_data=[]
    
    for link in prof_ratemy_links:
        neu_page_link=ratemy_neu_map[link]
        prof_scraper=ProfessorScraper(link,neu_page_link)
        review_data=prof_scraper.scrape()
        test_review_data.append(review_data)
    
    write_data_json(test_review_data,key)

def write_data_json(test_review_data,key):
    
    des_path='../neujsondata'
    file_name=f"data{key}.json"
    
    full_dest_path=os.path.join(des_path,file_name)
    
    ##cd to a direcotry called data and then begin writing the data to there
    with open(full_dest_path, "w") as file:
        json.dump(test_review_data, file, indent=4) 

main_test()


    