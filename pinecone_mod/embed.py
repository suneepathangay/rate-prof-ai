from sentence_transformers import SentenceTransformer, util
from pinecone_mod.dataparser import Parser
from pinecone_mod.pineconeutil import get_model
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

class HybridEmbedder:
    def __init__(self, path, num_dimensions):
        # Dense embedding model
        self.dense_model = get_model()
        self.path = path
        self.parser = Parser(path=self.path)
        self.num_dimensions = num_dimensions
        
        # Sparse vector (TF-IDF) components
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000  # Limit number of features
        )
    
    def fit(self):
        """
        Prepare feature names and fit TF-IDF vectorizer
        """
        json_objects=self.parser.get_sample()
        
        df = pd.DataFrame(json_objects)
        self.feature_names = df.columns.tolist()
        
        # Prepare text for TF-IDF fitting
        text_corpus = self._create_text_corpus(json_objects)
        self.tfidf_vectorizer.fit(text_corpus)
    
    def _create_text_corpus(self, json_objects):
        """
        Create a corpus of text from JSON objects for TF-IDF
        """
        text_corpus = []
        for obj in json_objects:
            text_parts = []
            for key in self.feature_names:
                if key in obj and obj[key]:
                    if key in ['classes', 'comments']:
                        text_parts.extend(str(item) for item in obj[key])
                    else:
                        text_parts.append(str(obj[key]))
            text_corpus.append(" ".join(text_parts))
        return text_corpus
    
    def embed_json_file(self, json_file_num):
        """
        Generate both dense and sparse embeddings for a JSON file
        """
        data = self.parser.load_json(json_file_num)
        enhanced_data = self.parser.add_easiness_quality(data=data)
        
        ##over here add method to construct new json object that doesnt contain comments for embeddings
        vector_json_obj=self.get_vector_json_objs(json_objs=enhanced_data)
        
        
        # Embed each object with both dense and sparse representations
        embeddings = []
        sparse_embeddings = []
        
        for obj in enhanced_data:
            dense_emb = self.embed_json_obj(obj)
            sparse_emb = self.create_sparse_embedding(obj)
            
            embeddings.append(dense_emb)
            sparse_embeddings.append(sparse_emb)
        
        return {
            "dense_embeddings": embeddings,
            "sparse_embeddings": sparse_embeddings,
            "vector_objs": enhanced_data
        }
    
    def embed_json_obj(self, json_obj):
        """
        Create a dense embedding vector for a single JSON object
        """
        text_parts = []
        for key in self.feature_names:
            if key in json_obj and json_obj[key]:
                if key in ['classes', 'comments']:
                    text_parts.extend(str(item) for item in json_obj[key])
                else:
                    text_parts.append(str(json_obj[key]))
        
        combined_text = " ".join(text_parts)
        
        if combined_text.strip():
            # Get embedding while preserving semantic meaning
            embedding = self.dense_model.encode(combined_text, convert_to_numpy=True)
            # Normalize while keeping semantic relationships
            normalized_embedding = embedding / np.linalg.norm(embedding)
            return normalized_embedding
        else:
            return np.zeros(self.dense_model.get_sentence_embedding_dimension())
    
    def create_sparse_embedding(self, json_obj):
        """
        Create a sparse TF-IDF embedding for a JSON object
        """
        text_parts = []
        for key in self.feature_names:
            if key in json_obj and json_obj[key]:
                if key in ['classes', 'comments']:
                    text_parts.extend(str(item) for item in json_obj[key])
                else:
                    text_parts.append(str(json_obj[key]))
        
        combined_text = " ".join(text_parts)
        
        if combined_text.strip():
            # Convert to sparse TF-IDF representation
            tfidf_vector = self.tfidf_vectorizer.transform([combined_text])
            
            # Convert to dictionary format for Pinecone sparse vectors
            indices = tfidf_vector.indices.tolist()
            values = tfidf_vector.data.tolist()
            
            return {
                'indices': indices,
                'values': values
            }
        else:
            return {'indices': [], 'values': []}
    
    def embed_query(self, query):
        """
        Generate both dense and sparse embeddings for a query
        """
        # Dense embedding
        dense_embedding = self.dense_model.encode(query, convert_to_numpy=True)
        normalized_dense = dense_embedding / np.linalg.norm(dense_embedding)
        
        # Sparse embedding
        tfidf_vector = self.tfidf_vectorizer.transform([query])
        
        # Convert to dictionary format for Pinecone sparse vectors
        sparse_embedding = {
            'indices': tfidf_vector.indices.tolist(),
            'values': tfidf_vector.data.tolist()
        }
        
        return {
            'dense': normalized_dense,
            'sparse': sparse_embedding
        }
    
    def get_vector_json_obj(self,json_objs):
        
        vector_json_obj=[]
        
        for obj in json_objs:
            
            new_obj={}
            for key in obj:
                if key!='comments':
                    new_obj[key]=obj[key]
            vector_json_obj.append(new_obj)
        return vector_json_obj
    