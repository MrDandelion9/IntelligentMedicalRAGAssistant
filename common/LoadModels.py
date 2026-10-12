import os
from langchain_huggingface import HuggingFaceEmbeddings


def embedding_model():
    model_path = os.getenv("EMBEDDING_MODEL_PATH")

    embeddings = HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={
            "device": "cpu"
        }
    )

    return embeddings