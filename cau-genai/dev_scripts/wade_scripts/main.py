import json
from difflib import get_close_matches
from typing import Optional
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os



credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                   api_key = "6JMjtZKFsxcbaokewSx68NiNLNXSmfgrx5rY_vo9HNn9"
                  )

model_id = "ibm/granite-20b-multilingual"  # Choose a model (e.g., Granite, Flan, Mistral)

# Initialize model
model = Model(
    model_id=model_id,
    credentials=credentials,
    project_id="ba1d12f8-da6f-4cb1-a8a0-47c51a1285b7"  # Found in IBM Cloud
)

# Simple request-response test
prompt = "Hello my name is DOGUI.AI, what can you do"
response = model.generate_text(prompt)

current_directory = os.getcwd()


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
        return data
    
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> Optional[str]:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.10)
    return matches[0] if matches else None 

def get_answer_for_question(question: str, knowledge_base: dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:  # Fixed comparison here
            return q["answer"]
    return None  # Added return None if no match found


def chat_bot():
    knowledge_base: dict = load_knowledge_base(current_directory + '/training/exercises/github_introduction' + '/knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: Optional[str] = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank You! I learned a new response!')

if __name__ == "__main__":
    chat_bot()
 