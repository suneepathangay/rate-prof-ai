
import os
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from dbmanager.dbmanager import DbManager

class PipeLine:
    
    def __init__(self,path) -> None:
        self.path=path
        
        self.db_manager=DbManager()
        
    def load_coursicle_data(self):
        
        list_files=os.listdir(self.path)
        
        for file_name in list_files:
            
            data=self.get_json(file_name=file_name)
            
    
    
    def parse_data(self):
        pass
            
            
            
    
    def get_json(self,file_name):
        
        with open(file=self.path+"/"+file_name, mode="r") as file:
            data = json.load(file)
            return data
            
        