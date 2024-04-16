import json
import numpy as np
from difflib import get_close_matches
from typing import Union

def load_knowledgebase(file_path: str) -> dict:
    with open(file_path,'r') as file:
        data: dict= json.load(file)
    return data
def save_knowldege_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data,file,indent=2)
        
from sentence_transformers import SentenceTransformer
model_name = 'bert-base-nli-mean-tokens'
model = SentenceTransformer(model_name)

def question_encoder(Knowledge_base: dict):
    questions = []
    for q in Knowledge_base["questions"]:
        questions.append(q['question'])
    
    question_vecs= model.encode(questions)
    return questions,question_vecs

from sklearn.metrics.pairwise import cosine_similarity
def find_best_match(user_question: str, questions: list[str], question_vecs: list[str]):
    sims = cosine_similarity(
    [model.encode(user_question)],
    question_vecs[:])
    
    return questions[np.argmax(sims)]

def get_answer_for_question(question: str, Knowledge_base: dict) -> Union[str,None]:
    for q in Knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
