
import os
import json
from supabase import Client
import json
from dotenv import load_dotenv

class DBManager:
    
    def __init__(self,path) -> None:
        self.path=path
        self.client=Client(supabase_url=os.getenv("DATABASE_URL"),supabase_key=os.getenv("DATABASE_KEY"))
        
    def construct_prof_row(self,prof_name):
        
        
        return_obj={"prof_name":prof_name}
        
        prof_data=self.get_data_from_supa(prof_name=prof_name)
        #reviews avalible for this professor
        if prof_data:
            return_obj['classes']=prof_data['classes']
            return_obj['comments']=prof_data['comments']
            return_obj['quality']=prof_data['quality']
            return_obj['difficulty']=prof_data['difficulty']
        
        
        
            
    def get_json(self,file_name):
        with open(self.path+"/"+file_name, "r") as file:
                data = json.load(file)
                return data

    
    
    ##method to get professor data from the supabase
    def get_prof_data_from_supa(self,prof_name):
        try:
            response=self.client.table(os.getenv("NORTHEASTERN_TABLE")).select("*").eq("prof_name",prof_name).execute()
            print(response)
        except Exception as e:
            print(e)
        
    
    def insert_class_data_obj(self,data):
        
        try:
            self.client.table(os.getenv("NORTHEASTERN_CLASS_TABLE")).insert([data]).execute()
        except Exception as e:
            print(e)
    
    
    
    def write_json_data_to_data_obj(self,path):
        
        files=os.listdir("../neujsondata")
        
        
        
        for file in files:
            
            if file.endswith(".git") or file.endswith(".txt"):
                continue
            
            json_data=self.get_json(file_name=file)[0]

            
            for key in json_data:
                row_json={}
                row_json['class']=file+key
                row_json['prof_names']=", ".join(json_data[key]['prof_names'])
                row_json['hours']=json_data[key]['hours']
                row_json['attributes']=json_data[key]['attributes']
            
                self.insert_class_data_obj(data=row_json)
            
            
    
    def get_json(self,file_name):
        with open(self.path+"/"+file_name, "r") as file:
                data = json.load(file)
                return data
            
        
      
 