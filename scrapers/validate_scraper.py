
import os
import json
import sys
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from dbmanager.dbmanager import DBManager

class Validator:
    
    def __init__(self) -> None:
        
        self.db_manager=DBManager()
    
    
    def validate(self):
        
        missing_classes=[]

        
        list_files=os.listdir(self.path)
        
        for file_name in list_files:
            
            if file_name.endswith(".txt") or file_name.endswith(".git"):
                continue
            
            
            json_data=self.get_json(file_name=file_name)[0]
            
            
            
            
            for class_name,val in json_data.items():
                print(file_name)
                if self.check_fields(json_obj=val):
                    url=f"https://www.coursicle.com/neu/courses/{file_name}/{class_name}"
                    missing_classes.append(url)
        
        return missing_classes
                    
            
        
                    
                
    
    
    def check_fields(self,json_obj):
        print(json_obj)
        return len(json_obj["prof_names"])==0 and json_obj["hours"]=="" and json_obj["attributes"]==""
            
    
    
    def get_json(self,file_name):
        with open(self.path+"/"+file_name, "r") as file:
                data = json.load(file)
                return data
    
    