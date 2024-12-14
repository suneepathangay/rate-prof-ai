##this class is the data pipeline to get the coursicle data and then get the rate my professor data
from scrapers.coursicle import CoursicleScraper
from dotenv import load_dotenv


class Pipeline:
    
    def __init__(self) -> None:
        
        self.coursicle=CoursicleScraper()