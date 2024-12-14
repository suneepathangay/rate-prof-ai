
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))

from coursicle_scrapers.coursicle import CoursicleScraper
from coursicle_scrapers.validate_scraper import Validator



def run_main():
    try: 
    
        s=CoursicleScraper(path="../neujsondata")
        list_cats=s.load_cats_from_txt()
        ##only run this once 
        # cats=s.get_class_categories()
        # s.write_cats_to_txt(list_cats=cats)
        s.get_classes_per_category()
        
        
        # print(s.offset) 
        #print(list_cats)        
    except Exception as e:
        print(e)



def run_validate():
    

        validator=Validator(path="../neujsondata")
        missing_classes=validator.validate()

        
        s=CoursicleScraper(path="../neujsondata")
        
        s.fill_missing(missing_classes=missing_classes)

        
def cleanup():
    s=CoursicleScraper(path="../neujsondata")
    s.write_custom_link(category_url="https://www.coursicle.com/neu/courses/CS/")
    

run_validate()