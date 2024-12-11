
import os
from supabase import create_client, Client
import supabase
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))
from coursicle_scrapers.rateprof import ProfessorScraper

class DbManager:
    
    def __init__(self) -> None:
        
        self.client=Client(supabase_url=os.getenv("DATABASE_URL"),supabase_key="DATABASE_KEY")
        self.table_name=os.getenv("DATBASE_NAME")
        
    
    
    
    def insert_data(self,data):
        
        try:
            self.client.table(self.table_name).insert([data]).execute()
            print("insert data successful")
            
        except Exception as e:
            print("insert data failed")
            print(e)
    
    
    def find_classes_for_professor(self,prof_name):
        ##finds all the classes for that professor
        pass
    
    
    def find_professors_for_class(self,class_name):
        pass
    
    def find_professor_info(self,prof_name):
        ##finds the data associated with that professor
        try:
            response=self.client.table(self.table_name).select("*").eq("prof_name",prof_name).execute()
                
            if len(response.data)<1:
                return None
                
            return response.data[0]
        except Exception as e:
            print("getting professor info failed")
            print(e)
    




class DbHelper:
    
    def __init__(self) -> None:
        self.prof_scraper=ProfessorScraper()

    
    def get_coursicle_data_row(self,data):
        pass
    
    def get_prof_data_row(self,data):
        pass
    
    