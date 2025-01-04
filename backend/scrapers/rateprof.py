
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class RateMyProfScraper:
    
    def __init__(self) -> None:
        pass
    
    
    def scrape(self,prof_name,school_name):
        
        review_tags=self.get_review_tags(prof_name=prof_name,school_name=school_name)
        
        
        if review_tags:
        
            comments=map(self.extract_comments_from_tag,review_tags)
            
            cleaned_comments=list(filter(lambda comment: comment!=None,comments))
            
            return cleaned_comments
        

    
    
    def extract_comments_from_tag(self, tag):
        try:
            list_tags = tag.find_all()

            for inner_tag in list_tags:
       
                class_list = inner_tag.get('class', [])
                
                for class_name in class_list:
                    if 'Comments' in class_name.split('__'):
                        return inner_tag.text
            
            return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        
        
        
    
    
    def get_review_tags(self,prof_name,school_name):
        
        prof_search_url=self.create_prof_search_url(prof_name=prof_name)
        
        
        if not prof_search_url:
            return None
        
        neu_prof_url=self.get_prof_url(prof_search_url=prof_search_url,school_name=school_name,prof_name=prof_name)
        print(neu_prof_url)
        if neu_prof_url:
            response= requests.get(url=neu_prof_url)
        
            if response.status_code==200:
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                ratings_list_container=soup.find('ul', {'id': 'ratingsList'})
                
                if ratings_list_container:
                    
                    return ratings_list_container.find_all("li")
                
            
                
        
    def create_prof_search_url(self,prof_name):
 
        try:
            first_name=prof_name.split(" ")[0]
            last_name=prof_name.split(" ")[1]
    
            url=f"https://www.ratemyprofessors.com/search/professors?q={first_name}%20{last_name}"
            
            return url
        except Exception as e:
            print(prof_name)
            print(e)

    def get_prof_url(self, prof_search_url,school_name,prof_name):
        
        response=requests.get(url=prof_search_url)
        

        
        if response.status_code==200:
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            
            if not self.validate_prof_school_name(soup=soup,school_name=school_name,prof_name=prof_name):
                return None
            
            a_tags = soup.find_all('a')
            
            for tag in a_tags:
                
                div_tags=tag.find_all("div")
                for div_tag in div_tags:
                    class_names=div_tag.get("class")
                    for class_name in class_names:
                        if class_name.split("-")[0]=="CardSchool__School":
                            if div_tag.text==school_name:
                                return "https://www.ratemyprofessors.com"+tag.get('href')
                
            
        return None
    
    
    def validate_prof_school_name(self,soup:BeautifulSoup,prof_name,school_name):
        
        prof_school_objs=self.get_prof_school_names(soup=soup)
        
        for obj in prof_school_objs:
            
            if obj:
                if obj['prof_name']==prof_name and obj['school_name']==school_name:
                    return True
        
        return False
            
    
    
    ##method to validate that we are getting the reviews for the proper professor at northeastern
    def get_prof_school_names(self,soup:BeautifulSoup):
        
        tags=soup.find_all()
        
        school_names=[]
        prof_names=[]
        
        for tag in tags:
            
            class_list = tag.get('class', [])
            
            for class_name in class_list:
                
                if "CardSchool__School" in class_name.split("-"):
                    school_names.append(tag.text)
                if "CardName__StyledCardName" in class_name.split("-"):
                    prof_names.append(tag.text)
         
        
        size_list=min(len(school_names),len(prof_names))
        
        def create_prof_school_obj(i):
            
            return {"prof_name":prof_names[i],"school_name":school_names[i]}
        
        prof_school_objs=[create_prof_school_obj(i) for i in range(size_list)]
        
        return prof_school_objs
        
        
    


