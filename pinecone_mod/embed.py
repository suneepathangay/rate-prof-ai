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
        Returns list of embedding vectors, one for each object to preserve meaning.
        """
        data = self.parser.load_json(json_file_num)
        enhanced_data = self.parser.add_easiness_quality(data=data)
        
        # Embed each object separately to preserve individual meanings
        embeddings = [self.embed_json_obj(obj) for obj in enhanced_data]
        return embeddings
    
    def embed_json_obj(self, json_obj):
        """
        Create an embedding vector for a single JSON object.
        Preserves the semantic meaning of the object's content.
        """
        text_parts = []
        
        for key in self.feature_names:
            if key in json_obj and json_obj[key]:
                # Include both key and value for context
                text_parts.append(f"{key}: {str(json_obj[key])}")
        
        combined_text = " ".join(text_parts)
        
        if combined_text.strip():
            # Get embedding while preserving semantic meaning
            embedding = self.model.encode(combined_text, convert_to_numpy=True)
            # Normalize while keeping semantic relationships
            normalized_embedding = embedding / np.linalg.norm(embedding)
            return normalized_embedding
        else:
            return np.zeros(self.model.get_sentence_embedding_dimension())