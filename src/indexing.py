"""
=============================================================
PIPELINE INDEXING — RAG UTS Data Engineering
=============================================================

Pipeline ini dijalankan SEKALI untuk:
1. Memuat dokumen dari folder data/
2. Memecah dokumen menjadi chunk-chunk kecil
3. Mengubah setiap chunk menjadi vektor (embedding)
4. Menyimpan vektor ke dalam vector database

Jalankan dengan: python src/indexing.py
=============================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ─── LANGKAH 0: Load konfigurasi dari .env ───────────────────────────────────
load_dotenv()

# Konfigurasi — bisa diubah sesuai kebutuhan
CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
DATA_DIR      = Path(os.getenv("DATA_DIR", "./data"))
VS_DIR        = Path(os.getenv("VECTORSTORE_DIR", "./vectorstore"))


# =============================================================
# TODO MAHASISWA:
# Pilih salah satu implementasi di bawah (A, B, atau C)
# Hapus komentar pada blok yang kalian pilih
# =============================================================

def build_index_langchain():

    import pandas as pd
    from PyPDF2 import PdfReader
    from langchain_core.documents import Document
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from embedding import get_embedding_model

    print("=" * 50)
    print("Memulai Pipeline Indexing (Langchain + ChromaDB)")
    print("=" * 50)

    #LANGKAH 1: Load Dokumen
    all_chunks = []

    for file_path in DATA_DIR.rglob("*"):
        if file_path.name.startswith('.'): continue # Lewati file tersembunyi
        
        content = ""
        #load data PDF
        if file_path.suffix == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                content += page.extract_text() + "\n"
                
        # Load data csv
        elif file_path.suffix == ".csv":
            df = pd.read_csv(file_path)
            skip = 0
            if "Inflasi" in file_path.name:
                skip = 3
            elif "Penumpang" in file_path.name:
                skip = 3
            df = pd.read_csv(file_path, skiprows=skip)
            df.columns = [col.strip() for col in df.columns]
            for _, row in df.iterrows():
                topic_context = file_path.stem.replace("_", " ").replace("-", " ")
                row_text = f"Sumber {topic_context} -> "
                row_details = ", ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                full_content = row_text + row_details
                if len(full_content.strip()) > 10:
                    all_chunks.append(Document(
                        page_content=full_content,
                        metadata={
                            "source": file_path.name, 
                            "topic": topic_context,
                            "type": "tabular"
                        }
                    ))

        #LANGKAH 2: Chunking
        if content:
            # Algoritma sederhana: memotong berdasarkan karakter dengan overlap
            for i in range(0, len(content), CHUNK_SIZE - CHUNK_OVERLAP):
                chunk_text = content[i : i + CHUNK_SIZE]
                if len(chunk_text.strip()) > 50: # Hindari chunk kosong/terlalu pendek
                    all_chunks.append(Document(
                        page_content=chunk_text,
                        metadata={"source": file_path.name}
                    ))

    print(f"   {len(all_chunks)} chunk berhasil dibuat dari folder data/")

    # ─── LANGKAH 3: Embedding Model ───
    embedding_model = get_embedding_model()

    # ─── LANGKAH 4: Simpan ke ChromaDB ───
    VS_DIR.mkdir(parents=True, exist_ok=True)
    
    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embedding_model,
        persist_directory=str(VS_DIR)
    )
    
    print("\n" + "=" * 50)
    print("✅ Indexing dan embedding selesai! Data siap digunakan di UI.")
    print("=" * 50)
    
    return vectorstore

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # TODO: Ganti sesuai implementasi yang kalian pilih
    build_index_langchain()

