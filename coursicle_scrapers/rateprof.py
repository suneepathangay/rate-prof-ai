
import requests
from bs4 import BeautifulSoup
import json

class ProfessorScraper:
    
    def __init__(self) -> None:
        self.list_tags=self.set_json("tags.json")

        
        self.class_tags=self.set_json("classtags.json")["classes"]
        self.comment_tags=self.set_json("classtags.json")["comments"]
        self.quality_tags=self.set_json("classtags.json")["quality"]
        self.diff_tags=self.set_json("classtags.json")["difficulty"]
        
        
        
        
        
    def scrape_iter(self,prof_name):
        
        currNode=None
        
        
        
        response=requests.get(self.create_url(prof_name=prof_name))
        
        if response.status_code==200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            
            currNode=None
        
            for tag in self.list_tags:
                typ=tag["type"]
                name=tag["name"]
                
                if not currNode:
                    if typ=="id":
                        currNode=soup.find(id=name)
                    else:
                        currNode=soup.find(class_=name)
                else:
                    
                    if typ=="id":
                        currNode=currNode.find(id=name)
                    else:
                        currNode=currNode.find(class_=name)
            
            ##at this point we have the parent element for all the li elements of ratings
            return currNode
            
            
        else:
            print("network error")
            
            
    def get_classes(self,currNode):
        
            list_tags=currNode.find_all(['li'])

            classes=set()

            for tag in list_tags:
                
                
                #if div element is an ad if it is we dont go 
                div_element=tag.find(id="ad_controller")
                
                if not div_element:

                    start_node=None
                    
                    for class_tag in self.class_tags:
                        
                        
                        if not start_node:
                            start_node=tag.find(class_=class_tag)
                        else:
                            start_node=start_node.find(class_=class_tag)
                        
                    if start_node:
                        classes.add(start_node.text)
            return classes
    
    def get_comments(self,currNode):
        
        comments=[]
        
        list_tags=currNode.find_all(['li'])
        
        for tag in list_tags:
            
            div_element=tag.find(id="ad_controller")
            
            if not div_element:
                
                start_node=None
                
                for comm_tag in self.comment_tags:
                    
                    if not start_node:
                        start_node=tag.find(class_=comm_tag)
                    else:
                        start_node=start_node.find(class_=comm_tag)
            
                if start_node:
                    comments.append(start_node.text)
                
        return comments
        
    def get_quality(self,currNode):
        
        quality=[]
        
        list_tags=currNode.find_all(['li'])
        
        for tag in list_tags:
            
            div_element=tag.find(id="ad_controller")
            
            start_node=None
            
            if not div_element:
                
                for q_tag in self.quality_tags:
                    if not start_node:
                        start_node=tag.find(class_=q_tag)
                    else:
                        start_node=start_node.find(class_=q_tag)
                
                if start_node:
                    quality.append(start_node.text)
                    
        return quality
        
    
    def get_difficulty(self,currNode):
        difficulty=[]
        
        list_tags=currNode.find_all(['li'])
        
        for tag in list_tags:
            
            div_element=tag.find(id="ad_controller")
            
            start_node=None
            
            if not div_element:
                
                for d_tag in self.diff_tags:
                    
                    if not start_node:
                        start_node=tag.find(class_=d_tag)
                    else:
                        nodes=start_node.find_all(class_=d_tag)
                        
                        #special case where the class names were the same
                        if len(nodes)>1:
                            start_node=nodes[1]
                        elif nodes:
                            start_node=nodes[0]
                    
                        
                if start_node:
                    difficulty.append(start_node.text)
        return difficulty
    
    def scrape(self,prof_name):
        currNode=self.scrape_iter(prof_name=prof_name)
        if currNode:
            classes=self.get_classes(currNode=currNode)
            comments=self.get_comments(currNode=currNode)
            quality=self.get_quality(currNode=currNode)
            difficulty=self.get_difficulty(currNode=currNode)
            
            first_name=prof_name.split(" ")[0]
            last_name=prof_name.split(" ")[1]
            
            return {
                "prof_name":f"{first_name} {last_name}",
                "classes":list(classes),
                "comments":comments,
                "quality":quality,
                "difficulty":difficulty
            }
    
    def set_json(self,file_name):
       
        with open(file_name, 'r') as file:
            data = json.load(file) 
        return data

    
    def create_url(self,prof_name):
        
        prof_name=prof_name.split(" ")
        
        first_name=prof_name[0]
        last_name=prof_name[1]
        
        url=f"https://www.ratemyprofessors.com/search/professors/696?q={first_name}%20{last_name}"
        
        return url
        