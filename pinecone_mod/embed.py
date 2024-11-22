from sentence_transformers import SentenceTransformer, util
from pinecone_mod.dataparser import Parser
from pinecone_mod.macro import QualityLevel, DifficultyLevel


class Embedder:
    
    def __init__(self,path) -> None:

        self.model=SentenceTransformer('all-MiniLM-L6-v2')
        
        self.path=path
        
        self.parser=Parser(path=self.path)
        
    def embed_json_file(self,json_file_num):
        #embed each json object in the json file
        #to embed we can follow the previous embedding plan of embedding each feature
        data=self.parser.load_json(json_file_num)
        enchanced_data=self.parser.add_easiness_quality(data=data)
        
        d=enchanced_data[0]
        
        name=d['prof_name']
        classes=d['classes']
        comments=d['comments']
        
        quality=d[QualityLevel.TYPE.value].value
        difficulty=d[DifficultyLevel.TYPE.value].value
        
    
    
    def embed_feature(self):
        pass
        
        
        
        
         
         
         
        


