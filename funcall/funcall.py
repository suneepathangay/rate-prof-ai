##this class has the methods for the LLM to interact wiht

import sys
from pathlib import Path
from dotenv import load_dotenv
sys.path.append(str(Path(__file__).resolve().parent.parent))
from dbmanager.dbmanager import DBManager
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
import json
from prompt import extract_query_terms_prompt, function_calling_prompt, craft_response_prompt


class FuncCall:

    def __init__(self) -> None:
        
        load_dotenv()
        
        self.db_manager=DBManager()
        self.llm=self.setup_openai()
        
    
    def get_data(self,query):
        pass
    
    
    def extract_key_words_query(self,query):
        
    
        
        
        prompt = PromptTemplate(
            input_variables=["query_string"],
            template=extract_query_terms_prompt("")
        )
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({"query_string": query})
            
            json_data = json.loads(response.content)
            
            return json_data
        
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {"professor": "", "course": ""}
        except Exception as e:
            print(f"Error extracting terms: {e}")
            return {"professor": "", "course": ""}
    
    def get_class_data(self,class_name):
        pass
    
    def get_prof_data(self,prof_name):
        pass
    
    def pass_data_to_model(self,data):
        pass
    
    def setup_openai(self):
        chat = ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo"
        )
        return chat
    
    def get_llm(self):
        return self.llm

    def validate_query_req(self,query_json):
        if 'query' not in query_json:
            return False
        return True