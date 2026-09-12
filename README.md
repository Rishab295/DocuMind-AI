# DocuMind-AI
RAG Application Project



# 🧠 DocuMind AI

> An AI-powered document and data analysis workspace built with Streamlit, RAG, FAISS, Sentence Transformers, and Groq.

DocuMind AI is a web-based AI assistant that allows users to upload documents and datasets, ask questions, generate study materials, analyze data, and export AI-generated insights.

The application combines **Retrieval-Augmented Generation (RAG)** with **AI-powered data analysis** to provide a simple ChatGPT-style interface for working with personal documents and datasets.

---

## 🚀 Features

### 💬 AI Chat

Upload your documents and interact with them using natural language.

- Ask questions about uploaded documents
- Retrieve relevant document content
- Generate AI-powered answers
- Chat-style interface
- Context-aware responses

### 📚 Study Mode

Turn uploaded educational documents into study material.

- 📄 Document summaries
- ⭐ Important topics
- 🧠 Cheat cards
- ❓ Practice questions
- 📖 AI-generated explanations

### 📊 Data Analysis

Upload CSV or Excel datasets and explore them using an interactive dashboard.

- Dataset overview
- Column statistics
- Missing-value analysis
- Numerical statistics
- Interactive Plotly charts
- Data quality checks
- AI-generated insights

### 📄 Document Processing

Supported file formats:

- PDF
- TXT
- CSV
- XLSX

PDF and text documents can be processed for RAG-based question answering.

### 📥 Export Center

Export generated results and analysis.

- Study materials
- Dataset statistics
- Charts
- AI insights
- PDF reports

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      User           │
                    │  Upload Documents   │
                    │   & Ask Questions   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Streamlit       │
                    │    Web Interface    │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │ Document        │        │ Dataset         │
        │ Processing      │        │ Analysis        │
        └────────┬────────┘        └────────┬────────┘
                 │                          │
                 ▼                          ▼
        ┌─────────────────┐        ┌─────────────────┐
        │ Text Chunking   │        │ Pandas          │
        └────────┬────────┘        └────────┬────────┘
                 │                          │
                 ▼                          ▼
        ┌─────────────────┐        ┌─────────────────┐
        │ Sentence        │        │ Plotly          │
        │ Transformers    │        │ Visualization   │
        └────────┬────────┘        └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ FAISS Vector    │
        │ Search          │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Relevant Context│
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Groq LLM        │
        │ GPT-OSS-120B    │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ AI Response     │
        └─────────────────┘
````

---

# 🧩 Tech Stack

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Core programming language      |
| Streamlit             | Web application and UI         |
| Groq API              | Large Language Model inference |
| GPT-OSS-120B          | AI response generation         |
| Sentence Transformers | Text embeddings                |
| FAISS                 | Vector similarity search       |
| PyPDF                 | PDF text extraction            |
| Pandas                | Data processing                |
| NumPy                 | Numerical computation          |
| Plotly                | Interactive visualizations     |
| ReportLab             | PDF report generation          |
| Kaleido               | Chart image export             |
| OpenPyXL              | Excel file processing          |

---

# 🔎 How RAG Works in DocuMind AI

DocuMind AI uses **Retrieval-Augmented Generation (RAG)** to answer questions based on uploaded documents.

### Step 1 — Upload

The user uploads a PDF or text document.

### Step 2 — Extract Text

The application extracts text from the uploaded document.

### Step 3 — Chunking

The document is divided into smaller chunks so that relevant information can be retrieved efficiently.

### Step 4 — Generate Embeddings

Each text chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

### Step 5 — Store in FAISS

The embeddings are stored in a FAISS vector index.

### Step 6 — User Question

The user asks a question about the uploaded document.

### Step 7 — Similarity Search

The question is converted into an embedding and compared with the document embeddings.

The most relevant chunks are retrieved.

### Step 8 — Generate Answer

The retrieved context is provided to the Groq-powered LLM.

The model generates the final answer using the relevant document information.

---

# 📂 Project Structure

```text
DocuMind-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml        # Local only - NOT uploaded to GitHub
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/Rishab295/DocuMind-AI.git
```

Navigate into the project:

```bash
cd DocuMind-AI
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 API Configuration

DocuMind AI uses the Groq API for AI generation.

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

**Never commit this file to GitHub.**

The `.gitignore` file already excludes:

```text
.streamlit/secrets.toml
```

---

# ▶️ Run Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

Or:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

---

# ☁️ Deployment

DocuMind AI can be deployed using Streamlit Community Cloud.

### Deployment steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select:

```text
Repository: Rishab295/DocuMind-AI
Branch: main
Main file: app.py
```

5. Add the API key under Streamlit Secrets:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

6. Deploy the application.

---

# 📊 Supported Data Files

DocuMind AI supports:

```text
CSV
XLSX
```

The application can provide:

* Dataset dimensions
* Data types
* Missing values
* Numerical statistics
* Interactive charts
* Data quality analysis
* AI-generated insights

---

# 📚 Supported Document Files

The RAG system supports:

```text
PDF
TXT
```

Users can upload documents and ask questions about their content.

---

# 🛡️ Security

API keys should never be stored directly inside the source code.

Use Streamlit secrets:

```text
.streamlit/secrets.toml
```

This file is excluded from Git using `.gitignore`.

For deployment, add the secret through the hosting platform's secret management system.

---

# 🎯 Use Cases

DocuMind AI can be used for:

* 📚 Student study assistance
* 📄 Research document analysis
* 📖 Educational material analysis
* 📊 Dataset exploration
* 📈 Business data analysis
* 🧾 Report generation
* 🔎 Document question answering
* 🧠 AI-powered knowledge retrieval

---

# 🔮 Future Improvements

Possible future improvements include:

* Multi-document conversations
* Conversation history
* Source citations
* Page-level PDF references
* DOCX support
* PPTX support
* Image/document OCR
* Authentication
* User accounts
* Cloud document storage
* Database integration
* Advanced analytics
* Voice interaction
* Streaming AI responses

---

# 🧪 Project Status

```text
Status: Active Development
Version: 1.0
```

The current version focuses on document-based RAG, study assistance, dataset analysis, and report generation.

---

# 👨‍💻 Author

**Rishab Das**

GitHub:

[https://github.com/Rishab295](https://github.com/Rishab295)

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project is intended for educational and portfolio purposes.

````

### One small correction

Since your GitHub repository is currently **private**, you can leave the README as-is. If you later make the repository public, this README will already look appropriate as a portfolio project.

After replacing your `README.md`, run:

```powershell
git add README.md
git commit -m "Improve project documentation"
````

Then we'll finish the GitHub push and get your **DocuMind AI live on Streamlit Cloud**.
