import io
import html

import faiss
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS — SAME DARK UI
# ============================================================

st.markdown(
    """
<style>
.stApp { background: #0b0f17; }

.main .block-container {
    max-width: 1450px;
    padding-top: 28px;
    padding-bottom: 60px;
    padding-left: 42px;
    padding-right: 42px;
}

[data-testid="stSidebar"] {
    background: #0f141d;
    border-right: 1px solid #202735;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 25px; }

.sidebar-brand {
    font-size: 25px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.5px;
}
.sidebar-subtitle {
    color: #8b95a7;
    font-size: 13px;
    margin-top: 5px;
    margin-bottom: 25px;
}
.sidebar-label {
    color: #697386;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 20px;
    margin-bottom: 10px;
}

[data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] [role="radio"] {
    padding: 10px 12px;
    border-radius: 9px;
    color: #aeb7c7;
}
[data-testid="stSidebar"] [role="radio"]:hover {
    background: #171e2a;
    color: #ffffff;
}
[data-testid="stSidebar"] [role="radio"][aria-checked="true"] {
    background: #1d2635;
    color: #ffffff;
}

.hero {
    background:
        radial-gradient(circle at 90% 10%, rgba(99, 102, 241, 0.18), transparent 30%),
        linear-gradient(135deg, #141b28, #10151f);
    border: 1px solid #252e3d;
    border-radius: 22px;
    padding: 34px 38px;
    margin-bottom: 28px;
}
.hero-title {
    font-size: 38px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -1.2px;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 16px;
    color: #9ca7b8;
    line-height: 1.6;
}

.page-title {
    font-size: 31px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.8px;
    margin-bottom: 5px;
}
.page-subtitle {
    color: #8d98aa;
    font-size: 14px;
    margin-bottom: 24px;
}

.feature-card {
    background: #121823;
    border: 1px solid #232c3a;
    border-radius: 17px;
    padding: 25px;
    min-height: 165px;
    transition: 0.2s ease;
}
.feature-card:hover {
    border-color: #3a4659;
    transform: translateY(-2px);
}
.feature-icon { font-size: 27px; margin-bottom: 15px; }
.feature-title {
    font-size: 18px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 7px;
}
.feature-text {
    color: #8e99ab;
    font-size: 13px;
    line-height: 1.6;
}

.metric-card {
    background: #121823;
    border: 1px solid #232c3a;
    border-radius: 15px;
    padding: 20px;
}
.metric-number {
    color: #f8fafc;
    font-size: 28px;
    font-weight: 800;
}
.metric-label {
    color: #7f8a9d;
    font-size: 12px;
    margin-top: 3px;
}

.section-title {
    color: #f1f5f9;
    font-size: 21px;
    font-weight: 750;
    margin-top: 28px;
    margin-bottom: 14px;
}

.info-card {
    background: #111824;
    border: 1px solid #263143;
    border-radius: 13px;
    padding: 17px 20px;
    margin-bottom: 12px;
}
.info-title {
    color: #e5e7eb;
    font-weight: 700;
    font-size: 15px;
}
.info-text {
    color: #8d98aa;
    font-size: 13px;
    margin-top: 5px;
}

.topic-card {
    background: #121823;
    border: 1px solid #252e3c;
    border-left: 4px solid #6366f1;
    border-radius: 11px;
    padding: 16px 18px;
    margin-bottom: 10px;
}
.topic-number {
    color: #818cf8;
    font-size: 12px;
    font-weight: 700;
}
.topic-name {
    color: #f1f5f9;
    font-size: 16px;
    font-weight: 700;
}

.cheat-card {
    background: #121823;
    border: 1px solid #293344;
    border-radius: 15px;
    padding: 21px;
    margin-bottom: 14px;
}
.cheat-label {
    color: #818cf8;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.cheat-question {
    color: #f8fafc;
    font-size: 17px;
    font-weight: 700;
    margin-top: 7px;
}
.cheat-answer {
    color: #9ba6b7;
    font-size: 14px;
    line-height: 1.6;
    margin-top: 10px;
}

.file-card {
    background: #121823;
    border: 1px solid #252e3b;
    border-radius: 10px;
    padding: 11px 13px;
    margin-bottom: 7px;
    color: #cbd5e1;
    font-size: 13px;
}

.chat-source {
    background: #111824;
    border: 1px solid #283344;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 8px;
    color: #9ca7b8;
    font-size: 12px;
}

.stButton > button {
    border-radius: 9px;
    border: 1px solid #303b4d;
    background: #171f2c;
    color: #e5e7eb;
    font-weight: 600;
    min-height: 42px;
}
.stButton > button:hover {
    border-color: #6366f1;
    color: #ffffff;
    background: #1b2433;
}

.stDownloadButton > button {
    border-radius: 10px;
    background: #6366f1;
    color: white;
    border: none;
    font-weight: 700;
    min-height: 45px;
}
.stDownloadButton > button:hover { background: #5558d9; }

[data-testid="stDataFrame"] {
    border: 1px solid #283344;
    border-radius: 12px;
}

hr { border-color: #232c3a !important; }

[data-testid="stExpander"] {
    background: #111824;
    border: 1px solid #273143;
    border-radius: 12px;
}

.stCaption { color: #7f8a9d !important; }

[data-testid="stFileUploader"] {
    background: #111824;
    border-radius: 13px;
    border: 1px dashed #354155;
    padding: 5px;
}

button[data-baseweb="tab"] { color: #8e99ab; }
button[data-baseweb="tab"][aria-selected="true"] { color: #ffffff; }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "documents": [],
    "chunks": [],
    "index": None,
    "embeddings": None,
    "chat_history": [],
    "study_material": {},
    "dataframe": None,
    "dataset_name": "",
    "charts": [],
    "processed_files": set(),
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# GROQ AI
# ============================================================

def ask_ai(prompt):
    """Call the hosted Groq model using the Streamlit secret."""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return (
            "⚠️ GROQ_API_KEY is not configured.\n\n"
            "Create `.streamlit/secrets.toml` and add:\n\n"
            'GROQ_API_KEY = "YOUR_NEW_GROQ_API_KEY"'
        )

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are DocuMind AI, a precise and helpful document "
                        "and data assistant. Follow the user's requested format. "
                        "Never invent facts when the prompt says to use supplied data only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=3000,
        )

        return response.choices[0].message.content

    except Exception as e:
        return (
            "⚠️ I couldn't connect to the Groq AI service.\n\n"
            "Check that your GROQ_API_KEY is valid and that your selected "
            "Groq model is available.\n\n"
            f"Technical error: {e}"
        )


# ============================================================
# DOCUMENT EXTRACTION
# ============================================================

def extract_pdf(file):
    reader = PdfReader(file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"text": text, "page": page_number})

    return pages


def extract_text_file(file):
    content = file.read()

    try:
        text = content.decode("utf-8")
    except Exception:
        text = content.decode("latin-1", errors="ignore")

    return [{"text": text, "page": 1}]


# ============================================================
# CHUNKING + RAG
# ============================================================

def split_text(text, chunk_size=1000, overlap=200):
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    step = max(1, chunk_size - overlap)

    while start < len(text):
        chunk = text[start:start + chunk_size]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += step

    return chunks


def process_document(file):
    filename = file.name
    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "pdf":
        pages = extract_pdf(file)
    elif extension == "txt":
        pages = extract_text_file(file)
    else:
        return 0

    added = 0

    for page in pages:
        for chunk in split_text(page["text"]):
            st.session_state.chunks.append(
                {
                    "text": chunk,
                    "source": filename,
                    "page": page["page"],
                }
            )
            added += 1

    if filename not in st.session_state.documents:
        st.session_state.documents.append(filename)

    return added


def build_index():
    if not st.session_state.chunks:
        st.session_state.index = None
        st.session_state.embeddings = None
        return

    model = load_embedding_model()
    texts = [item["text"] for item in st.session_state.chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype("float32")

    # Cosine similarity through normalized vectors + inner product.
    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    st.session_state.embeddings = embeddings
    st.session_state.index = index


def retrieve_documents(question, k=5):
    if st.session_state.index is None:
        return []

    model = load_embedding_model()

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    _, indices = st.session_state.index.search(
        query_embedding,
        min(k, len(st.session_state.chunks)),
    )

    return [
        st.session_state.chunks[idx]
        for idx in indices[0]
        if 0 <= idx < len(st.session_state.chunks)
    ]


def answer_question(question):
    results = retrieve_documents(question)

    if not results:
        return "Please upload and process a PDF or TXT document first.", []

    context_parts = []

    for result in results:
        context_parts.append(
            f"SOURCE: {result['source']}\n"
            f"PAGE: {result['page']}\n\n"
            f"{result['text']}"
        )

    context = "\n\n-------------------------\n\n".join(context_parts)

    # Keep chat requests small enough for Groq's standard on-demand TPM limit.
    # Five 1,000-character chunks are already enough for a basic RAG answer.
    context = context[:10000]

    prompt = f"""
Answer the user's question using ONLY the supplied document context.

Rules:
- Do not invent information.
- If the answer is not supported by the documents, clearly say that.
- Explain clearly and naturally.
- When useful, mention the document name and page number.
- Do not claim to have read anything outside the supplied context.

QUESTION:
{question}

DOCUMENT CONTEXT:
{context}
"""

    return ask_ai(prompt), results


def get_document_text(max_chars=10000):
    if not st.session_state.chunks:
        return ""

    parts = []
    total = 0

    for chunk in st.session_state.chunks:
        part = (
            f"\nSOURCE: {chunk['source']}\n"
            f"PAGE: {chunk['page']}\n"
            f"{chunk['text']}\n"
        )

        if total + len(part) > max_chars:
            break

        parts.append(part)
        total += len(part)

    return "".join(parts)


# ============================================================
# STUDY MODE
# ============================================================

def generate_summary():
    document = get_document_text()

    return ask_ai(
        f"""
Create a clear and structured summary of the uploaded document.

Requirements:
- Cover the major concepts.
- Use simple language.
- Preserve important terminology.
- Use headings and bullet points.
- Focus on exam/revision usefulness.
- Use ONLY information from the document.
- Do not invent information.

DOCUMENT:
{document}
"""
    )


def generate_topics():
    document = get_document_text()

    return ask_ai(
        f"""
Read the uploaded document and identify the most important topics.

Use this exact style:

1. Topic Name
   → One-line explanation.

2. Topic Name
   → One-line explanation.

Prioritize concepts useful for revision and exams.
Use ONLY information from the document.

DOCUMENT:
{document}
"""
    )


def generate_cheat_cards():
    document = get_document_text()

    return ask_ai(
        f"""
Create 10 concise study cheat cards from the uploaded document.

Format:

CARD 1
Question: ...
Answer: ...

CARD 2
Question: ...
Answer: ...

Keep answers short and easy to memorize.
Use ONLY information from the document.

DOCUMENT:
{document}
"""
    )


def generate_questions():
    document = get_document_text()

    return ask_ai(
        f"""
Create 10 practice questions based ONLY on the uploaded document.

Include:
- definitions
- concepts
- understanding questions
- exam-style questions

Provide an answer after every question.

DOCUMENT:
{document}
"""
    )


# ============================================================
# DATASET
# ============================================================

def load_dataset(file):
    name = file.name.lower()

    if name.endswith(".csv"):
        return pd.read_csv(file)

    if name.endswith(".xlsx"):
        excel = pd.ExcelFile(file)
        return pd.read_excel(file, sheet_name=excel.sheet_names[0])

    return None


def analyze_dataset(df):
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    categorical = df.select_dtypes(exclude=np.number).columns.tolist()

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric": numeric,
        "categorical": categorical,
        "missing": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
    }


def create_dataset_charts(df):
    charts = []

    numeric = df.select_dtypes(include=np.number).columns.tolist()
    categorical = df.select_dtypes(exclude=np.number).columns.tolist()

    if numeric:
        column = numeric[0]
        charts.append(
            (
                "Distribution",
                px.histogram(
                    df,
                    x=column,
                    title=f"Distribution — {column}",
                    marginal="box",
                ),
            )
        )

    if categorical and numeric:
        category = categorical[0]
        value = numeric[0]

        grouped = (
            df.groupby(category, dropna=False)[value]
            .sum()
            .reset_index()
            .sort_values(value, ascending=False)
            .head(10)
        )

        charts.append(
            (
                "Category Comparison",
                px.bar(
                    grouped,
                    x=category,
                    y=value,
                    title=f"{value} by {category}",
                ),
            )
        )

    if len(numeric) >= 2:
        x, y = numeric[0], numeric[1]

        charts.append(
            (
                "Relationship",
                px.scatter(
                    df,
                    x=x,
                    y=y,
                    title=f"{x} vs {y}",
                ),
            )
        )

        charts.append(
            (
                "Correlation Matrix",
                px.imshow(
                    df[numeric].corr(),
                    text_auto=True,
                    title="Correlation Matrix",
                ),
            )
        )

    return charts


def generate_data_insights(df):
    info = analyze_dataset(df)

    try:
        stats = df.describe(include="all").fillna("").to_string()
    except Exception:
        stats = "Statistical summary unavailable."

    # Avoid sending an unnecessarily huge table to the API.
    stats = stats[:10000]

    return ask_ai(
        f"""
You are a professional data analyst.

Analyze this dataset profile.

Dataset:
{st.session_state.dataset_name}

Rows:
{info['rows']}

Columns:
{info['columns']}

Numeric columns:
{info['numeric']}

Categorical columns:
{info['categorical']}

Missing values:
{info['missing']}

Duplicate rows:
{info['duplicates']}

Statistical summary:
{stats}

Provide:
1. 3–5 important insights.
2. Important patterns.
3. Data quality issues.
4. Columns deserving attention.
5. Useful business questions.

Do not invent facts. Only discuss information supported by the dataset.
"""
    )


# ============================================================
# PDF EXPORT
# ============================================================

def safe_paragraph_text(text):
    if not text:
        return ""

    return html.escape(str(text)).replace("\n", "<br/>")


def generate_pdf():
    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        leading=30,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=17,
        leading=21,
        spaceBefore=15,
        spaceAfter=10,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=8,
    )

    story = [
        Paragraph("DocuMind AI", title_style),
        Paragraph("AI Study & Data Analysis Report", body_style),
        Spacer(1, 15),
    ]

    if st.session_state.documents:
        story.append(Paragraph("Uploaded Documents", heading_style))
        for name in st.session_state.documents:
            story.append(
                Paragraph(
                    safe_paragraph_text(f"• {name}"),
                    body_style,
                )
            )

    study = st.session_state.study_material

    for key, title in [
        ("summary", "Document Summary"),
        ("topics", "Important Topics"),
        ("cheat_cards", "Cheat Cards"),
        ("questions", "Practice Questions"),
    ]:
        if study.get(key):
            story.append(Paragraph(title, heading_style))
            story.append(
                Paragraph(
                    safe_paragraph_text(study[key]),
                    body_style,
                )
            )

    df = st.session_state.dataframe

    if df is not None:
        story.append(PageBreak())
        story.append(Paragraph("Dataset Analysis", heading_style))

        info = analyze_dataset(df)

        table = Table(
            [
                ["Metric", "Value"],
                ["Rows", str(info["rows"])],
                ["Columns", str(info["columns"])],
                ["Missing Values", str(info["missing"])],
                ["Duplicate Rows", str(info["duplicates"])],
            ],
            colWidths=[220, 100],
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#202938")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("PADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )

        story.append(table)
        story.append(Spacer(1, 15))

        for chart_name, fig in st.session_state.charts:
            try:
                image_bytes = pio.to_image(
                    fig,
                    format="png",
                    width=900,
                    height=500,
                )

                story.append(Paragraph(chart_name, heading_style))
                story.append(
                    Image(
                        io.BytesIO(image_bytes),
                        width=500,
                        height=278,
                    )
                )
                story.append(Spacer(1, 12))
            except Exception:
                pass

        if study.get("data_insights"):
            story.append(PageBreak())
            story.append(Paragraph("AI Data Insights", heading_style))
            story.append(
                Paragraph(
                    safe_paragraph_text(study["data_insights"]),
                    body_style,
                )
            )

    document.build(story)
    buffer.seek(0)

    return buffer


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">✦ DocuMind AI</div>
        <div class="sidebar-subtitle">
            Your intelligent document & data workspace
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">Workspace</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "💬 AI Chat",
            "📚 Study Mode",
            "📊 Data Analysis",
            "📄 Documents",
            "📥 Export Center",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-label">Add files</div>',
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Upload",
        type=["pdf", "txt", "csv", "xlsx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files and st.button(
        "⚡ Process Files",
        use_container_width=True,
    ):
        new_files = [
            f for f in uploaded_files
            if f.name not in st.session_state.processed_files
        ]

        if not new_files:
            st.info("These files have already been processed.")

        else:
            processed_count = 0
            chunk_count = 0

            with st.spinner("Processing your files..."):
                for file in new_files:
                    filename = file.name.lower()

                    try:
                        if filename.endswith((".csv", ".xlsx")):
                            df = load_dataset(file)

                            if df is not None:
                                st.session_state.dataframe = df
                                st.session_state.dataset_name = file.name
                                st.session_state.charts = create_dataset_charts(df)
                                processed_count += 1

                        else:
                            added = process_document(file)
                            chunk_count += added
                            processed_count += 1

                        st.session_state.processed_files.add(file.name)

                    except Exception as e:
                        st.error(f"Could not process {file.name}: {e}")

                if st.session_state.chunks:
                    build_index()

            if processed_count:
                st.success(
                    f"{processed_count} file(s) processed • "
                    f"{chunk_count} RAG chunks added."
                )

    st.divider()

    st.caption(f"📄 {len(st.session_state.documents)} documents")
    st.caption(f"🧩 {len(st.session_state.chunks)} RAG chunks")

    if st.session_state.dataframe is not None:
        st.caption(
            f"📊 {len(st.session_state.dataframe):,} dataset rows"
        )


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">✦ Your AI Workspace</div>
            <div class="hero-subtitle">
                Understand documents, create study material,
                analyze datasets and generate professional reports
                — all in one place.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (len(st.session_state.documents), "Documents"),
        (len(st.session_state.chunks), "RAG Chunks"),
        (
            len(st.session_state.dataframe)
            if st.session_state.dataframe is not None
            else 0,
            "Dataset Rows",
        ),
        (len(st.session_state.charts), "Visualizations"),
    ]

    for col, (number, label) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{number:,}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">What would you like to do?</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    features = [
        (
            c1,
            "💬",
            "Ask AI",
            "Chat with your uploaded documents using RAG and hosted AI.",
        ),
        (
            c2,
            "📚",
            "Study Smarter",
            "Turn PDFs into summaries, important topics, cheat cards and questions.",
        ),
        (
            c3,
            "📊",
            "Analyze Data",
            "Upload CSV or Excel files and automatically discover patterns and visualizations.",
        ),
    ]

    for col, icon, title, description in features:
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-text">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Your workspace</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.documents:
        for name in st.session_state.documents:
            st.markdown(
                f"""
                <div class="file-card">
                    📄 {html.escape(name)}
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif st.session_state.dataframe is not None:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">
                    📊 {html.escape(st.session_state.dataset_name)}
                </div>
                <div class="info-text">
                    Dataset ready for analysis.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.info(
            "Upload a PDF, TXT, CSV or Excel file from the sidebar to begin."
        )


# ============================================================
# AI CHAT
# ============================================================

elif page == "💬 AI Chat":
    st.markdown(
        '<div class="page-title">💬 AI Chat</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Ask questions about your uploaded documents.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.chunks:
        st.info("Upload and process a PDF or TXT document first.")
    else:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input(
            "Ask anything about your documents..."
        )

        if question:
            st.session_state.chat_history.append(
                {"role": "user", "content": question}
            )

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Searching your knowledge base..."):
                    answer, sources = answer_question(question)

                st.markdown(answer)

                if sources:
                    with st.expander("📚 View sources"):
                        for source in sources:
                            st.markdown(
                                f"""
                                <div class="chat-source">
                                    <b>📄 {html.escape(source['source'])}</b>
                                    &nbsp; • &nbsp;
                                    Page {source['page']}
                                    <br><br>
                                    {html.escape(source['text'][:450])}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )


# ============================================================
# STUDY MODE
# ============================================================

elif page == "📚 Study Mode":
    st.markdown(
        '<div class="page-title">📚 Study Mode</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Turn your documents into a personalized revision pack.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.chunks:
        st.info("Upload and process a PDF or TXT document first.")
    else:
        tabs = st.tabs(
            [
                "📝 Summary",
                "⭐ Important Topics",
                "🧠 Cheat Cards",
                "❓ Practice Questions",
            ]
        )

        with tabs[0]:
            st.markdown("### 📝 Document Summary")

            if st.button("Generate Summary", use_container_width=True):
                with st.spinner("Creating your summary..."):
                    st.session_state.study_material["summary"] = (
                        generate_summary()
                    )

            if st.session_state.study_material.get("summary"):
                st.markdown(st.session_state.study_material["summary"])

        with tabs[1]:
            st.markdown("### ⭐ Important Topics")
            st.caption(
                "Short, revision-friendly explanations of the most important concepts."
            )

            if st.button(
                "Generate Important Topics",
                use_container_width=True,
            ):
                with st.spinner("Finding important topics..."):
                    st.session_state.study_material["topics"] = (
                        generate_topics()
                    )

            if st.session_state.study_material.get("topics"):
                st.markdown(st.session_state.study_material["topics"])

        with tabs[2]:
            st.markdown("### 🧠 Cheat Cards")
            st.caption(
                "Quick question-and-answer cards for revision."
            )

            if st.button(
                "Generate Cheat Cards",
                use_container_width=True,
            ):
                with st.spinner("Creating cheat cards..."):
                    st.session_state.study_material["cheat_cards"] = (
                        generate_cheat_cards()
                    )

            if st.session_state.study_material.get("cheat_cards"):
                st.markdown(
                    st.session_state.study_material["cheat_cards"]
                )

        with tabs[3]:
            st.markdown("### ❓ Practice Questions")
            st.caption("Test your understanding before an exam.")

            if st.button(
                "Generate Questions",
                use_container_width=True,
            ):
                with st.spinner("Creating practice questions..."):
                    st.session_state.study_material["questions"] = (
                        generate_questions()
                    )

            if st.session_state.study_material.get("questions"):
                st.markdown(
                    st.session_state.study_material["questions"]
                )


# ============================================================
# DATA ANALYSIS
# ============================================================

elif page == "📊 Data Analysis":
    st.markdown(
        '<div class="page-title">📊 Data Analysis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Explore your CSV or Excel dataset automatically.</div>',
        unsafe_allow_html=True,
    )

    df = st.session_state.dataframe

    if df is None:
        st.info("Upload a CSV or Excel file from the sidebar.")
    else:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">
                    📊 {html.escape(st.session_state.dataset_name)}
                </div>
                <div class="info-text">
                    Automatically profiled dataset
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        info = analyze_dataset(df)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Rows", f"{info['rows']:,}")
        with c2:
            st.metric("Columns", info["columns"])
        with c3:
            st.metric("Missing Values", f"{info['missing']:,}")
        with c4:
            st.metric("Duplicates", f"{info['duplicates']:,}")

        st.markdown(
            '<div class="section-title">Dataset Preview</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df, use_container_width=True, height=350)

        tabs = st.tabs(
            [
                "📈 Visualizations",
                "📐 Statistics",
                "🤖 AI Insights",
                "🔍 Data Quality",
            ]
        )

        with tabs[0]:
            if not st.session_state.charts:
                st.warning("No suitable visualizations were detected.")
            else:
                for chart_name, fig in st.session_state.charts:
                    st.markdown(f"### {chart_name}")
                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                    )

        with tabs[1]:
            st.markdown("### 📐 Statistical Summary")
            try:
                statistics = df.describe(include="all").transpose()
                st.dataframe(
                    statistics,
                    use_container_width=True,
                )
            except Exception:
                st.warning(
                    "Statistical summary could not be generated."
                )

        with tabs[2]:
            st.markdown("### 🤖 AI Data Insights")

            if st.button(
                "Analyze Dataset with AI",
                use_container_width=True,
            ):
                with st.spinner("Analyzing dataset..."):
                    st.session_state.study_material["data_insights"] = (
                        generate_data_insights(df)
                    )

            if st.session_state.study_material.get("data_insights"):
                st.markdown(
                    st.session_state.study_material["data_insights"]
                )

        with tabs[3]:
            st.markdown("### 🔍 Data Quality")

            missing = (
                df.isna()
                .sum()
                .sort_values(ascending=False)
            )
            missing = missing[missing > 0]

            if len(missing):
                st.warning("Columns containing missing values:")
                st.dataframe(
                    missing.rename("Missing Values"),
                    use_container_width=True,
                )
            else:
                st.success("No missing values detected.")

            if info["duplicates"] > 0:
                st.warning(
                    f"{info['duplicates']:,} duplicate rows detected."
                )
            else:
                st.success("No duplicate rows detected.")


# ============================================================
# DOCUMENTS
# ============================================================

elif page == "📄 Documents":
    st.markdown(
        '<div class="page-title">📄 Documents</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Manage the documents currently available to your AI assistant.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.documents:
        st.info("No documents have been uploaded yet.")
    else:
        for number, name in enumerate(
            st.session_state.documents,
            start=1,
        ):
            st.markdown(
                f"""
                <div class="file-card">
                    📄 <b>{number}.</b> {html.escape(name)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="section-title">Knowledge Base</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Documents",
                len(st.session_state.documents),
            )

        with c2:
            st.metric(
                "Indexed Chunks",
                len(st.session_state.chunks),
            )


# ============================================================
# EXPORT CENTER
# ============================================================

elif page == "📥 Export Center":
    st.markdown(
        '<div class="page-title">📥 Export Center</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Create one professional PDF containing your generated study and data material.</div>',
        unsafe_allow_html=True,
    )

    study = st.session_state.study_material

    st.markdown(
        '<div class="section-title">Report Contents</div>',
        unsafe_allow_html=True,
    )

    items = [
        ("📝", "Document Summary", bool(study.get("summary"))),
        ("⭐", "Important Topics", bool(study.get("topics"))),
        ("🧠", "Cheat Cards", bool(study.get("cheat_cards"))),
        ("❓", "Practice Questions", bool(study.get("questions"))),
        ("📊", "Dataset Analysis", st.session_state.dataframe is not None),
        ("📈", "Visualizations", bool(st.session_state.charts)),
        ("🤖", "AI Data Insights", bool(study.get("data_insights"))),
    ]

    for icon, name, available in items:
        status = "✓ Ready" if available else "○ Not generated"

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">{icon} {name}</div>
                <div class="info-text">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    has_content = bool(study) or st.session_state.dataframe is not None

    if not has_content:
        st.warning(
            "Generate study material or analyze a dataset before creating a report."
        )
    else:
        if st.button(
            "📄 Generate Complete PDF Report",
            use_container_width=True,
        ):
            with st.spinner("Building your professional report..."):
                try:
                    pdf = generate_pdf()

                    st.success("Your report is ready.")

                    st.download_button(
                        "⬇️ Download PDF Report",
                        data=pdf,
                        file_name="DocuMind_AI_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")