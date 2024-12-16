##this class has the methods for the LLM to interact wiht

import sys
from pathlib import Path
from dotenv import load_dotenv
sys.path.append(str(Path(__file__).resolve().parent.parent))
from dbmanager.dbmanager import DBManager
from langchain_openai import ChatOpenAI
import os


class FuncCall:

    def __init__(self) -> None:
        
        load_dotenv()
        
        self.db_manager=DBManager()
        self.llm=self.setup_openai()
        
    
    def get_data(self,query):
        pass
    
    
    def extract_key_words_query(self,query):
        pass
    
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
