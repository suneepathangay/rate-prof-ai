
import sys
from pathlib import Path
import os

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.dataparser import Parser
from pinecone_mod.embed import HybridEmbedder
from pinecone_mod.pipeline import Pipeline


def get_sample(path):
        
    parser=Parser(path=path)
    
    json=parser.load_json(1)
    cleaned_json=parser.add_easiness_quality(json)
    
    return cleaned_json
    
    
    


def load_json_test():
    
    path="../neujsondata"
    
    parser=Parser(path=path)
    data=parser.load_json(1)
    mapped_data=parser.add_easiness_quality(data=data)
    print(mapped_data)



def embedder_test():
    
    path="../neujsondata"
    
    embedder=HybridEmbedder(path=path,num_dimensions=384)
    
    
    sample_json_data=get_sample(path=path)
    
    embedder.fit(sample_json_data)
    
    dense_embedding=embedder.embed_json_file(1)
    
    


def pipeline_test():
    
    pipeline=Pipeline(path="../neujsondata",num_dimensions=768)
    pipeline.transform_data()
    
            

def query_test():
    
    path="../neujsondata"
    parser=Parser(path=path)