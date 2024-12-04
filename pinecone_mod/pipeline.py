
from pinecone_mod.dataparser import Parser
import os
import numpy as np
import json
import sqlite3
from dotenv import load_dotenv
from pinecone_mod.sqlscripts import create_table_script,insert_data_script,select_data


##Class that contains the methods to read the json data parse it and then write it to a sqlite3 database

##The SQLite3 database will be used by the function calling agent

class Pipeline:
    
    def __init__(self,path,table_name) -> None:
        
        load_dotenv()
        
        self.path=path
        self.parser= Parser(path=self.path)
        
        self.db_path=self.get_db_path()
        
        self.connection=sqlite3.connect(self.db_path)
        self.cursor=self.connection.cursor()
        self.table_name=table_name
    
    def get_db_path(self):
        general_path= os.path.abspath(os.path.join(os.getcwd(), '..'))
        return os.path.join(general_path,os.getenv("DATABASE_NAME"))
    
    def set_table_up(self):
        try:
            self.cursor.execute(create_table_script(table_name=self.table_name))
        except:
            print("table creation failed")
    
    def get_file_num(self,file_name):
        return int(file_name.split("data")[1].split(".")[0])
    
    
    def write_json_data_sqlite(self,data):
        try:
            prof_name=data['prof_name']
            classes=', '.join(data['classes']) 
            comments=' | '.join(data['comments'])
            difficulty=data['difficulty']
            quality=data['quality']
            
            insert_script = insert_data_script(
                table_name=self.table_name,
                professor_name="professor_name",  # Ensure column names match the table structure
                classes="classes",
                comments="comments",
                difficulty="difficulty",
                quality="quality"
            )
            
            self.cursor.execute(
                insert_script,(prof_name, classes, comments, difficulty, quality)
            )
            self.connection.commit() 
            print("insert successful")
        except:
            print("insert data failed")
            
    def write_json_to_sqlite(self):
        
        num_files=len(os.listdir(self.path))
        
        for file_num in range(1,num_files+1):
            json_data=self.unpack_json_from_file(file_num=file_num)
            transfomed_data=self.parser.add_easiness_quality(data=json_data)
            for data in transfomed_data:
                self.write_json_data_sqlite(data=data)
            
            

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
            
    
    def check_data(self):
        self.cursor.execute(select_data(self.table_name))
        return self.cursor.fetchall()
