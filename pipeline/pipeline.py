##this class is the data pipeline to get the coursicle data and then get the rate my professor data


import sys
from pathlib import Path
import time
from dotenv import load_dotenv
sys.path.append(str(Path(__file__).resolve().parent.parent))
from scrapers.coursicle import CoursicleScraper
from scrapers.rateprof import RateMyProfScraper
from dbmanager.dbmanager import DBManager

class Pipeline:
    
    def __init__(self) -> None:
        
        load_dotenv("../.env")
        
        self.coursicle=CoursicleScraper(school_name="NEU")
        self.rate_prof=RateMyProfScraper()
        self.db_manager=DBManager()
    
    
    def populate_class_data(self):
        self.coursicle.init_class_categories()
        self.coursicle.get_classes_per_category()
    
    def run(self):
        
       # self.populate_class_data()
        
        ##writes all the class data to the class database
        self.populate_prof_data()
        
        
    
    def get_prof_names(self):
        
        list_profs=[]
        
        list_prof_objs=self.db_manager.get_all_profs()

        
        for prof_obj in list_prof_objs:
            prof_names=prof_obj['prof_names']
            for name in prof_names.split(", "):
                list_profs.append(name)
        return list_profs
    
    
    
    def populate_prof_data(self):
        
        prof_names=self.get_prof_names()
        
        for i in range(len(prof_names)):
            
            prof_name=prof_names[i]
            comments=self.rate_prof.scrape(prof_name=prof_name,school_name="Northeastern University")
            
            comments_str=""
            if comments:
                comments_str=" ".join(comments)
                
            prof_data={"prof_name":prof_name,"reviews": comments_str}
            self.db_manager.write_prof_data(data=prof_data)
            
            time.sleep(5)
        
        
        
        
        
        
        

p=Pipeline()
p.run()

        
        