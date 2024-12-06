from supabase import create_client, Client
import supabase


class SupaBaseManager:
    
    def __init__(self,db_url,db_key,table_name) -> None:
        
        self.client=Client(supabase_url=db_url,supabase_key=db_key)
        self.table_name=table_name

    
    def insert_data(self,data):
        try:
            self.client.table(self.table_name).insert([data]).execute()
            print("insert data successful")
            
        except Exception as e:
            print("insert data failed")
            print(e)
    
    def find_classes_for_professor(self,prof_name):
        ##finds all the classes for that professor
        try:
            
            return self.find_professor_info(prof_name=prof_name)['classes']
                
        except Exception as e:
            print("failed to find classes for professor")
            print(e)
    
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

    
    def find_professors_for_class(self,class_name):
        
        professor_objs=[]
        ##finds the quality professors for a class
        response=self.client.table(self.table_name).select("*").range(0, 15000).execute()
        print(len(response.data))
        
        for r in response.data:
            classes=[cl.strip() for cl in r['classes'].split(",")]
            if class_name in classes:
                professor_objs.append(r)
        return professor_objs
                
    
    