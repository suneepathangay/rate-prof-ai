from pinecone_mod.embed import Embedder
from pinecone_mod.dataparser import Parser
import os
import numpy as np
from pinecone_mod.pineconeutil import connect_pinecone,add_vector,query_vector
##runs the full pipeline of getting the json data adding the attribute and embedding it
## the pipelin will then send these vectors to the pinecone instance

class Pipeline:
    
    def __init__(self,path,num_dimensions) -> None:
        
        self.path=path
        self.embedder= Embedder(path,num_dimensions)
        self.parser= Parser(path=self.path)
    
    
    def get_sample(self):
        
        list_objs=[]
        list_files=os.listdir(self.path)
        sample_size=0.1
        
        for i in range(1,int(len(list_files)*sample_size)):
            
            json_objs=self.parser.load_json(i)
            filtered_json_objs=filter(self.is_not_null,json_objs)
            enhanced_data = self.parser.add_easiness_quality(data=filtered_json_objs)
            for obj in enhanced_data:
                list_objs.append(obj)
        
        return list_objs
    
    def fit_embedder(self):
        
        list_json_objs=self.get_sample()
        
        self.embedder.fit(list_json_objs)
            
        
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
            
            vectors_obj=self.embedder.embed_json_file(file_num)
            vectors_file_arr=vectors_obj["embeddings"]
            json_file_arr=vectors_obj["vector_objs"]
            
            
            for j in range(len(vectors_file_arr)):
                vector_arr=vectors_file_arr[j].tolist()
                vector_id=self.get_vector_ide(i,j)
                json_obj=json_file_arr[j]
                print(json_obj['prof_name'])
                
                vecotr_obj= self.convert_vecotr_obj(vector_arr=vector_arr,vector_id=vector_id,json_obj=json_obj)
                add_vector(pinecone_index,vector_obj=vecotr_obj)
                print("vector being logged")
            
    
    def convert_vecotr_obj(self,vector_arr,vector_id,json_obj):
        return [{
            "id":vector_id,
            "values":vector_arr,
            "metadata":json_obj
        }]
    
    def get_vector_ide(self,vector_file_num,vector_index):
        return f"vector-{vector_file_num}-{vector_index}"
        
    def is_not_null(self,json_obj):
        if json_obj:
            return True
        return False
        

    
        