from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils.helpers import load_pdf_text
from langchain_openai import OpenAIEmbeddings
import pinecone
from pinecone import PodSpec
from src.settings import settings
from langchain_community.vectorstores import Pinecone

import os
os.environ["PINECONE_API_KEY"] = settings.API_KEY_PINECONE

pc = pinecone.Pinecone(api_key=settings.API_KEY_PINECONE)
index_name = "taborra-alarmas"

"""
Busca información relacionada con el negocio en los documentos proporcionados.

Args:
    text (str): Texto de entrada para la búsqueda.
    documents (list): Lista de documentos donde buscar.

Returns:
    dict: Resultado de la búsqueda.
"""
pdf_text = load_pdf_text("./src/database/TaborraAlarmasInfo.pdf")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=20,
    chunk_overlap=10,
    length_function=len
)

chunks = text_splitter.create_documents([pdf_text])

print(f"Chunks: {len(chunks)} ")

emmbeddings = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=len(chunks))

indexes = pc.list_indexes().names()

if index_name not in pc.list_indexes().names():
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )
    print(f"Index {index_name} created.")
else:
    print(f"Index {index_name} already exists.")

try: 
    vectore_store = Pinecone.from_documents(
        documents=chunks,
        embedding=emmbeddings,
        index_name=index_name,
    )

    index = pc.Index(index_name)
    print(index.describe_index_stats())

except Exception as e:
    print(f"Error creating vector store: {e}")


def search_information_bussiness(self, text: str, pdf_path: list):
    pdf_text = load_pdf_text("src/data/TaborraAlarmasInfo.pdf")
    print(f"PDF text {pdf_text}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        length_function=len
    )

    chunks = text_splitter.create_documents([pdf_text])
    return []