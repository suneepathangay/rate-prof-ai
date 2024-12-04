import sys
from pathlib import Path
from dotenv import load_dotenv
import os

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from pinecone_mod.pipeline import Pipeline


def main():
    
    load_dotenv()
    pipeline=Pipeline(path="../neujsondata")
    pipeline.write_json_supabase()


    
    

main()
