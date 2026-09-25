import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import date
import re

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Groww MF Facts Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.6rem 1.8rem;
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 18px;
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.25rem;
    }

    .hero p {
        margin-top: 0.5rem;
        margin-bottom: 0;
        opacity: 0.78;
        font-size: 1.05rem;
    }

    .mini-card {
        border: 1px solid rgba(128,128,128,0.20);
        padding: 1rem;
        border-radius: 14px;
        min-height: 115px;
    }

    .answer-card {
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 16px;
        padding: 1.3rem 1.4rem;
        margin-top: 0.8rem;
    }

    .source-box {
        margin-top: 1rem;
        padding: 0.85rem 1rem;
        border-radius: 10px;
        background: rgba(128,128,128,0.08);
    }

    .small-muted {
        opacity: 0.65;
        font-size: 0.88rem;
    }

    div.stButton > button {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# OFFICIAL-SOURCE KNOWLEDGE BASE
# =========================================================

knowledge_base = [
    {
        "id": "HDFC_FLEXI",
        "scheme": "HDFC Flexi Cap Fund",
        "aliases": [
            "hdfc flexi cap",
            "flexi cap fund",
            "flexi cap"
        ],
        "category": "Flexi Cap Fund",
        "facts": {
            "sip": "The minimum SIP amount is ₹100.",
            "expense": "The Total Expense Ratio (TER) for the Direct Plan is 0.77%.",
            "exit": (
                "The exit load is 1.00% if units are redeemed or switched out "
                "within 1 year from the date of allotment. No exit load is "
                "payable after 1 year."
            ),
            "lockin": "The scheme does not have a lock-in period.",
            "risk": "The scheme riskometer is Very High.",
            "benchmark": "The benchmark is NIFTY 500 Total Returns Index.",
            "about": (
                "HDFC Flexi Cap Fund is an open-ended dynamic equity scheme "
                "investing across large cap, mid cap and small cap stocks."
            )
        },
        "source": (
            "https://www.hdfcfund.com/explore/mutual-funds/"
            "hdfc-flexi-cap-fund/direct"
        )
    },

    {
        "id": "HDFC_ELSS",
        "scheme": "HDFC ELSS Tax Saver Fund",
        "aliases": [
            "hdfc elss",
            "hdfc elss tax saver",
            "elss tax saver",
            "tax saver fund",
            "elss"
        ],
        "category": "ELSS",
        "facts": {
            "sip": "The minimum SIP amount is ₹500.",
            "expense": "The Total Expense Ratio (TER) for the Direct Plan is 1.21%.",
            "exit": "The exit load is NIL.",
            "lockin": (
                "The scheme has a statutory lock-in period of 3 years "
                "from the date of allotment of units."
            ),
            "risk": "The scheme riskometer is Very High.",
            "benchmark": "The benchmark is NIFTY 500 Total Returns Index.",
            "minimum": "The minimum lump sum application amount is ₹500.",
            "about": (
                "HDFC ELSS Tax Saver Fund is an open-ended Equity Linked "
                "Savings Scheme with a statutory lock-in period of 3 years."
            )
        },
        "source": (
            "https://www.hdfcfund.com/explore/mutual-funds/"
            "hdfc-elss-tax-saver-fund/direct"
        )
    },

    {
        "id": "HDFC_LARGE",
        "scheme": "HDFC Large Cap Fund",
        "aliases": [
            "hdfc large cap",
            "large cap fund",
            "large cap"
        ],
        "category": "Large Cap Fund",
        "facts": {
            "sip": "The minimum SIP amount is ₹100.",
            "expense": "The Total Expense Ratio (TER) for the Direct Plan is 1.03%.",
            "exit": (
                "The exit load is 1.00% if units are redeemed or switched out "
                "within 1 year from the date of allotment. No exit load is "
                "payable after 1 year."
            ),
            "lockin": "The scheme does not have a lock-in period.",
            "risk": "The scheme riskometer is Very High.",
            "benchmark": "The benchmark is NIFTY 100 Total Return Index.",
            "about": (
                "HDFC Large Cap Fund is an open-ended equity scheme "
                "predominantly investing in large cap stocks."
            )
        },
        "source": (
            "https://www.hdfcfund.com/explore/mutual-funds/"
            "hdfc-large-cap-fund/direct"
        )
    }
]


# =========================================================
# CREATE RETRIEVAL DOCUMENTS
# =========================================================

def create_document(item):
    fact_text = " ".join(item["facts"].values())

    return (
        f"Scheme: {item['scheme']}. "
        f"Category: {item['category']}. "
        f"{fact_text}"
    )


documents = [create_document(item) for item in knowledge_base]

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)

document_vectors = vectorizer.fit_transform(documents)


# =========================================================
# GUARDRAILS
# =========================================================

ADVICE_PHRASES = [
    "should i invest",
    "should i buy",
    "should i sell",
    "should i redeem",
    "should i switch",
    "should i hold",
    "good investment",
    "good fund",
    "bad fund",
    "best fund",
    "better fund",
    "recommend",
    "recommendation",
    "worth investing",
    "which fund should",
    "where should i invest",
    "is it worth",
    "is this good",
    "is this safe",
    "invest my money",
    "portfolio"
]

PERFORMANCE_PHRASES = [
    "future return",
    "future returns",
    "expected return",
    "expected returns",
    "highest return",
    "highest returns",
    "how much return",
    "how much returns",
    "will it grow",
    "return next year",
    "returns next year",
    "predict return",
    "predict returns",
    "better returns",
    "compare returns",
    "past returns",
    "historical returns",
    "performance comparison",
    "which will perform",
    "which performs better"
]

PII_WORDS = [
    "my pan",
    "pan number",
    "my aadhaar",
    "my aadhar",
    "aadhaar number",
    "aadhar number",
    "my otp",
    "account number",
    "bank account",
    "my email",
    "email address",
    "my phone",
    "phone number",
    "mobile number"
]

UNSUPPORTED_AMCS = [
    "sbi",
    "axis",
    "icici",
    "nippon",
    "parag parikh",
    "ppfas",
    "motilal",
    "kotak",
    "quant",
    "aditya birla",
    "mirae",
    "canara robeco",
    "dsp",
    "franklin",
    "tata mutual",
    "uti",
    "bandhan",
    "edelweiss"
]


def contains_pii(query):
    q = query.lower()

    if any(word in q for word in PII_WORDS):
        return True

    pii_patterns = [
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",   # PAN-like
        r"\b\d{12}\b",                  # Aadhaar-like
        r"\b\d{10}\b",                  # Phone-like
        r"\b\d{6}\b",                   # OTP-like
        r"[\w\.-]+@[\w\.-]+\.\w+"       # Email-like
    ]

    return any(
        re.search(pattern, query, re.IGNORECASE)
        for pattern in pii_patterns
    )


def classify_query(query):
    q = query.lower()

    if contains_pii(query):
        return "pii"

    if any(phrase in q for phrase in ADVICE_PHRASES):
        return "advice"

    if any(phrase in q for phrase in PERFORMANCE_PHRASES):
        return "performance"

    if any(amc in q for amc in UNSUPPORTED_AMCS):
        return "unsupported"

    return "factual"


# =========================================================
# SCHEME IDENTIFICATION
# =========================================================

def identify_scheme(query):
    q = query.lower()

    # Explicit scheme matching gets priority.
    for item in knowledge_base:
        for alias in item["aliases"]:
            if alias in q:
                return item

    return None


# =========================================================
# RETRIEVAL
# =========================================================

def retrieve(query):
    explicit_scheme = identify_scheme(query)

    if explicit_scheme:
        return explicit_scheme, 1.0, "Explicit scheme match"

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    best_index = similarities.argmax()
    best_score = float(similarities[best_index])

    if best_score < 0.12:
        return None, best_score, "No confident match"

    return (
        knowledge_base[best_index],
        best_score,
        "TF-IDF cosine similarity"
    )


# =========================================================
# INTENT / FACT IDENTIFICATION
# =========================================================

def detect_fact_type(query):
    q = query.lower()

    if "sip" in q:
        return "sip"

    if (
        "expense ratio" in q
        or "ter" in q
        or "expense" in q
    ):
        return "expense"

    if "exit load" in q or "exit" in q:
        return "exit"

    if (
        "lock-in" in q
        or "lock in" in q
        or "lockin" in q
        or "locked" in q
    ):
        return "lockin"

    if (
        "riskometer" in q
        or "risk-o-meter" in q
        or "risk" in q
    ):
        return "risk"

    if "benchmark" in q or "index" in q:
        return "benchmark"

    if (
        "minimum investment" in q
        or "minimum amount" in q
        or "lump sum" in q
        or "lumpsum" in q
    ):
        return "minimum"

    if (
        "what is" in q
        or "tell me about" in q
        or "about" in q
        or "category" in q
    ):
        return "about"

    return None


# =========================================================
# ANSWER GENERATION
# =========================================================

def generate_answer(query, retrieved_doc):
    fact_type = detect_fact_type(query)

    if fact_type is None:
        return (
            None,
            "unknown_fact"
        )

    facts = retrieved_doc["facts"]

    if fact_type not in facts:
        return (
            None,
            "fact_not_available"
        )

    return facts[fact_type], "success"


# =========================================================
# HELPERS
# =========================================================

def confidence_label(score, method):
    if method == "Explicit scheme match":
        return "High"

    if score >= 0.35:
        return "High"

    if score >= 0.20:
        return "Medium"

    return "Low"


def clear_question():
    st.session_state["question_input"] = ""


def set_example(question):
    st.session_state["question_input"] = question


# =========================================================
# SESSION STATE
# =========================================================

if "question_input" not in st.session_state:
    st.session_state["question_input"] = ""

if "queries_answered" not in st.session_state:
    st.session_state["queries_answered"] = 0


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 Assistant Scope")

    st.markdown(
        """
        **Product context:** Groww  
        **AMC:** HDFC Mutual Fund  
        **Corpus:** Official public sources
        """
    )

    st.divider()

    st.subheader("Supported schemes")

    for item in knowledge_base:
        st.markdown(f"✓ {item['scheme']}")

    st.divider()

    st.subheader("Supported facts")

    st.markdown(
        """
        - Minimum SIP
        - Expense ratio / TER
        - Exit load
        - Lock-in period
        - Riskometer
        - Benchmark
        - Basic scheme information
        """
    )

    st.divider()

    st.caption(
        "This prototype does not access Groww accounts, "
        "HDFC investor accounts or personal portfolios."
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>📊 Groww MF Facts Assistant</h1>
        <p>
            Verified mutual fund facts from official public sources —
            without investment advice.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "🔒 **Facts-only. No investment advice.** "
    "Do not share PAN, Aadhaar, OTPs, account numbers, "
    "email addresses or phone numbers."
)


# =========================================================
# FEATURE CARDS
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="mini-card">
            <b>🏦 3 Schemes</b><br><br>
            Selected HDFC Mutual Fund schemes.
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="mini-card">
            <b>🔎 Source-backed</b><br><br>
            Every factual answer includes an official source.
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="mini-card">
            <b>🛡️ Guardrails</b><br><br>
            Advice, performance and PII requests are restricted.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.subheader("Try an example")

e1, e2, e3 = st.columns(3)

with e1:
    if st.button(
        "💰 Flexi Cap minimum SIP",
        use_container_width=True
    ):
        set_example(
            "What is the minimum SIP for HDFC Flexi Cap Fund?"
        )
        st.rerun()

with e2:
    if st.button(
        "🔒 ELSS lock-in",
        use_container_width=True
    ):
        set_example(
            "What is the lock-in period of HDFC ELSS Tax Saver Fund?"
        )
        st.rerun()

with e3:
    if st.button(
        "📈 Large Cap benchmark",
        use_container_width=True
    ):
        set_example(
            "What is the benchmark of HDFC Large Cap Fund?"
        )
        st.rerun()


# =========================================================
# QUERY BOX + PROCESSING
# =========================================================

st.subheader("Ask a question")

question = st.text_input(
    "Mutual fund question",
    value=st.session_state.get("question_input", ""),
    placeholder="e.g. What is the exit load of HDFC Flexi Cap Fund?",
    label_visibility="collapsed"
)

ask_clicked = st.button(
    "Ask",
    type="primary",
    use_container_width=False
)

if ask_clicked and question.strip():

    query_type = classify_query(question)

    # -------------------------
    # PII
    # -------------------------

    if query_type == "pii":

        st.warning(
            "🔒 **Please don't share personal information.** "
            "This assistant does not accept or process PAN, Aadhaar, "
            "account numbers, OTPs, email addresses or phone numbers. "
            "You can ask public factual questions about supported schemes."
        )

    # -------------------------
    # ADVICE
    # -------------------------

    elif query_type == "advice":

        st.warning(
            "🛡️ **Facts-only assistant.** "
            "I can provide verified facts about mutual fund schemes, "
            "but I can't recommend whether you should buy, sell, hold, "
            "redeem or switch a fund. Ask about the scheme's SIP, "
            "expense ratio, exit load, lock-in, riskometer or benchmark."
        )

        st.markdown(
            "**Educational resource:** "
            "[SEBI Investor — Mutual Funds]"
            "(https://investor.sebi.gov.in/securities-mf-investments.html)"
        )

    # -------------------------
    # PERFORMANCE
    # -------------------------

    elif query_type == "performance":

        st.warning(
            "📉 **Performance request restricted.** "
            "I don't calculate, predict or compare mutual fund returns. "
            "Please refer to official AMC sources for published "
            "scheme information and historical disclosures."
        )

        st.markdown(
            "**Educational resource:** "
            "[SEBI Investor — Mutual Funds]"
            "(https://investor.sebi.gov.in/securities-mf-investments.html)"
        )

    # -------------------------
    # UNSUPPORTED FUND
    # -------------------------

    elif query_type == "unsupported":

        st.info(
            "ℹ️ **Outside the current corpus.** "
            "I couldn't verify this from the available official sources. "
            "This prototype currently supports HDFC Flexi Cap Fund, "
            "HDFC ELSS Tax Saver Fund and HDFC Large Cap Fund."
        )

    # -------------------------
    # FACTUAL QUERY
    # -------------------------

    else:

        retrieved_doc, score, method = retrieve(question)

        if retrieved_doc is None:

            st.error(
                "I couldn't verify this from the available official "
                "sources. Try mentioning one of the supported scheme "
                "names and the exact fact you need."
            )

        else:

            answer, status = generate_answer(
                question,
                retrieved_doc
            )

            if status == "unknown_fact":

                st.info(
                    "I found the relevant scheme, but I couldn't identify "
                    "a supported factual field in your question. "
                    "Try asking about SIP, expense ratio, exit load, "
                    "lock-in, riskometer or benchmark."
                )

            elif status == "fact_not_available":

                st.info(
                    "I couldn't verify that specific fact from the "
                    "available indexed official information."
                )

            else:

                st.success("✓ Verified from indexed official source")

                st.markdown("### Answer")

                st.write(answer)

                st.markdown(
                    f"**Source:** "
                    f"[{retrieved_doc['scheme']} — HDFC Mutual Fund]"
                    f"({retrieved_doc['source']})"
                )

                col_a, col_b = st.columns(2)

                with col_a:
                    st.caption(
                        "Retrieval confidence: "
                        f"{confidence_label(score, method)}"
                    )

                with col_b:
                    st.caption(
                        "Last updated from sources: "
                        f"{date.today().strftime('%d %b %Y')}"
                    )

elif ask_clicked:

    st.warning("Please enter a question.")


# =========================================================
# SUPPORTED SCHEME REFERENCE TABLE
# =========================================================

st.divider()

with st.expander("📋 View supported scheme reference"):

    st.markdown(
        """
        This table shows the factual fields currently indexed by the
        prototype. It is **not a recommendation or fund ranking**.
        """
    )

    reference_data = []

    for item in knowledge_base:
        reference_data.append(
            {
                "Scheme": item["scheme"],
                "Category": item["category"],
                "Minimum SIP": item["facts"].get(
                    "sip", "Not indexed"
                ).replace("The minimum SIP amount is ", ""),
                "Riskometer": item["facts"].get(
                    "risk", "Not indexed"
                ).replace("The scheme riskometer is ", ""),
                "Benchmark": item["facts"].get(
                    "benchmark", "Not indexed"
                ).replace("The benchmark is ", "")
            }
        )

    st.dataframe(
        reference_data,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# ARCHITECTURE / TRANSPARENCY
# =========================================================

with st.expander("⚙️ How this prototype works"):

    st.markdown(
        """
        **1. Query classification**  
        The question is first checked for investment advice,
        performance requests, unsupported funds and personally
        identifiable information.

        **2. Scheme identification**  
        Explicit scheme names are matched before similarity search
        to reduce cross-scheme retrieval errors.

        **3. Retrieval**  
        The indexed scheme documents are represented using
        TF-IDF vectors. Cosine similarity is used as a fallback
        retrieval method when an explicit scheme is not identified.

        **4. Grounded fact extraction**  
        The requested factual field is returned only from the
        retrieved scheme's indexed official-source facts.

        **5. Citation**  
        Every successful factual response includes its corresponding
        official HDFC Mutual Fund source.

        **Important:** This lightweight prototype uses deterministic
        fact extraction rather than an external paid LLM API.
        """
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.markdown("### Disclaimer")

st.caption(
    "Facts-only. No investment advice. This prototype provides factual "
    "information from selected official public sources and does not "
    "recommend buying, selling, holding, redeeming or switching mutual "
    "funds. It does not calculate, predict or compare investment returns. "
    "Scheme information may change over time; verify the latest information "
    "using the linked official source. Do not enter PAN, Aadhaar, OTPs, "
    "account numbers, email addresses, phone numbers or other personal data."
)
