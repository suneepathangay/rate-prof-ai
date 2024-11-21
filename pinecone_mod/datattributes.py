import os
import json
import numpy as np

##class to get some stats about the numerical data in our json dataset

class DataAttributes:
    
    def __init__(self,path) -> None:
        self.path=path
        self.files=self.get_files()
    
        
    
    def get_files(self):
        
        return os.listdir(self.path)
    
    def get_difficulty_and_quality(self):
        
        difficulty=[]
        quality=[]
        
        for file_name in self.files:
            
            with open(self.path+"/"+file_name, "r") as file:
                    json_data = json.load(file) 
                    
                    for json_obj in json_data:
                        if json_obj:
                            prof_name=json_obj['prof_name']
                            
                            for diff in json_obj['difficulty']:
                                difficulty.append((prof_name,float(diff)))
                            for q in json_obj['quality']:
                                quality.append((prof_name,float(q)))
        
        return difficulty,quality

    def get_difficulty_quality_thresholds(self):
        
        difficulty,quality=self.get_difficulty_and_quality()
        
        q25_diff = np.percentile([diff[1] for diff in difficulty], 25)
        q75_diff = np.percentile([diff[1] for diff in difficulty], 75) 
        
        q25_qual = np.percentile([qual[1] for qual in quality], 25)
        q75_qual= np.percentile([qual[1] for qual in quality],75)
        
        
        return {"quality":[q25_qual,q75_qual],
                "difficulty":[q25_diff,q75_diff]
                }

            
            
            
            
        
        