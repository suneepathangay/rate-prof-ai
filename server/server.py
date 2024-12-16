from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import sys
from pathlib import Path
from dotenv import load_dotenv
sys.path.append(str(Path(__file__).resolve().parent.parent))
from funcall.funcall import FuncCall
from langchain.memory import RedisChatMessageHistory, ChatMessageHistory
import redis
import os
from chatservice import ChatService




app = Flask(__name__)
CORS(app)

chat_service=ChatService()






@app.route('/chat', methods=['POST'])
def process_request():
    
    
    req_data = request.get_json()
    
    response=chat_service.converse(request=req_data)
    
    if 'error' in response:
        return response
    
    return response
    







if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
