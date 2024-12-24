
import os
from supabase import Client
import traceback
from dotenv import load_dotenv


class DBManager:
    
    def __init__(self) -> None:
        load_dotenv()
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
            
    
    def write_prof_data(self,data):
        
        try:
            if data['reviews']!="":
                self.client.table(os.getenv("NORTHEASTERN_PROF_TABLE")).insert([data]).execute()
        
        except Exception as e:
            print(e)
            traceback.print_exc()
    
    def get_classes_data(self,class_name):
        try:
            return self.client.table(os.getenv("NORTHEASTERN_CLASS_TABLE")).select("*").eq("class",class_name).execute().data
      
        except Exception as e:
            print(e)
            traceback.print_exc()
    
    def get_prof_data(self,prof_name):
        try:
            return self.client.table(os.getenv("NORTHEASTERN_PROF_TABLE")).select("*").eq("prof_name",prof_name).execute().data
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            
    
    def get_classes_prof(self,prof_name):
        
        def filter_for_prof(prof_name,obj):
            if obj['prof_names']:
                prof_names=obj['prof_names'].split(", ")
                
                if prof_name in prof_names:
                    return True
                return False
        
        try:
            
            
            list_profs=self.client.table(os.getenv("NORTHEASTERN_CLASS_TABLE")).select("*").execute().data
            
            list_class_objs=list(filter(
                lambda obj: filter_for_prof(prof_name, obj), 
                list_profs
            ))
            
            return [obj['class'] for obj in list_class_objs]
            
        
        except Exception as e:
            print(e)
            traceback.print_exc()

    
        

