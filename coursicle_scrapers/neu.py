
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time







class CoursicleScraper:
    
    def __init__(self) -> None:
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_class_categories(self):
        
        self.driver.get("https://www.coursicle.com/neu/courses/")
        time.sleep(5)
        
        container_node=self.driver.find_element(by=By.ID, value="tileContainer")
        
        list_course_cats=container_node.find_elements(by=By.CLASS_NAME, value="tileElement")
        
        return [course_cat.get_attribute('href') for course_cat in list_course_cats][:-1]
    
    def get_classes_per_category(self,list_categories:str):
        
        category_map={}
        
        for i in range(0,2):
            
            link=list_categories[i]
            
            href_name=link.split("/")[-2]
            
            class_map_info=self.get_classes(link=link)
            category_map[href_name]=class_map_info
            self.driver.back()
            time.sleep(5)
        
        return category_map
            
    
    def get_classes(self,link):
        
        self.driver.get(link)
        time.sleep(5)
        
        container_node = self.driver.find_element(by=By.ID, value="tileContainer")
        classes=container_node.find_elements(by=By.CLASS_NAME,value="tileElement")
        
        class_map={}
        
        for c in classes:
            href=c.get_attribute('href')
            link=href
            href_name=href.split("/")[-2]
            
            
            class_info=self.get_class_info(link=link)
            class_map[href_name]=class_info
            self.driver.back()
            time.sleep(5)
        return class_map
            
            
    
    def get_class_info(self,link):
        
        return_obj={}
        
        self.driver.get(link)
        time.sleep(5)
                
        return_obj['prof_names']=self.get_prof_names()
        return_obj['hours']=self.get_class_timings()
        return_obj['attributes']=self.get_nu_path()

        
        return return_obj
            
        
    def get_prof_names(self):
        try:
            
            prof_names_container=self.driver.find_elements(by=By.CLASS_NAME, value="professorLink")
            
            if prof_names_container:
                
                prof_names=[]
                
                for name_container in prof_names_container:
                    prof_names.append(name_container.text)
                    
                return prof_names
            
            return []

        except:
            return []
    
    def get_class_timings(self):
        
        try:
            class_timings_container=self.driver.find_element(by=By.ID, value="subItemTypicallyHeld")
        
            if class_timings_container:
                
                sub_container=class_timings_container.find_element(by=By.CLASS_NAME, value="subItemContent")
                
                if sub_container:
                    
                    hours=sub_container.find_element(by=By.CLASS_NAME, value="subItemContent").text

                    return hours
            
            return ""
        except:
            return ""
    
    def get_nu_path(self):
        
        try:
        
            attributes_container=self.driver.find_element(by=By.ID, value="subItemAttributes")
            
            
            if attributes_container:
                
                attributes=self.driver.find_element(by=By.CLASS_NAME, value="subItemContent").text
                
                return attributes

            return ""
        
        except:
            return ""

            
                    
         
        
        
        
        
            
        
        
        
            
            
    
    


s=CoursicleScraper()
cats=s.get_class_categories()
class_cat_map=s.get_classes_per_category(list_categories=cats)

print(class_cat_map)