# 🤖 RAG Starter Pack — UTS Data Engineering

> **Retrieval-Augmented Generation** — Sistem Tanya-Jawab Cerdas Berbasis Dokumen

Starter pack ini adalah **kerangka awal** proyek RAG untuk UTS Data Engineering D3/D4.
Mahasiswa mengisi, memodifikasi, dan mengembangkan kode ini sesuai topik kelompok masing-masing.

---

## 👥 Identitas Kelompok

| Nama | NIM | Tugas Utama |
|------|-----|-------------|
| Edwin Nur Cahyo  | 244311012 | Data Enginner         |
| Dheandra Khoirunnisa Pambudi  | 244311009 | Data Analysist         |
| Julyo Firnanda  | 244311016 | Project Manager         |

**Topik Domain:** *(Bisnis)*  
**Stack yang Dipilih:** *(LangChain)*  
**LLM yang Digunakan:** *(Gemini)*  
**Vector DB yang Digunakan:** *(ChromaDB)*

---

## 🗂️ Struktur Proyek

```
rag-uts-kelompok5/
├── data/                    # Dokumen sumber Anda (PDF, TXT, dll.)
│   └── sample.txt           # Contoh dokumen (ganti dengan dokumen Anda)
├── src/
│   ├── indexing.py          # 🔧 WAJIB DIISI: Pipeline indexing
│   ├── query.py             # 🔧 WAJIB DIISI: Pipeline query & retrieval
│   ├── embeddings.py        # 🔧 WAJIB DIISI: Konfigurasi embedding
│   └── utils.py             # Helper functions
├── ui/
│   └── app.py               # 🔧 WAJIB DIISI: Antarmuka Streamlit
├── docs/
│   └── arsitektur.png       # 📌 Diagram arsitektur (buat sendiri)
├── evaluation/
│   └── hasil_evaluasi.xlsx  # 📌 Tabel evaluasi 10 pertanyaan
├── notebooks/
│   └── 01_demo_rag.ipynb    # Notebook demo dari hands-on session
├── .env.example             # Template environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚡ Cara Memulai (Quickstart)

### 1. Clone & Setup

```bash
# Clone repository ini
git clone https://github.com/[username]/rag-uts-[kelompok].git
cd rag-uts-[kelompok]

# Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# atau: venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Konfigurasi API Key

```bash
# Salin template env
cp .env.example .env

# Edit .env dan isi API key Anda
# JANGAN commit file .env ke GitHub!
```

### 3. Siapkan Dokumen

Letakkan dokumen sumber Anda di folder `data/`:
```bash
# Contoh: salin PDF atau TXT ke folder data
cp dokumen-saya.pdf data/
```

### 4. Jalankan Indexing (sekali saja)

```bash
python src/indexing.py
```

### 5. Jalankan Sistem RAG

```bash
# Dengan Streamlit UI
streamlit run ui/app.py

# Atau via CLI
python src/query.py
```

---

## 🔧 Konfigurasi

Semua konfigurasi utama ada di `src/config.py` (atau langsung di setiap file):

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `CHUNK_SIZE` | 500 | Ukuran setiap chunk teks (karakter) |
| `CHUNK_OVERLAP` | 50 | Overlap antar chunk |
| `TOP_K` | 3 | Jumlah dokumen relevan yang diambil |
| `MODEL_NAME` | *Gemini* | Nama model LLM yang digunakan |

---

## 📊 Hasil Evaluasi

*(Isi setelah pengujian selesai)*

| # | Pertanyaan | Jawaban Sistem | Jawaban Ideal | Skor (1-5) |
|---|-----------|----------------|---------------|-----------|
| 1 | Data jumlah penumpang kereta api pada Non-Jabodetabek bulan Januari | Berdasarkan konteks yang tersedia, jumlah penumpang kereta api di Non Jabodetabek pada bulan  Januari adalah  7.763 orang | Jumlah penumpang KAI Non-Jabodetabek bulan Januari ialah sebanyak 7.763  | 5 |
| 2 | Berapa banyak jumlah penumpang kereta api pada bulan juni di daerah Jabodetabek berdasarkan data csv? | berdasarkan dokumen yang tersedia, jumlah penumpang kereta api di daerah Jabodetabek pada bulan Juni adalah 28.205. | Jumlah penumpang KAI pada bulan Juni di daerah Jabodetabek ialah sebanyak 28.205 jiwa. | 5 |
| 3 | Inflasi bulanan pada bulan Maret di tahun 2025 | - | Sesuai dengan data, inflasi bulanan pada bulan Maret tahun 2025 menyentuh angka 1,65% | 1 |
| 4 | Berapa nilai inflasi bulanan (M-to-M) untuk DKI Jakarta pada bulan Oktober 2025? | Dokumen yang diberikan hanya memuat data laju inflasi tahunan dan pertumbuhan ekonomi nasional (Indonesia) untuk periode tahun 2018 hingga 2022, serta tidak mencantumkan data bulanan (M-to-M), data spesifik wilayah DKI Jakarta, maupun proyeksi data untuk tahun 2025. | Data variatif, di antaranya Oktober (0,31%). | 2 |
| 5 | Berapa banyak total Penumpang Kereta Api di daerah bagian Jawa (Jabodetabek+Non Jabodetabek) di bulan Agustus 2025? | Berdasarkan data yang tersedia, jumlah penumpang kereta api di daerah Jawa (Jabodetabek+Non Jabodetabek) pada bulan Agustus 2025 adalah sebanyak 36.694 orang. | Pada data Jumlah Penumpang Kereta Api pada Jawa (Jabodetabek+Non Jabodetabek) di bulan Agustus 2025 ialah 36.694 | 5 |
| 6 | Dalam artikel "Pengaruh Inflasi Terhadap Pertumbuhan Ekonomi", apa indikator penting dari kemajuan perekonomian suatu negara? | Berdasarkan konteks yang diberikan, indikator penting dari kemajuan perekonomian suatu negara adalah pertumbuhan ekonomi | Pertumbuhan ekonomi. | 5 |
| 7 | Berapa total seluruh penumpang kereta api di Indonesia pada bulan Juni 2025 menurut tabel data? | Berdasarkan konteks yang diberikan, dokumen hanya menyebutkan bahwa data penumpang kereta api dikumpulkan dari situs web BPS Indonesia dengan fokus pada wilayah Jawa (tidak termasuk Jabodetabek) dan merujuk pada "Tabel 1" untuk daftar variabel. Namun, nilai data spesifik untuk jumlah penumpang pada bulan Juni 2025 tidak dicantumkan dalam teks tersebut. | Pada data Jumlah Penumpang Kereta Api di Indonesia bulan Juni 2025 ialah 45.614 | 2 |
| 8 | Apa pengaruh Inflasi Terhadap Pertumbuhan Ekonomi? | Berdasarkan konteks yang diberikan, pengaruh inflasi terhadap pertumbuhan ekonomi adalah sebagai berikut: Mempengaruhi Kebijakan Negara & Menjaga Keseimbangan Pertumbuhan | Inflasi yang rendah dan stabil akan meningkatkan pertumbuhan ekonomi, sedangkan inflasi yang tidak stabil atau terlalu tinggi akan memperburuknya. | 4 |
| 9 | Dalam artikel mengenai peramalan penumpang kereta api, apa kepanjangan dari metode "MAPE" yang digunakan untuk mengukur akurasi? | Saya tidak menemukan informasi mengenai kepanjangan dari metode "MAPE" dalam dokumen yang tersedia. Dokumen tersebut hanya menyebutkan bahwa MAPE dan RMSE digunakan sebagai alat untuk mengevaluasi hasil peramalan tanpa memberikan rincian kepanjangannya. | Mean Absolute Percentage Error. | 2 |
| 10 | Berapa jumlah penumpang kereta api Non JabodetabeK pada bulan November 2025? | Berdasarkan konteks yang tersedia, jumlah penumpang kereta api Non Jabodetabek (Jawa) pada bulan November 2025 adalah sebanyak 7.970 orang. | Jumlah penumpang KAI (Non Jabodetabek (Jawa)) pada bulan November 2025 sebanyak 7.970 | 5 |

**Rata-rata Skor:** 3,6  
**Analisis:** Ketergantungan pada kualitas dokumen, Jawaban masih bersifat generatif, Prompt tidak spesifik, Belum ada evaluasi otomatis, Performa tergantung konfigurasi

---

## 🏗️ Arsitektur Sistem

![Diagram Arsitektur](https://github.com/edwinyxxz/RAG-UTS-Kelompok_5/blob/main/Arsitektur%20Sistem.drawio%20(4).png)

```
[Dokumen] → [Loader] → [Splitter] → [Embedding] → [Vector DB]
                                                         ↕
[User Query] → [Query Embed] → [Retriever] → [Prompt] → [LLM] → [Jawaban]
```

---

## 📚 Referensi & Sumber

- Framework: *(LangChain docs / LlamaIndex docs)*
- LLM: *(Groq / Gemini / Ollama)*
- Vector DB: *(ChromaDB / FAISS docs)*

---

## 👨‍🏫 Informasi UTS

- **Mata Kuliah:** Data Engineering
- **Program Studi:** D4 Teknologi Rekayasa Perangkat Lunak
- **Deadline:** *23 April 2026*
