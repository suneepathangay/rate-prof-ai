import os
import json
from pinecone_mod.datattributes import DataAttributes
from pinecone_mod.macro import DifficultyLevel, QualityLevel

##class to parse the json and convert our numericla data to categorical data for embedding

class Parser:
    
    def __init__(self,path):
        self.path=path
        
        self.attributes=DataAttributes(self.path)
        
        self.difficulty_thresholds=self.attributes.get_difficulty_quality_thresholds()['difficulty']
        self.quality_thresholds=self.attributes.get_difficulty_quality_thresholds()['quality']
        
    def list_json_files(self):
        
        files=os.listdir(self.path)

        return files
    
    def load_json(self,file_num):
        
        files=self.list_json_files()
        
        if file_num<0 or file_num>len(files):
            raise IndexError
        
        for i in range(len(files)):
            filename=files[i]
            
            file_parts=filename.split("data")
            file_number=int(file_parts[1].split(".")[0])
            if file_number==file_num:
                with open(self.path+"/"+files[i], "r") as file:
                    data = json.load(file) 
                    return data
    
    
    def add_easiness_quality(self,data):
        
        #filtering to check for none
        filtered_data=filter(None,data)
        
        easy_added= map(lambda d: self.add_easiness(d),filtered_data)
        diff_added=map(lambda d: self.add_quality(d),easy_added)
        
        classes_changed=map(lambda d:self.parse_classes(d),diff_added)
        reviews_changed=map(lambda d:self.parse_reviews(d),classes_changed)
        
        return list(reviews_changed)
                
        
    
    def add_easiness(self,data):
        #take the average of the data and compare against the q25 and q75
        
            sum_easiness=[]
                
            for easy_score in data["difficulty"]:
                sum_easiness.append(float(easy_score))
            
            if len(sum_easiness)==0:
                data[DifficultyLevel.TYPE.value]=DifficultyLevel.UNKNOWN.value
                return data
                
            average_diff=sum(sum_easiness)/len(sum_easiness)
                
                
            q25,q75=self.difficulty_thresholds[0],self.difficulty_thresholds[1]
            
            if average_diff<=q25:
                    #add EASY
                data[DifficultyLevel.TYPE.value]=DifficultyLevel.EASY.value
            elif average_diff<q75:
                    #add MEDIUM
                data[DifficultyLevel.TYPE.value]=DifficultyLevel.MEDIUM.value
            else:
                    #add HARD
                data[DifficultyLevel.TYPE.value]=DifficultyLevel.HARD.value
            return data
        
    
    def add_quality(self,data):
        #take the average of the data and compare against the q25 and q75
        quality_scores=[]

        for score in data['quality']:
            quality_scores.append(float(score))
        
        if len(quality_scores)==0:
            data[QualityLevel.TYPE.value]=QualityLevel.UNKNOWN.value
            return data
        
        avg_qul=sum(quality_scores)/len(quality_scores)
        
        q25,q75=self.difficulty_thresholds[0],self.difficulty_thresholds[1]
        
        if avg_qul<=q25:
            data[QualityLevel.TYPE.value]= QualityLevel.LOW.value
        elif avg_qul<q75:
            data[QualityLevel.TYPE.value]=QualityLevel.DECENT.value
        else:
            data[QualityLevel.TYPE.value]=QualityLevel.GOOD.value
    
        return data
    
    def parse_classes(self,data):
        string_classes = ', '.join(data['classes'])
        data['classes']=string_classes
        
        return data
    
    def parse_reviews(self,data):
        string_comments = ' | '.join(data['comments'])
        data['comments']=string_comments
        
        return data
