import json
from difflib import get_close_matches
from typing import Optional

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator




def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
        return data
    
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> Optional[str]:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None 

def get_answer_for_question(question: str, knowledge_base: dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:  # Fixed comparison here
            return q["answer"]
    return None  # Added return None if no match found


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')


    credentials = Credentials(
        url="https://us-south.ml.cloud.ibm.com",
        api_key="[SECRET]"
    )

    model_id = "ibm/granite-3-8b-instruct"  # Choose a model (e.g., Granite, Flan, Mistral)

    params = {
    # "frequency_penalty": 0,
    "max_new_tokens": 900,
    "min_new_tokens":0,
    "repetition_penalty":1

    # "presence_penalty": 0,
    # "temperature": 0.7,  # Increased temperature for varietywhat
    # "top_p": 0.9         # Adjusted for a broader token selection
    }

    # Initialize model
    model = ModelInference(
        model_id=model_id,
        credentials=credentials,
        params= {
    # "frequency_penalty": 0,
    "max_new_tokens": 900,
    "min_new_tokens":0,
    
    # "presence_penalty": 0,
    # "temperature": 0.7,  # Increased temperature for varietywhat
    # "top_p": 0.9         # Adjusted for a broader token selection
    },

        project_id="[SECRET]"  # Found in IBM Cloud
    )

    print(model)
    # prompt: str = input('You: ')
    # print("Dogui AI:\n")
    # Simple request-response test
    r = True
    while r:
        prompt = input('\n$User:\n')
        print(f"generating ({prompt})")

        # prompt for watson
        prompt=f"""
        You are Dogui AI, meant to create a very descriptive response based of the users question.
        Your primary purpose is to craft highly vivid, engaging, and richly detailed responses based on th euser's questions.
        Here is their description"{prompt}"."""
        
        if prompt == "q":
            r = False
            exit(0)
        # prompt = "What is 2 + 2?"
        response = model.generate_text(prompt)
        print(f"Dogui AI: {response}")


    # print(f"Dogui AI:{response}")

    # while True:
    #     user_input: str = input('You: ')

    #     if user_input.lower() == 'quit':
    #         break

    #     best_match: Optional[str] = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    #     if best_match:
    #         answer: str = get_answer_for_question(best_match, knowledge_base)
    #         print(f'Dogui AI: {answer}')
    #     else:
    #         print('Bot: I don\'t know the answer. Can you teach me?')
    #         new_answer: str = input('Type the answer or "skip" to skip: ')

    #         if new_answer.lower() != 'skip':
    #             knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
    #             save_knowledge_base('knowledge_base.json', knowledge_base)
    #             print('Bot: Thank You! I learned a new response!')

if __name__ == "__main__":
    chat_bot()
