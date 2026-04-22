"""
=============================================================
PIPELINE QUERY — RAG UTS Data Engineering
=============================================================

Pipeline ini dijalankan setiap kali user mengajukan pertanyaan:
1. Ubah pertanyaan user ke vektor (query embedding)
2. Cari chunk paling relevan dari vector database (retrieval)
3. Gabungkan konteks + pertanyaan ke dalam prompt
4. Kirim ke LLM untuk mendapatkan jawaban

Jalankan CLI dengan: python src/query.py
=============================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
TOP_K         = int(os.getenv("TOP_K", 3))
VS_DIR        = Path(os.getenv("VECTORSTORE_DIR", "./vectorstore"))
LLM_MODEL     = os.getenv("LLM_MODEL_NAME", "llama3-8b-8192")


# =============================================================
# TODO MAHASISWA:
# Pilih implementasi yang sesuai dengan pilihan LLM kalian
# =============================================================


# def load_vectorstore():
#     """Memuat vector database yang sudah dibuat oleh indexing.py"""
#     from langchain_community.embeddings import HuggingFaceEmbeddings
#     from langchain_community.vectorstores import Chroma

#     if not VS_DIR.exists():
#         raise FileNotFoundError(
#             f"Vector store tidak ditemukan di '{VS_DIR}'.\n"
#             "Jalankan dulu: python src/indexing.py"
#         )

#     embedding_model = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
#         model_kwargs={"device": "cpu"}
#     )

#     vectorstore = Chroma(
#         persist_directory=str(VS_DIR),
#         embedding_function=embedding_model
#     )
#     return vectorstore

#Percobaan1
def load_vectorstore():
    
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from embedding import get_embedding_model

    embedding_model = get_embedding_model()

    vectorstore = Chroma(
        persist_directory=str(VS_DIR),
        embedding_function=embedding_model
    )
    return vectorstore


def retrieve_context(vectorstore, question: str, top_k: int = TOP_K) -> list:
    """
    LANGKAH 1 & 2: Query embedding + Similarity search.
    
    Fungsi ini:
    - Mengubah pertanyaan ke vektor
    - Mencari top_k chunk paling relevan
    - Mengembalikan list dokumen relevan
    """
    results = vectorstore.similarity_search_with_score(question, k=top_k)
    
    contexts = []
    for doc, score in results:
        contexts.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "score": round(float(score), 4)
        })
    
    return contexts


def build_prompt(question: str, contexts: list) -> str:
    """
    LANGKAH 3: Membangun prompt untuk LLM.
    
    Prompt yang baik untuk RAG harus:
    - Memberikan instruksi jelas ke LLM
    - Menyertakan konteks yang sudah diambil
    - Menanyakan pertanyaan user
    - Meminta LLM untuk jujur jika tidak tahu
    
    TODO: Modifikasi prompt ini sesuai domain dan bahasa proyek kalian!
    """
    context_text = "\n\n---\n\n".join(
        [f"[Sumber: {c['source']}]\n{c['content']}" for c in contexts]
    )

    prompt = f"""Kamu adalah asisten yang membantu menjawab pertanyaan berdasarkan dokumen yang diberikan.

INSTRUKSI:
- Jawab HANYA berdasarkan konteks di bawah ini
- Jika jawaban tidak ada dalam konteks, katakan "Saya tidak menemukan informasi tersebut dalam dokumen yang tersedia"
- Jawab dalam Bahasa Indonesia yang jelas dan ringkas
- KORELASIKAN HUBUNGKAN DAN KORELASIKAN informasi sesuai konteks
- BUATLAH KESIMPULAN yang logis sesuai pertanyaan dan konteks
- Jangan mengarang informasi yang tidak ada di konteks

KONTEKS:
{context_text}

PERTANYAAN:
{question}

JAWABAN:"""
    
    return prompt

# ─────────────────────────────────────────────────────────────
# OPSI LLM B: Google Gemini (gratis tier)
# ─────────────────────────────────────────────────────────────
def get_answer_gemini(prompt: str) -> str:
    from google import genai
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    return response.text

def answer_question(question: str, vectorstore=None) -> dict:
    """
    Fungsi utama: menerima pertanyaan, mengembalikan jawaban + konteks.
    Returns:
        dict dengan keys: answer, contexts, prompt
    """
    if vectorstore is None:
        vectorstore = load_vectorstore()
    
    # Retrieve
    print(f"🔍 Mencari konteks relevan untuk: '{question}'")
    contexts = retrieve_context(vectorstore, question)
    print(f"   ✅ {len(contexts)} chunk relevan ditemukan")
    
    # Build prompt
    prompt = build_prompt(question, contexts)
    
    # Generate answer
    print("🤖 Mengirim ke LLM...")
    
    # TODO: Ganti sesuai LLM yang kalian pilih
    # answer = get_answer_groq(prompt)
    answer = get_answer_gemini(prompt)
    # answer = get_answer_ollama(prompt)
    
    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "prompt": prompt
    }


# ─── CLI Interface ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  🤖 RAG System — UTS Data Engineering")
    print("  Ketik 'keluar' untuk mengakhiri")
    print("=" * 55)

    try:
        vs = load_vectorstore()
        print("✅ Vector database berhasil dimuat\n")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        exit(1)

    while True:
        print()
        question = input("❓ Pertanyaan Anda: ").strip()
        
        if question.lower() in ["keluar", "exit", "quit", "q"]:
            print("👋 Sampai jumpa!")
            break
        
        if not question:
            print("⚠️  Pertanyaan tidak boleh kosong.")
            continue
        
        try:
            result = answer_question(question, vs)
            
            print("\n" + "─" * 55)
            print("💬 JAWABAN:")
            print(result["answer"])
            
            print("\n📚 SUMBER KONTEKS:")
            for i, ctx in enumerate(result["contexts"], 1):
                print(f"  [{i}] Skor: {ctx['score']:.4f} | {ctx['source']}")
                print(f"      {ctx['content'][:100]}...")
            print("─" * 55)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Pastikan API key sudah diatur di file .env")
