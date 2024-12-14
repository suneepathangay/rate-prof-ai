
import sys
from pathlib import Path

from dotenv import load_dotenv
sys.path.append(str(Path(__file__).resolve().parent.parent))
import traceback
from scrapers.coursicle import CoursicleScraper
from scrapers.validate_scraper import Validator



def run_main():
    try: 
        
        load_dotenv(dotenv_path="../.env")
        s=CoursicleScraper(school_name="NEU")
        
 
        s.get_classes_per_category()
             
    except Exception as e:
        traceback.print_exc()
        print(e)



def run_validate():
    

        validator=Validator(path="../neujsondata")
        missing_classes=validator.validate()

        
        s=CoursicleScraper(path="../neujsondata")
        
        s.fill_missing(missing_classes=missing_classes)

        
def cleanup():
    s=CoursicleScraper(path="../neujsondata")
    s.write_custom_link(category_url="https://www.coursicle.com/neu/courses/CS/")
    
run_main()