# Auto LLM Chatbot

This package is for using LLM in Chatbot applications with automatic chat history management using vector db (chroma db) on you local machine.

# Why Auto LLM Chatbot

1. No need to worry about a hundred or thousands of lines of code to just manage very old chat history as context for ongoing conversations.
2. Easily you can build chatbot in few lines, see below example.
3. Fully customizable, you have control over your data, your chats.
4. Easily you can integrate with any framework or existing code you are using.

## Features-

1. Build chatbot easily
2. No need to worry about chat history management.


## How this works-

1. You just need to create skeleton of project.
2. Auto LLM Chatbot will store your conversation (user input and ai's output) automatically in (vector db) chroma db, and everytime it will automatically fetch chat history whenever you chat with llm next time.

## Prerequisites-

1. Python
2. Knowledge of GenAI

## Example Usage-

```
from auto_llm_chatbot.chatbot import chat


llm_settings = {
    "provider": 'ollama',
    "base_url": 'http://localhost:11434',
    "model": "llama3.1",
    "options": {},
    "api_key": None
}
embedding_model_settings = {
    "provider": 'ollama',
    "base_url": 'http://localhost:11434',
    "model": "nomic-embed-text",
    "api_key": None
}
# llm_settings = {
#     "provider": 'openai',
#     "base_url": "https://api.openai.com/v1",
#     "model": "gpt-4o-mini",
#     "options": {},
#     "api_key": ""
# }
# embedding_model_settings = {
#     "provider": 'openai',
#     "base_url": "https://api.openai.com/v1",
#     "model": "text-embedding-ada-002",
#     "api_key": ""
# }
chroma_settings = {
    "host": None,
    "port": None,
    "settings": None
}

memory_settings = {
    "try_queries": True,
    "results_per_query": 3,
}
collection_name = "conversation"
unique_session_id = "012"
unique_message_id = "A01"
system_message = "You are a helpful assistant."
buffer_window_chats = [
    {'role': 'user', 'content': 'what is 7*5?'},
    {'role': 'assistant', 'content': '35'},
]
query = "Who is PM of India?"
response = chat(query=query, system_message=system_message,
                llm_settings=llm_settings,
                chroma_settings=chroma_settings,
                embedding_model_settings=embedding_model_settings,
                memory_settings=memory_settings,
                memory=True,
                collection_name=collection_name,
                unique_session_id=unique_session_id,
                unique_message_id=unique_message_id,
                buffer_window_chats=buffer_window_chats)
print("Assistant: ", response)
```

*You can see, we are having initial conversation with assistant, where it is not aware of context (check next output also)-*

```
Vector Database Queries sliced: ['What is the date of the conversation?', 'Has the user asked about politics or current events before?', 'who is PM of India?']

Processing queries to vector database: 100%|██████████| 3/3 [00:01<00:00,  2.21it/s]
0 past conversation fetched.'
system: You are a helpful assistant.
Here is the memory of old conversations-
{'memories': '[]'}

user: what is 7*5?
assistant: 35
user: who is PM of India?
Assistant:  As of my last knowledge update in October 2023, the Prime Minister of India is Narendra Modi. He has been in office since May 2014. Please verify with a current source to confirm this information, as political positions can change.
```

*Below you can see assistant remember the context in next run, fetched context as memories-*

```
Vector Database Queries sliced: ["Who is 'him' referring to?", "What information does the user already have about 'him'?", 'Tell me more about him?']

Processing queries to vector database:   0%|          | 0/3 [00:00<?, ?it/s]Number of requested results 3 is greater than number of elements in index 1, updating n_results = 1
Processing queries to vector database:  33%|███▎      | 1/3 [00:00<00:01,  1.84it/s]Number of requested results 3 is greater than number of elements in index 1, updating n_results = 1
Processing queries to vector database:  67%|██████▋   | 2/3 [00:00<00:00,  2.27it/s]Number of requested results 3 is greater than number of elements in index 1, updating n_results = 1
Processing queries to vector database: 100%|██████████| 3/3 [00:01<00:00,  2.14it/s]
3 past conversation fetched.'
system: You are a helpful assistant.
Here is the memory of old conversations-
{'memories': "['user: who is PM of India?\\nassistant: As of my last knowledge update in October 2023, the Prime Minister of India is Narendra Modi. He has been in office since May 2014. Please verify with a current source to confirm this information, as political positions can change.', 'user: who is PM of India?\\nassistant: As of my last knowledge update in October 2023, the Prime Minister of India is Narendra Modi. He has been in office since May 2014. Please verify with a current source to confirm this information, as political positions can change.', 'user: who is PM of India?\\nassistant: As of my last knowledge update in October 2023, the Prime Minister of India is Narendra Modi. He has been in office since May 2014. Please verify with a current source to confirm this information, as political positions can change.']"}

user: what is 7*5?
assistant: 35
user: Tell me more about him?
Insert of existing embedding ID: A01
Add of existing embedding ID: A01
Assistant:  Narendra Modi is the Prime Minister of India, having been in office since May 2014. He is a member of the Bharatiya Janata Party (BJP) and the Rashtriya Swayamsevak Sangh (RSS), a Hindu nationalist volunteer organization. Modi was born on September 17, 1950, in Vadnagar, Gujarat.

Before becoming Prime Minister, he served as the Chief Minister of Gujarat from 2001 to 2014. His tenure as Prime Minister has been marked by significant economic reforms, such as the Goods and Services Tax (GST), the Make in India initiative, and efforts to improve infrastructure and digital connectivity.

Modi's government has also been known for its focus on national security, and he has taken a strong stance on issues concerning terrorism and cross-border relations, especially with Pakistan. He has been a polarizing figure in Indian politics, with both supporters praising his leadership and critics raising concerns about religious tensions and democratic backsliding.

Modi's foreign policy emphasizes strengthening India's global standing and relationships, particularly in the Indo-Pacific region. His leadership style is characterized by a strong central authority and a focus on development and progress.

For the latest developments or specific policies, it is recommended to consult current and authoritative sources.
```


## Understand Settings Parameters-

- llm_settings
  - provider: can be `openai` or `ollama` only for now.
  - base_url: base url of provider
  - model: name of model
  - options: This is optional, by default it usages default settings of provider
  - api_key: API key from provider
     ```
     # openai llm_settings
     llm_settings = {
         "provider": 'openai',
         "base_url": "https://api.openai.com/v1",
         "model": "gpt-4o-mini",
         "options": {},
         "api_key": ""
     }
    
    # ollama llm_settings 
    llm_settings = {
        "provider": 'ollama',
        "base_url": 'http://localhost:11434',
        "model": "llama3.1",
        "options": {},
        "api_key": None
    }
    ```
    
- embedding_model_settings
  - provider: can be `openai` or `ollama` only for now.
  - base_url: base url of provider
  - model: name of model
  - options: This is optional, by default it usages default settings of provider
  - api_key: API key from provider
     ```
     # openai embedding_model_settings
     embedding_model_settings = {
         "provider": 'openai',
         "base_url": "https://api.openai.com/v1",
         "model": "text-embedding-ada-002",
         "api_key": ""
     }
    
     # ollama embedding_model_settings
     embedding_model_settings = {
         "provider": 'ollama',
         "base_url": 'http://localhost:11434',
         "model": "nomic-embed-text",
         "api_key": None
     }
    ```


- embedding_model_settings
  - host: host url of chromadb
  - port: port of chromadb
  - settings: chromadb settings, including authentication. Read chromadb documentation.
     ```
      chroma_settings = {
          "host": None,
          "port": None,
          "settings": None
      }
    ```
    
- memory_settings-
  - try_queries: It means, assistant will refine your query to search for similar embeddings in chromadb.
  
    Example: Your input is 'My name is Dipesh'

    Assistant might try these queries in vector db: 'who is Dipesh?', 'is there any conversation with Dipesh?', 'My name is Dipesh' etc.
  - results_per_query: How many relevant chats you want to fetch from vector db.
    ```
     memory_settings = {
         "try_queries": True,
         "results_per_query": 3,
     }
    ```

- `collection_name = "conversation"`: (str) This the collection name you want to create in vector db.
- `unique_session_id = "012"`: (str) This you need to manage. Example if user-A is having conversation in session-1 or user-A is having conversation in session-2.
- `unique_message_id = "A01"`: (str) This you need to manage. It can be any unique message id. You can use uuid as string here,
- `system_message = "You are a helpful assistant."`: (str) Any system message or prompt.
- `buffer_window_chats`: If you want to manage sliding window chat history, you can pass last-n message (last-n conversation) like this in OpenAI's format.

  Example:

  ```
  buffer_window_chats = [
      {'role': 'user', 'content': 'what is 7*5?'},
      {'role': 'assistant', 'content': '35'},
  ]
  ```
- `query = "Tell me more about him?"`: Any current / last human message.

## FAQs-

1. Can I customize LLM endpoints
    - Yes you can use any OpenAI compatible endpoints.

2. Can I use custom hosted chromadb
    - Yes you can use custom endpoints for chromadb, if not provided then it will create chroma dir in your root folder of project.

3. I don't want to manage history. Just wanted to chat.
    - Yes you can, just set `memory=False`
 
4. Any doubts or suggestions please raise issue or connect me at `dipesh.paul@systango.com`
