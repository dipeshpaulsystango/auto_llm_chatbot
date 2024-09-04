from auto_llm_chatbot.chatbot import chat

# llm_settings = {
#     "provider": 'ollama',
#     "base_url": 'http://localhost:11434',
#     "model": "llama3.1",
#     "options": {},
#     "api_key": None
# }
# embedding_model_settings = {
#     "provider": 'ollama',
#     "base_url": 'http://localhost:11434',
#     "model": "nomic-embed-text",
#     "api_key": None
# }
llm_settings = {
    "provider": 'openai',
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini",
    "options": {},
    "api_key": ""
}
embedding_model_settings = {
    "provider": 'openai',
    "base_url": "https://api.openai.com/v1",
    "model": "text-embedding-ada-002",
    "api_key": ""
}
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
query = "Tell me more about him?"
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
