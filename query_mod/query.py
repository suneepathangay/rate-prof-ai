

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.dataparser import Parser
from rapidfuzz import process
from customgpt_client import CustomGPT


class Query:
    
    def __init__(self) -> None:
        pass
    
    
    def query(self,query_string):
        pass

        
        
    

query=Query()
query.query("Which teacher is best for CS3500")

##