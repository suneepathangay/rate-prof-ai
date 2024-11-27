

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.dataparser import Parser
from pinecone_mod.embed import Embedder
from dotenv import load_dotenv
import os
from pinecone_mod.pineconeutil import get_model,query_vector,connect_pinecone


class Query:
    
    def __init__(self) -> None:
        self.model=get_model()
        self.index=connect_pinecone()
    
    def query_pinecone(self,query_string):
        
        load_dotenv()
        
        query_vector_arr=self.convert_query_string(query_string=query_string).tolist()
        
        response=query_vector(index=self.index,query_vector=query_vector_arr)
        
        if not response or 'matches' not in response:
            return 
        
        for match in response['matches']:
            json_obj=match['metadata']
            print(json_obj)
        
        
    
    def convert_query_string(self,query_string):
        return self.model.encode(query_string,convert_to_numpy=True)
    

query=Query()
query.query_pinecone("What teachers teach OOD?")