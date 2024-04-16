from fastapi import FastAPI
from pydantic import BaseModel
import json
import numpy as np
from difflib import get_close_matches
from typing import Union
import a2

app = FastAPI()

# @app.get('/')
#async def scoring_endpoint():
                
                
class scoringitem(BaseModel):
    question : str

@app.post('/input')
async def scoring_endpoint(item: scoringitem):
    knowledge_base: dict = a2.load_knowledgebase("A1_knowledge_base.json")
    print("Bot: Greetings! How can I help you make the most of your time?")
    while True:
        user_input: str= item.model_dump()["question"]
        
        if(user_input.lower() == 'quit'):
            break
        
        questions,question_vecs = a2.question_encoder(knowledge_base)
        
        best_match: Union[str,None] = a2.find_best_match(user_input.lower(),questions,question_vecs)
        
        if best_match:
            answer: str = a2.get_answer_for_question(best_match, knowledge_base)
            ans = {"bot": answer}
            return ans
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str =input('Type the answer or "skip" to skip: ')
            
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question":user_input, "answer":new_answer})
                a2.save_knowldege_base('C:\\Users\\achin\\OneDrive\\Desktop\\Minor 2\\Code\\A1_knowledge_base.json', knowledge_base)
                print('Bot: Thank You!! I Learned a new response!')

