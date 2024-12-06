from enum import Enum

class DifficultyLevel(Enum):
    EASY = "easy level difficulty"
    MEDIUM = "medium level difficulty"
    HARD = "hard level difficulty"
    
    UNKNOWN="unknown level of difficulty"
    
    TYPE = "difficulty"

class QualityLevel(Enum):
    LOW = "low level quality"
    DECENT = "medium level quality"
    GOOD = "good level quality"
    
    UNKNOWN="unknown level of quality"
    
    TYPE="quality"
