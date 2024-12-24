def extract_query_terms_prompt(query_string):
    template = f"""
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

        User query: "{query_string}"
    """
    return template


def function_calling_prompt(keywords,user_query):
    template = f"""
        You are an assistant that is responsible for when given a user query and keywords extracted from that user query, to determine 
        which functions to call along with which parameters along:

        User query: "{user_query} Keywords:{keywords}"
    """
    return template