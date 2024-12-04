from supabase import create_client, Client
import supabase


class SupaBaseManager:
    
    def __init__(self,db_url,db_key,table_name) -> None:
        
        self.client=Client(supabase_url=db_url,supabase_key=db_key)
        self.table_name=table_name

    
    def insert_data(self,data):
        try:
            response=self.client.table(self.table_name).insert([data]).execute()
            print("insert data successful")
            
        except Exception as e:
            print("insert data failed")
            print(e)
    
    