import os

from langchain_chroma import Chroma

from common.LoadModels import embedding_model
from dotenv import load_dotenv

load_dotenv()


#链接向量库
def get_vector_store():

    persist_directory = os.getenv(
        "CHROMA_PERSIST_DIRECTORY"
    )

    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model(),
        collection_name="medical_datas",
    )

    return vector_store