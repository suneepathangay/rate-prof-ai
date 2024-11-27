import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.pipeline import Pipeline
from pinecone_mod.dataparser import Parser

def main():
    pipeline=Pipeline(path="../neujsondata",num_dimensions=384)
    pipeline.transform_data()
    

main()