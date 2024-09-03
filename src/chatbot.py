from lazyme import color_print as cprint

from llm import ollama_chat, openai_chat, run_embedding
from chroma_handler import create_client, recall, push_msg_to_vector_store


def chat(query, system_message, llm_settings, chroma_settings, embedding_model_settings, memory_settings, memory = True,
         collection_name = None,
         unique_session_id = None,
         unique_message_id = None):
    chroma_client = create_client(chroma_host=chroma_settings['host'],
                                  chroma_port=chroma_settings['port'],
                                  settings=chroma_settings['settings'])
    if memory:
        if collection_name is None or unique_session_id is None or unique_message_id is None:
            raise ValueError('Collection name, unique session id, and unique message id are required')
        query_embedding = run_embedding(embedding_model_settings=embedding_model_settings, query=query)
        memories = recall(query, collection_name, unique_session_id, chroma_client,
                          query_embedding, try_queries=memory_settings['try_queries'],
                          results_per_query=memory_settings['results_per_query'],
                          llm_settings=llm_settings,
                          embedding_model_settings=embedding_model_settings, )
        messages = [
            {'role': 'system', 'content': system_message + f"\nHere is the memory of old conversations-\n{memories}\n"},
            {'role': 'user', 'content': query}
        ]

        for i in messages:
            cprint(f"{i['role']}: {i['content']}", color='cyan')
        if llm_settings['provider'] == 'ollama':
            chat_response = ollama_chat(messages=messages,
                                        model=llm_settings['model'],
                                        base_url=llm_settings['base_url'],
                                        options=llm_settings['options'])
            chat_response = chat_response['message']['content']
        else:
            chat_response = openai_chat(messages=messages, api_key=llm_settings['api_key'],
                                        base_url=llm_settings['base_url'], model=llm_settings['model'])
            chat_response = chat_response.choices[0].message.content

        data = f"user: {query}\nassistant: {chat_response}"
        data_embedding = run_embedding(embedding_model_settings=embedding_model_settings, query=data)

        push_msg_to_vector_store(collection_name=collection_name, unique_session_id=unique_session_id,
                                 unique_message_id=unique_message_id, chroma_client=chroma_client,
                                 embeddings=data_embedding,
                                 data=data)
        return chat_response
    else:
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': query}
        ]
        if llm_settings['provider'] == 'ollama':
            chat_response = ollama_chat(messages=messages, model=llm_settings['model'],
                                        base_url=llm_settings['base_url'],
                                        options=llm_settings['options'])
        else:
            chat_response = openai_chat(messages=messages, api_key=llm_settings['api_key'],
                                        base_url=llm_settings['base_url'], model=llm_settings['model'])
        return chat_response


if __name__ == '__main__':
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
    system_message = "You are a helpful assistant"
    response = chat(query=input("You: "), system_message=system_message,
                    llm_settings=llm_settings,
                    chroma_settings=chroma_settings,
                    embedding_model_settings=embedding_model_settings,
                    memory_settings=memory_settings,
                    memory=True,
                    collection_name=collection_name,
                    unique_session_id=unique_session_id,
                    unique_message_id=unique_message_id)
    print(response)
