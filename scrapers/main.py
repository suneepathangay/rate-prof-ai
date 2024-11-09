from neu import SchoolScraper
from prof import ProfessorScraper


class Main:
    
    def __init__(self) -> None:
        pass
    
    def main(self):
        school_scraper=SchoolScraper()
        
        prof_names=school_scraper.scrape_prof_names()
        
        prof_neu_page_links=school_scraper.get_prof_page_links(prof_names=prof_names)
        
        prof_ratemy_links=school_scraper.scrape_prof_links(prof_page_links=prof_neu_page_links)
        
        for link in prof_ratemy_links:
            
            prof_scraper=ProfessorScraper(link)
        
        
            prof_scraper.scrape()
