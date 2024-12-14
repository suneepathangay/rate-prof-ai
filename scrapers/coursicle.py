
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
import os







class CoursicleScraper:
    
    def __init__(self,path) -> None:
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.path=path
        self.offset=self.load_offset()
        self.cats=self.load_cats_from_txt()

    def get_class_categories(self):
        
        self.driver.get("https://www.coursicle.com/neu/courses/")
        time.sleep(5)
        
        container_node=self.driver.find_element(by=By.ID, value="tileContainer")
        
        list_course_cats=container_node.find_elements(by=By.CLASS_NAME, value="tileElement")
        
        return [course_cat.get_attribute('href') for course_cat in list_course_cats][:-1]
    
    def get_classes_per_category(self):
        
        
        for i in range(self.offset,len(self.cats)):
            
            link=self.cats[i]
            
            href_name=link.split("/")[-2]
            
            try:
                class_map_info=self.get_classes(link=link)
                self.write_json(file_name=href_name,data=class_map_info,class_id=None)
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


    def write_json(self, file_name, data,class_id):
        
        file_path = os.path.join(self.path, file_name)

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []
        
        existing_data[0][class_id]=data

        with open(file_path, "w") as file:
            json.dump(existing_data, file, indent=4)

        

    def write_cats_to_txt(self,list_cats):
        
        file_path = os.path.join(self.path, "categories.txt")
    
        # Write the list to the file
        with open(file_path, "w") as file:
            for category in list_cats:
                file.write(f"{category}\n")
    
    def load_cats_from_txt(self):
        # Define the file path
        file_path = os.path.join(self.path, "categories.txt")
        
        # Read the file and load the data into a list
        with open(file_path, "r") as file:
            list_cats = [line.strip() for line in file]  # Remove any trailing newline characters
        return list_cats
    
    def load_offset(self):
        ##load the number from txt
        file_path = os.path.join(self.path, "offset.txt")
        
        with open(file_path, "r") as file:
            offset = int(file.read().strip())  # Read and strip any whitespace or newline
            return offset
    
    def write_offset(self):
        file_path = os.path.join(self.path, "offset.txt")
        with open(file_path, "w") as file:
            file.write(f"{self.offset}\n") 
    
    def fill_missing(self,missing_classes):
        try:
            for url in missing_classes:
                file_name=self.path+"/"+url.split("/")[5]
                
                class_id=url.split("/")[6]
                
                json_data=self.get_class_info(url)
                self.write_json(file_name=file_name,data=json_data,class_id=class_id)
                time.sleep(5)
        except Exception as e:
            print(e)
    
    
    ##backup method for when I fuck up and rewrite data by accident
    def write_custom_link(self,category_url):
        
        file_name=category_url.split("/")[5]
        
        class_map_info=self.get_classes(link=category_url)
        self.write_json(file_name=file_name,data=class_map_info)
        
        
        
        
        
        
        


        
        
        
        
    
        
        
        
