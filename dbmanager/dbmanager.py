
import os
import json
from supabase import Client
import json
import traceback


class DBManager:
    
    def __init__(self) -> None:
        self.client=Client(supabase_url=os.getenv("DATABASE_URL"),supabase_key=os.getenv("DATABASE_KEY"))
        

    
    def insert_class_data_obj(self,data):
        
        try:
            self.client.table(os.getenv("NORTHEASTERN_CLASS_TABLE")).insert([data]).execute()
        except Exception as e:
            traceback.print_exc()
            print(e)
    
    
    
    def write_json_data_to_data_obj(self,json_data,file_name):

        for key in json_data:
                row_json={}
                row_json['class']=file_name+key
                row_json['prof_names']=", ".join(json_data[key]['prof_names'])
                row_json['hours']=json_data[key]['hours']
                row_json['attributes']=json_data[key]['attributes']
            
                self.insert_class_data_obj(data=row_json)
    
    
    def get_all_profs(self):
        try:
            return self.client.table(os.getenv("NORTHEASTERN_CLASS_TABLE")).select("prof_names").execute().data

        except Exception as e:
            print(e)
            traceback.print_exc()
            
        
      
 