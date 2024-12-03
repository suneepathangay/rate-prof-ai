

##class that contains the different funtions for the agent to use
#

##plan for the func calling

##take the query string and give the LLM a prompt to extract the key words such as professor name,classes, quality, difficulty

##we will validate that professor name, classes, quality, difficulty exist and that there are no spelling mistakes

##based on the key words we will construct a prompt and offer the LLM the names and descriptsions of these functions

##then the LLM will choose a function or multiple and it will execute it to get the JSON data
 
##then that info will be passed back to the LLM to processs sds

class FunctionCalling:

    def __init__(self) -> None:
        pass
        
    def map_query_func(self,query):
        #over here in this method we will match the query to the function using an llm
        pass
    
    def find_classes_for_professor(self):
        ##finds all the classes for that professor
        pass
    
    def find_professor_info(self):
        ##finds the data associated with that professor
        pass
    
    def find_quality_professors(self):
        ##this method finds the quality professors at northeastern
        pass
    
    def find_quality_professors_for_class(self):
        ##finds the quality professors for a class
        pass
    
    def find_difficulty_per_class(self):
        ##find the difficulty for the class across professors that teach that class
        pass
    
    def list_all_professors(self):
        #gets all the professors
        pass