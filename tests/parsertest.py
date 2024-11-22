
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.dataparser import Parser



def load_json_test():
    
    path="../neujsondata"
    
    parser=Parser(path=path)
    data=parser.load_json(1)
    mapped_data=parser.add_easiness_quality(data=data)
    print(mapped_data)


load_json_test()