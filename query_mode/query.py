

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.dataparser import Parser
from pinecone_mod.embed import HybridEmbedder
from dotenv import load_dotenv
import os
from pinecone_mod.pineconeutil import get_model,query_vector,connect_pinecone



class Query:
    
    def __init__(self,path) -> None:
        self.embedder=HybridEmbedder(path=path,num_dimensions=768)
        self.embedder.fit()
        
        self.index=connect_pinecone()
        
    
    def convert_query_string(self,query_string):
        query_vectors=self.embedder.embed_query(query=query_string)
        
        query_dense=query_vectors['dense'].tolist()
        query_sparse=query_vectors['sparse']
        
        return query_dense,query_sparse

    def query(self,query_string):
        
        query_dense,query_sparse=self.convert_query_string(query_string=query_string)
        
        
        response=query_vector(index=self.index,dense_vector=query_dense,sparse_vector=query_sparse)
            
        if not response or 'matches' not in response:
            return 
            
        list_json_obj=[]
            
        for match in response['matches']:
            json_obj=match['metadata']
            list_json_obj.append(json_obj)
            
            
        for obj in list_json_obj:
            print(obj)



query=Query("../neujsondata")
query.query("What is your opinion on Gene Cooperman?")
