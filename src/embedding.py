import os
from pathlib import Path
from dotenv import load_dotenv

VS_DIR        = Path(os.getenv("VECTORSTORE_DIR", "./vectorstore"))

def get_embedding_model(): 
    from langchain_community.embeddings import HuggingFaceEmbeddings
       
    return HuggingFaceEmbeddings(
        model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs = {"device": "cpu"}
    )