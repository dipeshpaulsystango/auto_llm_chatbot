import ollama
from ollama import Client
from openai import OpenAI
from abc import ABC, abstractmethod


def ollama_chat(model, messages, options: dict, base_url = None):
    if options is None:
        options = dict()
    if base_url is None:
        response = ollama.chat(model=model, messages=messages, options=options)
    else:
        client = Client(host=base_url)
        response = client.chat(model=model, messages=messages, options=options)
    return response


def ollama_generate(model, prompt, options: dict, base_url = None):
    if options is None:
        options = dict()
    if base_url is None:
        response = ollama.generate(model=model, prompt=prompt, options=options)
    else:
        client = Client(host=base_url)
        response = client.generate(model=model, prompt=prompt, options=options)
    return response


def ollama_embeddings(model, prompt, base_url = None):
    if base_url is None:
        response = ollama.embeddings(model=model, prompt=prompt)
    else:
        client = Client(host=base_url)
        response = client.embeddings(model=model, prompt=prompt)
    return response


def openai_chat(messages: list[dict], api_key, base_url, model = "gpt-3.5-turbo"):
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return chat_completion


def run_embedding(embedding_model_settings, query):
    if embedding_model_settings['provider'] == 'ollama':
        if embedding_model_settings['base_url'] is None:
            query_embedding = ollama.embeddings(model=embedding_model_settings['model'], prompt=query)
        else:
            client = Client(host=embedding_model_settings['base_url'])
            query_embedding = client.embeddings(model=embedding_model_settings['model'], prompt=query)
        query_embedding = query_embedding['embedding']
    else:
        llm_client = OpenAI(api_key=embedding_model_settings['api_key'],
                            base_url=embedding_model_settings['base_url'])
        query_embedding = llm_client.embeddings.create(
            input=query,
            model=embedding_model_settings['model']
        )
        query_embedding = query_embedding.data[0].embedding
    return query_embedding


class CustomLLM:
    def __init__(self, name = 'custom_llm'):
        self.name = name

    @abstractmethod
    def chat(self) -> str:
        """
        Create custom chat model here it should return inference output as text
        :return: (str) output of model
        """
        pass


if __name__ == '__main__':
    model = 'llama3.1'
    prompt = "What is the capital of France?"
    options = {"max_tokens": 10}

    response_chat = ollama_chat(model, [
        {"role": "user", "content": prompt},
    ], options)
    print("Chat Response:", response_chat)

    response_generate = ollama_generate(model, prompt, options)
    print("Generate Response:", response_generate)

    response_embeddings = ollama_embeddings(model, prompt)
    print("Embeddings Response:", response_embeddings)


    class MyCustomLLM(CustomLLM):
        def chat(self) -> str:
            return "This is the custom chat response."


    llm = MyCustomLLM()
    print(llm.chat())
