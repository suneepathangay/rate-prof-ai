
import requests
import json

class NeuSearchClient():
    
    def __init__(self) -> None:
        pass
    
    def get_course_info(self,course_name):
        
        subject_name=""
        course_number=""
        for i in range(len(course_name)):
            if course_name[i].isalpha():
                subject_name+=course_name[i]
            else:
                course_number+=course_name[i]
        
        query=self.get_course_info_graphql(subject_name=subject_name,course_number=course_number)
        
        response=requests.post(url="https://api.searchneu.com/",json=query)
        
        if response.status_code==200:
            return response.json()
        return None
    
    def parse_course_json_obj(self,json_obj):
        
        return_obj={}
        
        data=json_obj['data']
        class_obj=data['class']
        
        #english name of the course
        course_name=class_obj['name']
        
        #course number
        course_number=class_obj['subject']+class_obj['classId']
        
        #course description
        course_description=class_obj["latestOccurrence"]["desc"]
        
        pre_req_obj=class_obj["latestOccurrence"]['prereqs']
        
        prereq_criteria=self.get_prereq_criteria(json_obj=pre_req_obj)
        
        prof_names=self.get_course_obj_prof_names(json_obj=class_obj["allOccurrences"])
        
        return_obj['course_name']=course_name
        return_obj['course_number']=course_number
        return_obj['preq_expression']=prereq_criteria
        return_obj['prof_names']=prof_names
        return_obj['course_description']=course_description
        
        return return_obj
        
    
    
    def get_course_obj_prof_names(self,json_obj):
        
        prof_names=set()
        
        for obj in json_obj:
            for section in obj['sections']:
                for prof in section['profs']:
                    prof_names.add(prof)
        
        return prof_names
        
        
    
    def get_prereq_criteria(self,json_obj):
        
        operator=json_obj['type']
        
        expression=[]
        
        for value_obj in json_obj['values']:
            
            if 'type' not in value_obj:
                expression.append(value_obj['subject']+value_obj['classId'])
                expression.append(operator)
            
            else:
                sub_expression=self.get_prereq_criteria(value_obj)
                expression.append(sub_expression)
        
        return expression
    
    
                
            
            
            
        
        
        
    
    def get_all_courses(self):
        
        response=requests.post(url="https://api.searchneu.com/",json=self.get_all_course_graphql_query())
        
        if response.status_code==200:
            return response.json()
        return None
    
    def get_all_course_graphql_query(self):
        
        return {
        "query": "query searchResults($termId: String!, $query: String, $offset: Int = 0, $first: Int = 1000, $subject: [String!], $nupath: [String!], $honors: Boolean, $campus: [String!], $classType: [String!], $classIdRange: IntRange) {\n  search(\n    termId: $termId\n    query: $query\n    offset: $offset\n    first: $first\n    subject: $subject\n    nupath: $nupath\n    honors: $honors\n    campus: $campus\n    classType: $classType\n    classIdRange: $classIdRange\n  ) {\n    pageInfo {\n      hasNextPage\n    }\n    filterOptions {\n      nupath {\n        value\n        count\n        description\n      }\n      subject {\n        value\n        count\n        description\n      }\n      classType {\n        value\n        count\n        description\n      }\n      campus {\n        value\n        count\n        description\n      }\n      honors {\n        value\n        count\n        description\n      }\n    }\n    nodes {\n      type: __typename\n      ... on Employee {\n        email\n        firstName\n        lastName\n        name\n        officeRoom\n        phone\n        primaryDepartment\n        primaryRole\n      }\n      ... on ClassOccurrence {\n        name\n        subject\n        classId\n        termId\n        host\n        desc\n        nupath\n        prereqs\n        coreqs\n        prereqsFor\n        optPrereqsFor\n        maxCredits\n        minCredits\n        classAttributes\n        url\n        prettyUrl\n        lastUpdateTime\n        feeAmount\n        feeDescription\n        sections {\n          campus\n          classId\n          classType\n          crn\n          honors\n          host\n          lastUpdateTime\n          meetings\n          profs\n          seatsCapacity\n          seatsRemaining\n          subject\n          termId\n          url\n          waitCapacity\n          waitRemaining\n        }\n      }\n    }\n  }\n}\n",
        "variables": {
            "termId": "202530",
            "query": "",
            "offset": 0,
            "first": 1000
        },
        "operationName": "searchResults"
        }
    
    def get_course_info_graphql(self,subject_name,course_number):
        return {"query":"query getClassPageInfo($subject: String!, $classId: String!) {\n  class(subject: $subject, classId: $classId) {\n    name\n    subject\n    classId\n    latestOccurrence {\n      desc\n      prereqs\n      coreqs\n      prereqsFor\n      optPrereqsFor\n      maxCredits\n      minCredits\n      classAttributes\n      url\n      prettyUrl\n      lastUpdateTime\n      feeAmount\n      nupath\n      host\n      termId\n    }\n    allOccurrences {\n      termId\n      sections {\n        classType\n        crn\n        seatsCapacity\n        seatsRemaining\n        waitCapacity\n        waitRemaining\n        campus\n        profs\n        meetings\n        url\n      }\n    }\n  }\n}\n","variables":{"subject":subject_name,"classId":course_number},"operationName":"getClassPageInfo"}

    


search=NeuSearchClient()
prof_names=search.parse_course_json_obj(search.get_course_info(course_name="CS4500"))
print(prof_names)