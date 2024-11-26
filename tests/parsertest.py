
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.dataparser import Parser
from pinecone_mod.embed import Embedder
from pinecone_mod.pipeline import Pipeline



def load_json_test():
    
    path="../neujsondata"
    
    parser=Parser(path=path)
    data=parser.load_json(1)
    mapped_data=parser.add_easiness_quality(data=data)
    print(mapped_data)



def embedder_test():
    
    path="../neujsondata"
    
    embedder=Embedder(path=path,num_dimensions=384)
    
    embedder.embed_json_file(1)


def pipeline_test():
    
    pipeline=Pipeline(path="../neujsondata",num_dimensions=384)
    test_embedding=pipeline.transform_data()
    
    
            


pipeline_test()