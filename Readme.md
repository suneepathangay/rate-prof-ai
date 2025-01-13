Overview

About: This repository is the backend code for the ratemyprofesserGPT. It leverages Flask, Redis, Langchain, and OpenAI API. This project creates a RAG-based chatbot that allows students to chat with data scraped from Coursicle and RateMyProfessor.com.

Process:
Originally, I only leveraged the scraped data for all the professors at Northeastern University. Then I would take this data, embed it, and perform a vector search to allow the LLM to interact with the data. However, there were some key problems with this. Some of the data that was scraped from RateMyProfessor was outdated, and it did not provide information on courses, which I felt was important. More concerning, though, was embedding the JSON data, which proved to be problematic and often very inaccurate compared to the search query.

To solve this, I tried a variety of solutions, such as exploring stronger embedding models and converting the JSON into text data based on a sentence template. However, the retrieval results were still poor. I even explored using a customGPT. However, in the end, I went with a method called function calling.

For the function calling I designed it to follow 2 sort of phases. Phase one is the present the LLM with the user query and based on the prompt it will return a json object containing 2 potential keywords course name and professor name. Then based on that I would present the query along with the keywords along with a list of supabase functions that I created and prompted it to decide which functions and input are appropriate based on the query. Then I executed that and retrieved the data and passed it back to the LLM to create a response.

TODOs:

Add table in database to map the informal name of the course to the course number

Work on adding the course planning feature by getting the data from the searchneu data for the course

Add a validation layer for the keywords so that in case a user mispells a professor name or course name,
it should still recognize that keyword ie. C3500 should be interpreted as CS3500.

Create a frontend lol.