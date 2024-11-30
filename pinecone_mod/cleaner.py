import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class AdvancedPreprocessor:
    def __init__(self, language='english'):
        # Download necessary NLTK resources
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()
    
    def preprocess(self, text):
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = text.split()
        
        # Remove stop words and lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stop_words
        ]
        
        # Rejoin processed tokens
        return ' '.join(processed_tokens)