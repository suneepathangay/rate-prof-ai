from pathlib import Path
from dotenv import load_dotenv
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from dbmanager.dbmanager import DBManager
import os
import json
import traceback
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from prompt import extract_query_terms_prompt, function_calling_prompt

class FuncCall:
    def __init__(self) -> None:
        load_dotenv()
        self.db_manager = DBManager()
        self.llm = self.setup_openai()

    def extract_key_words_query(self, query):
        prompt = PromptTemplate(
            input_variables=["query_string"],
            template=extract_query_terms_prompt()
        )
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({"query_string": query})
            return json.loads(response.content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {"prof_name": [], "course_name": []}
        except Exception as e:
            print(f"Error extracting terms: {e}")
            return {"prof_name": [], "course_name": []}

    def match_query_function(self, query, keywords_obj):
        
        
        prompt = PromptTemplate(
            input_variables=["user_query", "keywords"],
            template=function_calling_prompt()
        )
        
        
        chain = prompt | self.llm
        
        
        try:
            
            response = chain.invoke({
                "user_query": query,
                "keywords": json.dumps(obj=keywords_obj)
            })
            print(response.content)
            json_objs=json.loads(response.content)
            
            return self.execute_function_calling(json_objs=json_objs)
        
        except Exception as e:
            print(f"Error matching functions: {e}")
            traceback.print_exc()
            return []

    def get_class_data(self, class_name):
        return self.db_manager.get_classes_data(class_name=class_name)
    
    def get_prof_reviews(self, prof_name):
        return self.db_manager.get_prof_data(prof_name=prof_name)
    
    def get_classes_for_prof(self, prof_name):
        return self.db_manager.get_classes_prof(prof_name=prof_name)

    def setup_openai(self):
        return ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo"
        )
    

    def map_function(self,function_name,parameter):
        
        if function_name=="get_class_data":
            return self.get_class_data(class_name=parameter)
        if function_name=="get_prof_reviews":
            return self.get_prof_reviews(prof_name=parameter)
        if function_name=="get_classes_for_prof":
            return self.get_classes_for_prof(prof_name=parameter)
        return None

    def filter_json_function_calling(self,obj):
        
        if "function_name" in obj and "parameter" in obj:
            return True
        return False
    
    def execute_function_calling(self,json_objs):
        
        filtered_json_objs=filter(self.filter_json_function_calling,json_objs)
        
        mapped_data = [
            self.map_function(obj["function_name"], obj["parameter"]) for obj in filtered_json_objs
        ]
        
        return mapped_data
                
    

            
    
f=FuncCall()
query_string="what does that mf Gene Cooperman teach?"
keywords=f.extract_key_words_query(query=query_string)

raw_json=f.match_query_function(query=query_string,keywords_obj=keywords)
print(raw_json)


#Which classes does Ben Lerner teach?
#Does Ben Lerner teach CS3500?
#What are the reivews for Gene Cooperman? 
#What are the timings for CS3000?
#Who is the best professor for DS4400?
#What are the timings for ENGL1450?
#What NUPath requirements does GEO4300 satisfy?