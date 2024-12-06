
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from database_mod.dataparser import Parser
from database_mod.pipeline import Pipeline
from query_mod.query import Query
from database_mod.dbmanager import SupaBaseManager




def load_json_test():
    
    path="../neujsondata"
    
    parser=Parser(path=path)
    data=parser.load_json(1)
    mapped_data=parser.add_easiness_quality(data=data)
    print(mapped_data)




def find_classes_test():
    
    load_dotenv()
     
    db_manager=SupaBaseManager(db_url=os.getenv("DATABASE_URL"),
                                        db_key=os.getenv("DATABASE_KEY"),
                                        table_name=os.getenv("NORTHEASTERN_TABLE"))
     
    data=db_manager.find_classes_for_professor(prof_name="Benjamin Lerner")
    print(data)

def find_prof_per_class():
    load_dotenv()
    db_manager=SupaBaseManager(db_url=os.getenv("DATABASE_URL"),
                                        db_key=os.getenv("DATABASE_KEY"),
                                        table_name=os.getenv("NORTHEASTERN_TABLE"))
    
    data=db_manager.find_professors_for_class(class_name="CS3500")
    print(data)
    
    

find_prof_per_class()
            
