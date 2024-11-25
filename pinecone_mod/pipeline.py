from pinecone_mod.embed import Embedder
from pinecone_mod.dataparser import Parser
import os
##runs the full pipeline of getting the json data adding the attribute and embedding it

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
            enhanced_data = self.parser.add_easiness_quality(data=json_objs)
            for obj in enhanced_data:
                list_objs.append(obj)
        
        return list_objs
    
    def fit_embedder(self):
        
        list_json_objs=self.get_sample()
        
        self.embedder.fit(list_json_objs)
            
        
    def transform_data(self):
        
        self.fit_embedder()
        
        list_files=os.listdir(self.path)
        
        list_embeddings=[]
        
        for file in list_files:
            file_num=file.split("data")[1].split(".")[0]
            
            list_embeddings.append(self.embedder.embed_json_file(file_num))
        
        return list_embeddings 
