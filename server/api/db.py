import weaviate
import os

auth_config = weaviate.AuthApiKey(api_key=os.environ["API_KEY"])


lecture_class_name = "Lecture"
lecture_schema = {
    "class": lecture_class_name,
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "body", "dataType": ["text"]},
    ],
    "moduleConfig": {"generative-cohere": {}},
    "vectorizer": "text2vec-cohere",
}

convo_class_name = "Conversation"
convo_schema = {
    "class": convo_class_name,
    "properties": [
        {"name": "question", "dataType": ["text"]},
        {"name": "answer", "dataType": ["text"]},
    ],
    "moduleConfig": {"generative-cohere": {}},
    "vectorizer": "text2vec-cohere",
}


def connect_client():
    client = weaviate.Client(
        url="https://hacksc-educate-znzmsuk6.weaviate.network",
        additional_headers={"X-Cohere-Api-Key": os.environ["COHERE_KEY"]},
        auth_client_secret=auth_config,
    )

    return client


if __name__ == "__main__":
    # create schema

    client = connect_client()
    client.schema.create_class(lecture_schema)
    client.schema.create_class(convo_schema)
