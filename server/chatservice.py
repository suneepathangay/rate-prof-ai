
##service to interact with redis and openai
from dotenv import load_dotenv
import redis
import os
from langchain.memory import RedisChatMessageHistory, ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from funcall.funcall import FuncCall


class ChatService:
    
    def __init__(self) -> None:
        load_dotenv()
        self.func_call=FuncCall()
    
    
    def init_redis_client(self):
        
        host=os.getenv("REDIS_HOST")
        username=os.getenv("REDIS_USERNAME")
        password=os.getenv("REDIS_PASSWORD")
        port=os.getenv("REDIS_PORT")
        
        
        return f"redis://{username}:{password}@{host}:{port}"

    
    def get_conversation(self,request):
        
        if not self.validate_request(request=request):
            return {"error":"invalid json"}
        
        session_id=request['session_id']

        memory=self.get_message_history(session_id=session_id)
        
        memory = ConversationBufferMemory(
            memory_key="history", 
            return_messages=True,  
        )
        
        
        
        conversation = ConversationChain(
            llm=self.func_call.get_llm(),
            memory=memory,
            verbose=True
        )
        
        return conversation
    
    def get_message_history(self,session_id):
        
        message_history = RedisChatMessageHistory(
            url=self.init_redis_client(),
            session_id=session_id,
            key_prefix="langchain:"
        )
        print("mesage_value",message_history)
        return message_history
        
    
    def validate_request(self,request):
        
        if not request:
            return False
        
        if 'message' not in request or 'session_id' not in request:
            return False
        
        return True
    
    def converse(self,request):
    
        
        message=request['message']
        session_id=request['session_id']
        
        keywords=self.func_call.extract_key_words_query(query=message)
        raw_json_data=self.func_call.match_query_function(query=message,keywords_obj=keywords)
        
        ##give the data and the data cleaning prompt so it be put into 
        #response = conversation.predict(input=message)
        
        conversation=self.get_conversation(request=request)
        message_history=self.get_message_history(session_id=session_id)
        
        try:
            response = conversation.predict(input=message)
            message_history.add_user_message(message)
            message_history.add_ai_message(response)
            
            return {
                'response': response,
                'session_id': session_id,
                'message_history': [
                    {'role': msg.type, 'content': msg.content} 
                    for msg in message_history.messages
                ]
            }
            
        
        except Exception as e:
            return {"error": f"internal server error due {e}"} 
        


