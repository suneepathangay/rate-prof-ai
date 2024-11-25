Plan for database schema and lookup for the LLM

each json object has 5 keys: prof_name, comments, classes, quality, and difficulty

we can embed each attribute and then add them to get one single vector 

we need to transform difficulty and quality to words so that they can be processed easily

we need to do some data analysis on these two attributee by finding the average difficulty of all the profs

bottom 25% is easy middle 50 is medium and top 25% is hard

Once we embed each attirbute and add it to create one vector we can query using pinceone and feed the vectors to chatgpt

TODO Currently:

Write the data to Pinecone DB

Write Classes/Functions to query our pinecone DB

Select and config LLM to Use

Create UI


