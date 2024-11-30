from pinecone_mod.embed import HybridEmbedder
from pinecone_mod.dataparser import Parser
import os
import numpy as np
from pinecone_mod.pineconeutil import connect_pinecone,add_vector,query_vector
##runs the full pipeline of getting the json data adding the attribute and embedding it
## the pipelin will then send these vectors to the pinecone instance

class Pipeline:
    
    def __init__(self,path,num_dimensions) -> None:
        
        self.path=path
        self.embedder= HybridEmbedder(path,num_dimensions)

    
    
    def fit_embedder(self):
        self.embedder.fit()
            
        
    def transform_data(self):
        
        self.fit_embedder()
        
        list_files=os.listdir(self.path)
        
        
        pinecone_index=connect_pinecone()
        
        if not pinecone_index:
            print("connection failed")
            return
        
        for i in range(len(list_files)):
            
            file=list_files[i]

            file_num=int(file.split("data")[1].split(".")[0])
            
            embeddings_obj=self.embedder.embed_json_file(file_num)
            
            dense_embeddings=embeddings_obj["dense_embeddings"]
            sparese_embeddings=embeddings_obj["sparse_embeddings"]
            json_objs=embeddings_obj["vector_objs"]
            
            
            
            for j in range(len(json_objs)):
                dense_vector=dense_embeddings[j].tolist()
                sparese_vector=sparese_embeddings[j]
                vector_id=self.get_vector_ide(i,j)
                json_obj=json_objs[j]
                print(json_obj['prof_name'])
                
                vecotr_obj= self.convert_vector_obj(dense_vector=dense_vector,vector_id=vector_id,json_obj=json_obj,sparse_vector=sparese_vector)
                add_vector(pinecone_index,vector_obj=vecotr_obj)
                print("vector being logged")
            
    
    def convert_vector_obj(self,dense_vector,vector_id,json_obj,sparse_vector):
        
        return [
            {
                "id":vector_id,
                "values":dense_vector,
                "metadata":json_obj,
                "sparse_values":{
                    'indices':sparse_vector['indices'],
                    'values':sparse_vector['values']
                }
            }
        ]
        
    
    def get_vector_ide(self,vector_file_num,vector_index):
        return f"vector-{vector_file_num}-{vector_index}"
        

        

    
        