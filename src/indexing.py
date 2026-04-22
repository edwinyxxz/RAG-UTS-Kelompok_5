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


# ─────────────────────────────────────────────────────────────
# IMPLEMENTASI A: LangChain + ChromaDB (REKOMENDASI PEMULA)
# ─────────────────────────────────────────────────────────────

# def build_index_langchain():
#     """
#     Membangun index menggunakan LangChain dan ChromaDB.
    
#     Komponen yang digunakan:
#     - DirectoryLoader: memuat semua file dari folder data/
#     - RecursiveCharacterTextSplitter: memecah dokumen jadi chunk
#     - HuggingFaceEmbeddings: mengubah teks ke vektor (GRATIS, offline)
#     - Chroma: vector database lokal
#     """
#     from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
#     from langchain.text_splitter import RecursiveCharacterTextSplitter
#     from langchain_community.embeddings import HuggingFaceEmbeddings
#     from langchain_community.vectorstores import Chroma

#     print("=" * 50)
#     print("Memulai Pipeline Indexing (LangChain)")
#     print("=" * 50)

#     # ─── LANGKAH 1: Load Dokumen ─────────────────────────────
#     print("\n📄 Langkah 1: Memuat dokumen...")
    
#     # TODO: Sesuaikan dengan format dokumen kalian
#     # Untuk TXT:
#     loader = DirectoryLoader(
#         str(DATA_DIR),
#         glob="**/*.txt",
#         loader_cls=TextLoader,
#         loader_kwargs={"encoding": "utf-8"},
#         show_progress=True
#     )
    
#     # Untuk PDF (uncomment jika butuh):
#     # loader = DirectoryLoader(str(DATA_DIR), glob="**/*.pdf", loader_cls=PyPDFLoader)
    
#     documents = loader.load()
#     print(f"   {len(documents)} dokumen berhasil dimuat")
#     print(f"   Total karakter: {sum(len(d.page_content) for d in documents):,}")

#     # ─── LANGKAH 2: Chunking ─────────────────────────────────
#     print(f"\n  Langkah 2: Memecah dokumen (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=CHUNK_SIZE,
#         chunk_overlap=CHUNK_OVERLAP,
#         length_function=len,
#         separators=["\n\n", "\n", ".", " ", ""]
#     )
#     chunks = splitter.split_documents(documents)
    
#     print(f"  {len(chunks)} chunk berhasil dibuat")
#     print(f"  Rata-rata ukuran chunk: {sum(len(c.page_content) for c in chunks) // len(chunks)} karakter")
    
#     # Tampilkan contoh chunk pertama
#     print(f"\n   Contoh chunk pertama:")
#     print(f"   {'-'*40}")
#     print(f"   {chunks[0].page_content[:200]}...")

#     # ─── LANGKAH 3: Embedding ────────────────────────────────
#     print("\n Langkah 3: Membuat embedding (model lokal, tanpa API key)...")
    
#     # Model gratis dari HuggingFace, berjalan offline
#     # Alternatif model: 'paraphrase-multilingual-MiniLM-L12-v2' (mendukung Bahasa Indonesia)
#     embedding_model = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
#         model_kwargs={"device": "cpu"}
#     )
#     print("    Embedding model siap (multilingual, mendukung Bahasa Indonesia)")

#     # ─── LANGKAH 4: Simpan ke Vector DB ──────────────────────
#     print(f"\n️  Langkah 4: Menyimpan ke ChromaDB ({VS_DIR})...")
    
#     VS_DIR.mkdir(parents=True, exist_ok=True)
    
#     vectorstore = Chroma.from_documents(
#         documents=chunks,
#         embedding=embedding_model,
#         persist_directory=str(VS_DIR)
#     )
    
#     print(f"    {len(chunks)} chunk tersimpan di vector database")
#     print("\n" + "=" * 50)
#     print(" Indexing selesai! Vector database siap digunakan.")
#     print(f"   Lokasi: {VS_DIR.absolute()}")
#     print("=" * 50)
    
#     return vectorstore

# ─────────────────────────────────────────────────────────────
# IMPLEMENTASI B: From Scratch (tanpa LangChain)
# Uncomment blok ini jika memilih opsi from scratch
# ─────────────────────────────────────────────────────────────

# def build_index_scratch():
#     # """Implementasi RAG dari scratch menggunakan sentence-transformers + FAISS."""
#     import json
#     import numpy as np
#     from sentence_transformers import SentenceTransformer
#     import Chroma

#     print(" Memulai Pipeline Indexing (From Scratch)")

#     # Load dokumen
#     documents = []
#     for file_path in DATA_DIR.glob("**/*.txt"):
#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()
#             documents.append({"source": str(file_path), "content": content})
#     print(f" {len(documents)} dokumen dimuat")

#     # Chunking manual
#     chunks = []
#     for doc in documents:
#         text = doc["content"]
#         for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP):
#             chunk_text = text[i:i + CHUNK_SIZE]
#             if len(chunk_text) > 50:
#                 chunks.append({"source": doc["source"], "text": chunk_text, "id": len(chunks)})
#     print(f" {len(chunks)} chunk dibuat")

#     # Embedding
#     model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
#     texts = [c["text"] for c in chunks]
#     embeddings = model.encode(texts, show_progress_bar=True)
#     print(f" Embedding selesai, dimensi: {embeddings.shape}")
    
#     #Simpan Ke ChromaDB
# #     print(f"\n️  Langkah 4: Menyimpan ke ChromaDB ({VS_DIR})...")
    
#     VS_DIR.mkdir(parents=True, exist_ok=True)
#     vectorstore = Chroma.from_documents(
#         documents=chunks,
#         embedding=embedding_model,
#         persist_directory=str(VS_DIR)
#     )
    
#     print(f"    {len(chunks)} chunk tersimpan di vector database")
#     print("\n" + "=" * 50)
#     print(" Indexing selesai! Vector database siap digunakan.")
#     print(f"   Lokasi: {VS_DIR.absolute()}")
#     print("=" * 50)

#     return vectorstore

    # Simpan ke FAISS
    # VS_DIR.mkdir(parents=True, exist_ok=True)
    # index = faiss.IndexFlatL2(embeddings.shape[1])
    # index.add(embeddings.astype("float32"))
    # faiss.write_index(index, str(VS_DIR / "index.faiss"))

    # Simpan metadata
    # with open(VS_DIR / "chunks.json", "w", encoding="utf-8") as f:
    #     json.dump(chunks, f, ensure_ascii=False, indent=2)

    # print(f" Index FAISS tersimpan di {VS_DIR}")

#Percobaan1
def build_index_scratch():
    """
    Implementasi RAG: Manual Chunking (Scratch) + ChromaDB.
    Mendukung format TXT, PDF, dan CSV.
    """
    import pandas as pd
    from PyPDF2 import PdfReader
    from langchain_core.documents import Document
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma

    print("=" * 50)
    print("Memulai Pipeline Indexing (Scratch + ChromaDB)")
    print("=" * 50)

    # ─── LANGKAH 1: Load Dokumen (Multi-format) ───
    print("\n📄 Langkah 1: Memuat dokumen...")
    all_chunks = []

    for file_path in DATA_DIR.rglob("*"):
        if file_path.name.startswith('.'): continue # Lewati file tersembunyi
        
        content = ""
        if file_path.suffix == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                content += page.extract_text() + "\n"
        elif file_path.suffix == ".csv":
            df = pd.read_csv(file_path)
            content = df.to_string()

        # ─── LANGKAH 2: Chunking Manual (Scratch) ───
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
    print("\n🧬 Langkah 3: Menyiapkan model embedding...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"}
    )

    # ─── LANGKAH 4: Simpan ke ChromaDB ───
    print(f"\n📥 Langkah 4: Menyimpan ke ChromaDB ({VS_DIR})...")
    VS_DIR.mkdir(parents=True, exist_ok=True)
    
    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embedding_model,
        persist_directory=str(VS_DIR)
    )
    
    print("\n" + "=" * 50)
    print("✅ Indexing selesai! Data siap digunakan di UI.")
    print("=" * 50)
    
    return vectorstore

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # TODO: Ganti sesuai implementasi yang kalian pilih
    # build_index_langchain()
    
    # Atau jika from scratch:
    build_index_scratch()
