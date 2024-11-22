from sentence_transformers import SentenceTransformer, util


class Embedder:
    
    def __init__(self,path) -> None:

        self.model=SentenceTransformer('all-MiniLM-L6-v2')
        
        self.path=path
        
    def embed_data(self):
         ##first we need create an instance of the parser class
         pass
         
        


