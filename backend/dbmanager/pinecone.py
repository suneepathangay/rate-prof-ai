
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer,util
import random
import uuid



class PineconeConnection:
    
    def __init__(self) -> None:
        
        self.model=SentenceTransformer(os.getenv("MODEL_NAME"))
        
        self.index=setup_index()
    
        def setup_index():
            key=os.getenv("PINECONE_KEY")
            pc=Pinecone(api_key=key)
            name=os.getenv("PINECONE_INDEX_NAME")
            index=pc.Index(name=name)
            return index
            
    
    def embed_text(self,text):
        
        return self.model.encode(text)

    
    def search(self,text):
        
        text_embedding=self.embed_text(text)
        
        self.index.query(
            vector=text_embedding,
            
            top_k=2,
            include_values=True,
            include_metadata=True
        )
        
    def insert(self,text):
        
        vector_embedding=self.embed_text(text)
        
        self.index.upsert(
            vectors=[
                {
                    "id": uuid.uuid4(), 
                    "values":vector_embedding, 
                    "metadata": {"text_name": text}
                }
            ]
        )   
        
    
    
    


if __name__=="__main__":      

    pinecone=PineconeConnection()
    