


def extract_query_terms(query_string):
    template = """
        You are an assisstant that extracts two types of key terms from a user query. You will extract two key terms from the query. A course name and a professor name. Below is an example.
        user_query: "Does Benjamin Lerner teach CS3500?". In this case there are two key words. Benjamin Lerner(professor name) and CS3500(course name). There can also be a use case in which only 
        one key term exists such as user_query:"Who teaches ENGL1450?". In this cases there is only one key term ENGL1450(course name). Finally, there can be a query in which there are 0 key terms. In that case set profname and coursename 
        to empty strings
        
        Format responses as such: "[prof_name: profname, course_name:coursename]"
        
        Below is a real user query. Craft an answer based on the requirements and return a response
        
        User query: "{input}"

        Response:
        """
    return template


def decides_function(input,query):
    
        template = """
        You are an assisstant who is given a list of possible functions and you are responsible for deciding which function is best suited to retrieve information based on a user given query. 
        Additionally two paramters will be given to you, course_name and professor_name, you may use these when deciding which function is most appropriate and you may use a combination of them. Use them accordingly. Below are the functions are their documentation/description.
        If you feel that the user query cannot be answered via this functions, craft an apology detailing why you were unable to make a decision.
        
        get_class_data(course_name:string) ouputs the data such as professors that are teaching the course, course timings, and attributes such as which degree requirements the course fullfills and a short description about the course.
        
        get_prof_data(prof_name:string) outputs the data related to student reviews for the professor professor.
        
        User query: "This is the user query string: Does Benjamin Lerner teach DS4000. These are the two paramters provided to you. [course_name:DS4000,prof_name:Benjamin Lerner]"
        
        Response:
        """
        return template

def craft_response(input):
    pass
    