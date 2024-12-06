
from database_mod.dataparser import Parser
import os
import numpy as np
import json
import sqlite3
from dotenv import load_dotenv
from database_mod.dbmanager import SupaBaseManager



##Class that contains the methods to read the json data parse it and then write it to a sqlite3 database

##The SQLite3 database will be used by the function calling agent

class Pipeline:
    
    def __init__(self,path) -> None:
        
        self.path=path
        self.parser= Parser(path=self.path)
        self.db_manager=SupaBaseManager(db_url=os.getenv("DATABASE_URL"),
                                        db_key=os.getenv("DATABASE_KEY"),
                                        table_name=os.getenv("NORTHEASTERN_TABLE"))
        
    
    def get_file_num(self,file_name:str):
        return int(file_name.split("data")[1].split(".")[0])
    
    
    def write_json_supabase(self):
        
        num_files=len(os.listdir(self.path))  
        
        for file_num in range(1,num_files+1):
            
            json_data=self.unpack_json_from_file(file_num=file_num)
            enhanced_data=self.parser.add_easiness_quality(json_data)
            for data in enhanced_data:
                self.db_manager.insert_data(data=data)
                
            

    def unpack_json_from_file(self,file_num):
        
        files=os.listdir(path=self.path)
        
        for i in range(len(files)):
            file_name=files[i]
            if self.get_file_num(file_name=file_name)==file_num:
                data=self.get_json_data_from_file(file=file_name)
                return data
    
    
    def get_json_data_from_file(self,file):
        file_path= self.path+"/"+file
        with open(file_path, 'r') as f:
            data=json.load(f)
            return data
            
    
