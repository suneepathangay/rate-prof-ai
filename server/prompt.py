


def extract_query_terms(query_string):
    template = """
        You are an assistant that extracts two types of key terms from a user query: a course name and a professor name. Below are the rules for extraction:

        1. **Key Terms**:
        - **Professor Name**: Includes first and/or last names, and optional titles such as "Dr." or "Prof." (e.g., "Benjamin Lerner," "Dr. Smith").
        - **Course Name**: Includes course codes (e.g., "CS3500") or descriptive course names (e.g., "Intro to Biology").

        2. **Query Scenarios**:
        - If both a professor name and a course name are mentioned, extract both.
        - If only one key term exists, extract that term and leave the other blank.
        - If no key terms exist, set both `prof_name` and `course_name` to empty strings.
        - If multiple professors or courses are mentioned, return them as comma-separated lists.

        3. **Response Format**:
        Always format your response as:
        `[prof_name: professor1, professor2, ..., course_name: course1, course2, ...]`

        4. **Examples**:
        - Query: "What does Benjaman Lerner teach?"
            Response: [prof_name: Benjaman Lerner, course_name: ]
        - Query: "Is Professor Sarah Lee assigned MATH1100?"
            Response: [prof_name: Sarah Lee, course_name: MATH1100]
        - Query: "Does Dr. Lee offer CS3500?"
            Response: [prof_name: Dr. Lee, course_name: CS3500]
        - Query: "Who is teaching either BIOL3000 or CHEM2000?"
            Response: [prof_name: , course_name: BIOL3000, CHEM2000]
        - Query: "What courses are available this semester?"
            Response: [prof_name: , course_name: ]

        Below is a real user query. Craft an answer based on the requirements and return a response.

        User query: "{input}"

        Response:
        """
    return template


def decides_function(input,query):
    
        template = """
        You are an assisstant who is given a list of possible functions and you are responsible for deciding which function is best suited to retrieve information based on a user given query. 
        Additionally two parameters will be given to you, course_name and professor_name, you may use these when deciding which function is most appropriate and you may use a combination of them. Use them accordingly. Below are the functions and their documentation/description.
        If you feel that the user query cannot be answered via this functions, craft an apology detailing why you were unable to make a decision.
        
        get_class_data(course_name:string) ouputs the data such as professors that are teaching the course, course timings, and attributes such as which degree requirements the course fullfills and a short description about the course.
        
        get_prof_data(prof_name:string) outputs the data related to student reviews for the professor professor.
        
        User query: "This is the user query string: Does Benjamin Lerner teach DS4000. These are the two paramters provided to you. [course_name:DS4000,prof_name:Benjamin Lerner]"
        
        Response:
        """
        return template

def craft_response(input):
    pass
    