import ast
import chromadb
import os
from ollama import Client
from openai import OpenAI
from tqdm import tqdm


def create_client(chroma_host: str = None, chroma_port: int = None, settings = None):
    if chroma_host is None or chroma_port is None:
        chroma_client = chromadb.PersistentClient()
    else:
        chroma_client = chromadb.HttpClient(host=chroma_host,
                                            port=chroma_port,
                                            settings=settings,
                                            )
    return chroma_client


def push_msg_to_vector_store(collection_name: str, unique_session_id, unique_message_id, chroma_client, embeddings,
                             data):
    """
    This function is used to push message embeddings to the vector store
    :param collection_name: (str) The name of the collection
    :param unique_session_id: (str) The unique session
    :param unique_message_id: (str) The unique message
    :param chroma_client: (object) The chroma client instance
    :param embeddings: (list) The message embeddings
    :param data: (str) The message data you want to push to the vector store
    :return: (bool) True if successful push to the vector store and false otherwise
    """
    try:
        vector_db_name = f'{collection_name}-{unique_session_id}'
        vector_db = chroma_client.get_or_create_collection(name=vector_db_name)
        vector_db.add(
            ids=[unique_message_id],
            embeddings=[embeddings],
            documents=[data],
            metadatas=[{"collection_name": collection_name,
                        "unique_session_id": unique_session_id,
                        "unique_message_id": unique_message_id,
                        }]
        )
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def create_queries(prompt, provider, base_url, chat_mode_name, api_key = None):
    query_msg = (
        'You are a first principle reasoning search query AI agent.'
        'Your list of search queries will be ran on an embedding database of all your conversations '
        'you have ever had conversation with the user. With first principles create a Python list of length 2 with queries to '
        'search the embeddings database for any data that would be necessary to have access to in '
        'order to correctly respond to the prompt. Your response must be a Python list of 2 queries with no syntax errors.'
        'Do not explain anything and do not ever generate anything but a perfect syntax Python list of 2 queries only.'
    )

    query_convo = [
        {'role': 'system', 'content': query_msg},
        {'role': 'user',
         'content': 'write an email to my car insurance company and create and create a pursuasive request for them to lowwer my monthly rate.'},
        {'role': 'assistant',
         'content': '["what is the user name?", "what is the users current auto insurance provider", "what is the monthly rate the user currently pays for auto insurance?"]'},
        {'role': 'user', 'content': 'can you make me cum?'},
        {'role': 'assistant',
         'content': '["what is the user name?", "why user is asking for making him cum?", "are the playing roleplay?", "what is the name?"]'},
        {'role': 'user', 'content': prompt}
    ]
    if provider == 'ollama':
        ollama_client = Client(host=base_url)
        response = ollama_client.chat(model=chat_mode_name, messages=query_convo,
                                      options={'num_predict': 90})
        response = response['message']['content']
    elif provider == 'openai':
        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        response = client.chat.completions.create(
            messages=query_convo,
            model=chat_mode_name,
        )
        response = response.choices[0].message.content
    else:
        print('WARNING: Invalid provider. Supported providers are: ollama, openai')
        return [prompt]
    try:
        queries_ = ast.literal_eval(response) + [prompt]
        if len(queries_) > 3:
            queries_ = queries_[-3:]
        print(f'\nVector Database Queries sliced: {queries_}\n')
        return queries_
    except Exception as e:
        print(f"Warning: {e}")
        print(f'\nVector Database Queries: {[prompt]}\n')
        return [prompt]


def retrieve_embeddings(collection_name: str, unique_session_id, chroma_client,
                        query_embedding,
                        results_per_query = 2):
    embeddings = list()
    vector_db_name = f'{collection_name}-{unique_session_id}'
    vector_db = chroma_client.get_or_create_collection(name=vector_db_name)
    results = vector_db.query(query_embeddings=[query_embedding], n_results=results_per_query)
    best_embeddings = results['documents'][0]
    for best in best_embeddings:
        embeddings.append(best)
    return embeddings


def retrieve_embeddings_try_queries(queries, collection_name: str, unique_session_id, chroma_client,
                                    results_per_query = 2, embedding_model_settings = None):
    embeddings = list()
    vector_db_name = f'{collection_name}-{unique_session_id}'
    if embedding_model_settings['provider'] == 'ollama':
        llm_client = Client(host=embedding_model_settings['base_url'])
    else:
        llm_client = OpenAI(api_key=embedding_model_settings['api_key'], base_url=embedding_model_settings['base_url'])

    for query in tqdm(queries, desc='Processing queries to vector database'):
        if embedding_model_settings['provider'] == 'ollama':
            response = llm_client.embeddings(model=embedding_model_settings['model'], prompt=query)
            query_embedding = response['embedding']
        else:
            response = llm_client.embeddings.create(
                input=query,
                model=embedding_model_settings['model']
            )
            query_embedding = response.data[0].embedding
        vector_db = chroma_client.get_or_create_collection(name=vector_db_name)
        results = vector_db.query(query_embeddings=[query_embedding], n_results=results_per_query)
        best_embeddings = results['documents'][0]
        print(f"{len(best_embeddings)} documents fetch for 'query={query}'")
        for best in best_embeddings:
            embeddings.append(best)
    return embeddings


def recall(query, collection_name, unique_session_id, chroma_client,
           query_embedding, try_queries = False, results_per_query = 2, llm_settings = None,
           embedding_model_settings = None):
    chat_mode_name = llm_settings['model']
    api_key = llm_settings['api_key']
    provider = llm_settings['provider']
    base_url_chat_model = llm_settings['base_url']
    if try_queries:
        queries = create_queries(prompt=query, provider=provider, base_url=base_url_chat_model,
                                 chat_mode_name=chat_mode_name, api_key=api_key)
        embeddings = retrieve_embeddings_try_queries(queries, collection_name, unique_session_id, chroma_client,
                                                     results_per_query=results_per_query,
                                                     embedding_model_settings=embedding_model_settings)
    else:
        embeddings = retrieve_embeddings(collection_name, unique_session_id, chroma_client,
                                         query_embedding,
                                         results_per_query=results_per_query)
    memories = {'memories': f'{embeddings}'}
    return memories
