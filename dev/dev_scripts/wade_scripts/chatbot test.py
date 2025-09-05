import requests

url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

body = {
	"input": """<|system|>
You are Granite Chat, an AI language model developed by IBM. You are a cautious assistant. You carefully follow instructions. You are helpful and harmless and you follow ethical guidelines and promote positive behavior. You always respond to greetings (for example, hi, hello, g'\''day, morning, afternoon, evening, night, what'\''s up, nice to meet you, sup, etc) with \"Hello! I am Granite Chat, created by IBM. How can I help you today?\". Please do not say anything else and do not start a conversation.
<|user|>
What is 4 + 4
<|assistant|>
The sum of 4 and 4 is indeed 8. This is a basic arithmetic operation known as addition. In this case, you combine the values of 4 and 4, resulting in a total value of 8. If you have any more mathematical questions or need assistance with something else, please feel free to ask!
<|user|>
what did i ask before
<|assistant|>
I'\''m sorry for any confusion, but I am unable to recall your previous question. My purpose is to provide information and answer your questions as accurately and efficiently as possible. If you could please rephrase or provide more context about your previous question, I would be happy to help you again.
<|assistant|>
""",
	"parameters": {
		"decoding_method": "greedy",
		"max_new_tokens": 900,
		"min_new_tokens": 0,
		"repetition_penalty": 1.05
	},
	"model_id": "ibm/granite-20b-multilingual",
	"project_id": "[SECRET]"
}

headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Authorization": "Bearer [SECRET]"
}

response = requests.post(
	url,
	headers=headers,
	json=body
)

if response.status_code != 200:
	raise Exception("Non-200 response: " + str(response.text))

data = response.json()