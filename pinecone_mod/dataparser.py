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
        
        for filename in files:
            file_parts=filename.split("data")
            file_number=int(file_parts[1].split(".")[0])
            if file_number==file_num:
                with open(self.path+"/"+files[0], "r") as file:
                    data = json.load(file) 
                    return data
    
    
    def add_easiness_quality(self,data):
        
        easy_added= map(lambda d: self.add_easiness(d),data)
        diff_added=map(lambda d: self.add_quality(d),easy_added)
        
        return list(diff_added)
                
        
    
    def add_easiness(self,data):
        #take the average of the data and compare against the q25 and q75
        
            sum_easiness=[]
                
            for easy_score in data["difficulty"]:
                sum_easiness.append(float(easy_score))
            
            if len(sum_easiness)==0:
                data[DifficultyLevel.TYPE]=DifficultyLevel.UNKNOWN
                return data
                
            average_diff=sum(sum_easiness)/len(sum_easiness)
                
                
            q25,q75=self.difficulty_thresholds[0],self.difficulty_thresholds[1]
            
            if average_diff<=q25:
                    #add EASY
                data[DifficultyLevel.TYPE]=DifficultyLevel.EASY
            elif average_diff<q75:
                    #add MEDIUM
                data[DifficultyLevel.TYPE]=DifficultyLevel.MEDIUM
            else:
                    #add HARD
                data[DifficultyLevel.TYPE]=DifficultyLevel.HARD
            return data
        
    
    def add_quality(self,data):
        #take the average of the data and compare against the q25 and q75
        quality_scores=[]

        for score in data['quality']:
            quality_scores.append(float(score))
        
        if len(quality_scores)==0:
            data[QualityLevel.TYPE]=QualityLevel.UNKNOWN
            return data
        
        avg_qul=sum(quality_scores)/len(quality_scores)
        
        q25,q75=self.difficulty_thresholds[0],self.difficulty_thresholds[1]
        
        if avg_qul<=q25:
            data[QualityLevel.TYPE]= QualityLevel.LOW
        elif avg_qul<q75:
            data[QualityLevel.TYPE]=QualityLevel.DECENT
        else:
            data[QualityLevel.TYPE]=QualityLevel.GOOD
    
        return data
    
    
# parser=Parser(path="../neujsondata")
# print(parser.load_json(1))