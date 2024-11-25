from sentence_transformers import SentenceTransformer, util
from pinecone_mod.dataparser import Parser
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize

class Embedder:
    def __init__(self, path, num_dimensions) -> None:
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.path = path
        self.parser = Parser(path=self.path)
        self.num_dimensions = num_dimensions
        
    def fit(self, json_objects):
        """
        Store the feature names for consistent embedding generation.
        """
        df = pd.DataFrame(json_objects)
        self.feature_names = df.columns.tolist()
    
    def embed_json_file(self, json_file_num):
        """
        Load JSON file and embed all objects within it.
        """
        data = self.parser.load_json(json_file_num)
        enhanced_data = self.parser.add_easiness_quality(data=data)
        
        embeddings = [self.embed_json_obj(obj) for obj in enhanced_data]
        return embeddings
    
    def embed_json_obj(self, json_obj):
        """
        Create a combined embedding for all text fields in the JSON object.
        
        Strategy:
        1. Concatenate all text values with their keys for context
        2. Generate embedding using SentenceTransformer
        3. Normalize the embedding for cosine similarity
        """
        # Combine all text fields with their keys for context
        text_parts = []
        
        for key in self.feature_names:
            if key in json_obj and json_obj[key]:
                # Include both key and value for context
                text_parts.append(f"{key}: {str(json_obj[key])}")
        
        # Combine all text parts with spaces
        combined_text = " ".join(text_parts)
        
        # Generate embedding
        if combined_text.strip():
            embedding = self.model.encode(combined_text)
            # Normalize for cosine similarity
            normalized_embedding = normalize(embedding.reshape(1, -1))
            return normalized_embedding.flatten()
        else:
            # Return zero vector if no text is present
            return np.zeros(self.model.get_sentence_embedding_dimension())
        
         
         
         
        


