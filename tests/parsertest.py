
import sys
from pathlib import Path
import os

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.dataparser import Parser
from pinecone_mod.pipeline import Pipeline
from query_mod.query import Query



def load_json_test():
    
    path="../neujsondata"
    
    parser=Parser(path=path)
    data=parser.load_json(1)
    mapped_data=parser.add_easiness_quality(data=data)
    print(mapped_data)


    


def pipeline_test():
    
    pipeline=Pipeline(path="../neujsondata")
    
    
            
