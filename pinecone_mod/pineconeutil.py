
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer, util



def connect_pinecone():
    try:
        load_dotenv()
        
        key=os.getenv("PINECONE_API_KEY")
        name=os.getenv("PINECONE_INDEX_NAME")
        
        pc = Pinecone(api_key=key)
        index = pc.Index(name)
        return index
    except Exception as e:
        print("pinecone connection failed {}",e)
        return None

def add_vector(index,vector_obj):
    try:
        load_dotenv()
        index.upsert(
            vectors=vector_obj,
            namespace= os.getenv("PINECONE_INDEX_NAME")
        )
    except Exception as e:
        print("vector insert failed {}",e)
    
def query_vector(index,dense_vector,sparse_vector):
    try:
        load_dotenv()
        response = index.query(
        namespace=os.getenv("PINECONE_INDEX_NAME"),
        vector=dense_vector,
        sparse_vector=sparse_vector,
        top_k=5,
        include_values=True,
        include_metadata=True,
        )
        return response
    except Exception as e:
        print("vector query failed {}",e)
        return None


def get_model():
    load_dotenv()
    return SentenceTransformer(os.getenv("MODEL_NAME"))