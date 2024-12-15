
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
        
        ##TODO write the code to get the null rows and then add them to missing and then return
        pass
        
                    
            
        
                    
                
    
    
    def check_fields(self,json_obj):
        print(json_obj)
        return len(json_obj["prof_names"])==0 and json_obj["hours"]=="" and json_obj["attributes"]==""
            
    
    
    