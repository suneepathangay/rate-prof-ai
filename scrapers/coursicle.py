
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
import os
import sys
from pathlib import Path
import traceback
from dotenv import load_dotenv, set_key


project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from dbmanager.dbmanager import DBManager







class CoursicleScraper:
    
    def __init__(self,school_name) -> None:
        
        load_dotenv('.env')
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.school_name=school_name
        
        self.env_key = f"{self.school_name}_OFFSET"
        
        
        self.offset=self.load_offset()
        self.db_manager=DBManager()

    def init_class_categories(self):
        
        self.driver.get("https://www.coursicle.com/neu/courses/")
        time.sleep(5)
        
        container_node=self.driver.find_element(by=By.ID, value="tileContainer")
        
        list_course_cats=container_node.find_elements(by=By.CLASS_NAME, value="tileElement")
        
        self.cats=[course_cat.get_attribute('href') for course_cat in list_course_cats][:-1]
    
    def get_classes_per_category(self):
        
        
        for i in range(self.offset,len(self.cats)):
            
            link=self.cats[i]
            
            href_name=link.split("/")[-2]
            
            try:
                class_map_info=self.get_classes(link=link)
                self.db_manager.write_json_data_to_data_obj(json_data=class_map_info,file_name=href_name)
                print(class_map_info,href_name)
                self.offset += 1
                self.write_offset()
                self.driver.back()
                time.sleep(5)
            except Exception as e:
                print("captcha caught me rip.")
                print(e)
                time.sleep(25)
                ##setting the offset back to the value
                self.write_offset()
                break
                
           
            
    
    def get_classes(self,link):
        
        self.driver.get(link)
        time.sleep(5)
        
        container_node = self.driver.find_element(by=By.ID, value="tileContainer")
        classes=container_node.find_elements(by=By.CLASS_NAME,value="tileElement")
        
        class_map={}
        
        for c in classes:
            href=c.get_attribute('href')
            if href:
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
            traceback.print_exc()
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
            traceback.print_exc()
            return ""
    
    def get_nu_path(self):
        
        try:
        
            attributes_container=self.driver.find_element(by=By.ID, value="subItemAttributes")
            
            
            if attributes_container:
                
                attributes=self.driver.find_element(by=By.CLASS_NAME, value="subItemContent").text
                
                return attributes

            return ""
        
        except:
            traceback.print_exc()
            return ""

    
    def load_offset(self):
        """Load offset value from environment variable."""
        offset = os.getenv(self.env_key)
        if offset is None:
            self.write_offset(0)  # Initialize to 0 if not found
            return 0
        print(f"Loaded OFFSET: {offset}")  # Debugging line
        return int(offset)
    
    def write_offset(self, value=None):
        """Update offset in environment and persist it to .env file."""
        if value is not None:
            self.offset = value  # Update the in-memory value of the offset
        os.environ[self.env_key] = str(self.offset)  # Update in-memory environment variable
        set_key(".env", self.env_key, str(self.offset))  # Persist the updated offset in the .env file
        print(f"Updated OFFSET: {self.offset}")
    
    def fill_missing(self,missing_classes):
        try:
            for url in missing_classes:
                file_name=url.split("/")[5]
                json_data=self.get_class_info(url)
                self.db_manager.write_json_data_to_data_obj(json_data=json_data,file_name=file_name)
                time.sleep(5)
        except Exception as e:
            traceback.print_exc()
            print(e)
    
    
    ##backup method for when I fuck up and rewrite data by accident
    def write_custom_link(self,category_url):
        
        file_name=category_url.split("/")[5]
        
        class_map_info=self.get_classes(link=category_url)
        
        self.db_manager.write_json_data_to_data_obj(json_data=class_map_info,file_name=file_name)
        
        
        
        



        
        
        
        
    
        
        
        
