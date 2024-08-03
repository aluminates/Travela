import requests
import json
from autogen.agentchat import ConversableAgent

LLAMA_URL = "http://localhost:1234/v1/chat/completions"
LLAMA_HEADERS = {
    "Content-Type": "application/json"
}

def llama_chat(messages):
    data = {
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(LLAMA_URL, headers=LLAMA_HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

class LlamaAgent(ConversableAgent):
    def generate_response(self, messages):
        llama_messages = [{"role": m["role"], "content": m["content"]} for m in messages]
        return llama_chat(llama_messages)

agent = LlamaAgent(
    name="Travel Assistant",
    system_message="You are a helpful travel assistant.",
)