
from pinecone import Pinecone
from dotenv import load_dotenv
import os



def connect_pinecone():
    try:
        load_dotenv()
        
        key=os.getenv("PINECONE_API_KEY")
        name=os.getenv("PINECONE_INDEX_NAME")
        
        pc = Pinecone(api_key=key)
        index = pc.Index(name)
        return index
    except Exception as e:
        print("pinecone connection failed")

def add_vector(index):
    pass
    
connect_pinecone()

    