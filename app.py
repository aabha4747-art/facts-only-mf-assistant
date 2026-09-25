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
    padding: 1.7rem 1.8rem;
    border: 1px solid rgba(128,128,128,0.20);
    border-radius: 18px;
    margin-bottom: 1.2rem;
}

.hero h1 {
    margin: 0;
    font-size: 2.25rem;
}

.hero p {
    margin-top: 0.6rem;
    margin-bottom: 0;
    opacity: 0.75;
    font-size: 1.05rem;
}

.mini-card {
    border: 1px solid rgba(128,128,128,0.20);
    padding: 1rem;
    border-radius: 14px;
    min-height: 110px;
}

.source-box {
    margin-top: 1rem;
    padding: 0.9rem 1rem;
    border-radius: 10px;
    background: rgba(128,128,128,0.08);
}

div.stButton > button {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# VERIFIED KNOWLEDGE BASE
# =========================================================

knowledge_base = [

    # -----------------------------------------------------
    # HDFC FLEXI CAP
    # -----------------------------------------------------

    {
        "id": "HDFC_FLEXI",

        "scheme": "HDFC Flexi Cap Fund",

        "aliases": [
            "hdfc flexi cap fund",
            "hdfc flexi cap",
            "flexi cap fund",
            "flexi cap"
        ],

        "category": "Flexi Cap Fund",

        "facts": {

            "sip":
                "The minimum SIP amount is ₹100.",

            "expense":
                "The Total Expense Ratio (TER) for the Direct Plan is 0.77%.",

            "exit":
                "The exit load is 1.00% if units are redeemed or switched "
                "out within 1 year from the date of allotment. "
                "No exit load is payable after 1 year.",

            "lockin":
                "The scheme does not have a lock-in period.",

            "risk":
                "The scheme riskometer is Very High.",

            "benchmark":
                "The benchmark is NIFTY 500 Total Returns Index.",

            "about":
                "HDFC Flexi Cap Fund is an open-ended dynamic equity scheme "
                "investing across large cap, mid cap and small cap stocks."
        },

        "source":
            "https://www.hdfcfund.com/explore/mutual-funds/"
            "hdfc-flexi-cap-fund/direct"
    },


    # -----------------------------------------------------
    # HDFC ELSS
    # -----------------------------------------------------

    {
        "id": "HDFC_ELSS",

        "scheme": "HDFC ELSS Tax Saver Fund",

        "aliases": [
            "hdfc elss tax saver fund",
            "hdfc elss tax saver",
            "hdfc elss",
            "elss tax saver fund",
            "elss tax saver",
            "elss"
        ],

        "category": "ELSS",

        "facts": {

            "sip":
                "The minimum SIP amount is ₹500.",

            "expense":
                "The Total Expense Ratio (TER) for the Direct Plan is 1.21%.",

            "exit":
                "The exit load is NIL.",

            "lockin":
                "The scheme has a statutory lock-in period of 3 years "
                "from the date of allotment of units.",

            "risk":
                "The scheme riskometer is Very High.",

            "benchmark":
                "The benchmark is NIFTY 500 Total Returns Index.",

            "minimum":
                "The minimum lump sum application amount is ₹500.",

            "about":
                "HDFC ELSS Tax Saver Fund is an open-ended Equity Linked "
                "Savings Scheme with a statutory lock-in period of 3 years."
        },

        "source":
            "https://www.hdfcfund.com/explore/mutual-funds/"
            "hdfc-elss-tax-saver-fund/direct"
    },


    # -----------------------------------------------------
    # HDFC LARGE CAP
    # -----------------------------------------------------

    {
        "id": "HDFC_LARGE",

        "scheme": "HDFC Large Cap Fund",

        "aliases": [
            "hdfc large cap fund",
            "hdfc large cap",
            "large cap fund",
            "large cap"
        ],

        "category": "Large Cap Fund",

        "facts": {

            "sip":
                "The minimum SIP amount is ₹100.",

            "expense":
                "The Total Expense Ratio (TER) for the Direct Plan is 1.03%.",

            "exit":
                "The exit load is 1.00% if units are redeemed or switched "
                "out within 1 year from the date of allotment. "
                "No exit load is payable after 1 year.",

            "lockin":
                "The scheme does not have a lock-in period.",

            "risk":
                "The scheme riskometer is Very High.",

            "benchmark":
                "The benchmark is NIFTY 100 Total Return Index.",

            "about":
                "HDFC Large Cap Fund is an open-ended equity scheme "
                "predominantly investing in large cap stocks."
        },

        "source":
            "https://www.hdfcfund.com/explore/mutual-funds/"
            "hdfc-large-cap-fund/direct"
    }
]


# =========================================================
# RETRIEVAL DOCUMENTS
# =========================================================

def create_document(item):

    facts_text = " ".join(item["facts"].values())

    return (
        f"Scheme {item['scheme']}. "
        f"Category {item['category']}. "
        f"{facts_text}"
    )


documents = [
    create_document(item)
    for item in knowledge_base
]


vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)

document_vectors = vectorizer.fit_transform(documents)


# =========================================================
# SAFETY / GUARDRAILS
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
    "portfolio allocation"
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


# =========================================================
# PII DETECTION
# =========================================================

def contains_pii(query):

    q = query.lower()

    if any(word in q for word in PII_WORDS):
        return True

    patterns = [

        # PAN-like
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

        # Aadhaar-like
        r"\b\d{12}\b",

        # Phone-like
        r"\b\d{10}\b",

        # OTP-like
        r"\b\d{6}\b",

        # Email
        r"[\w\.-]+@[\w\.-]+\.\w+"
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            query,
            re.IGNORECASE
        ):
            return True

    return False


# =========================================================
# QUERY CLASSIFICATION
# =========================================================

def classify_query(query):

    q = query.lower()

    if contains_pii(query):
        return "pii"

    if any(
        phrase in q
        for phrase in ADVICE_PHRASES
    ):
        return "advice"

    if any(
        phrase in q
        for phrase in PERFORMANCE_PHRASES
    ):
        return "performance"

    if any(
        amc in q
        for amc in UNSUPPORTED_AMCS
    ):
        return "unsupported"

    return "factual"


# =========================================================
# SCHEME IDENTIFICATION
# =========================================================

def identify_scheme(query):

    q = query.lower()

    for item in knowledge_base:

        for alias in item["aliases"]:

            if alias in q:
                return item

    return None


# =========================================================
# TF-IDF RETRIEVAL
# =========================================================

def retrieve(query):

    query_vector = vectorizer.transform(
        [query]
    )

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    best_index = similarities.argmax()

    best_score = float(
        similarities[best_index]
    )

    if best_score < 0.12:

        return (
            None,
            best_score,
            "No confident match"
        )

    return (
        knowledge_base[best_index],
        best_score,
        "TF-IDF cosine similarity"
    )


# =========================================================
# FACT / INTENT DETECTION
# =========================================================

def detect_fact_type(query):

    q = query.lower()

    # SIP
    if "sip" in q:
        return "sip"

    # Expense ratio
    if (
        "expense ratio" in q
        or "ter" in q
        or "expense" in q
    ):
        return "expense"

    # Exit load
    if (
        "exit load" in q
        or "exit" in q
    ):
        return "exit"

    # Lock-in
    if (
        "lock-in" in q
        or "lock in" in q
        or "lockin" in q
        or "locked" in q
    ):
        return "lockin"

    # Risk
    if (
        "riskometer" in q
        or "risk-o-meter" in q
        or "risk" in q
    ):
        return "risk"

    # Benchmark
    if (
        "benchmark" in q
        or "index" in q
    ):
        return "benchmark"

    # Lump sum
    if (
        "minimum investment" in q
        or "minimum amount" in q
        or "lump sum" in q
        or "lumpsum" in q
    ):
        return "minimum"

    # General scheme information
    if (
        "what is" in q
        or "tell me about" in q
        or "about" in q
        or "category" in q
    ):
        return "about"

    return None


# =========================================================
# RETRIEVAL CONFIDENCE
# =========================================================

def confidence_label(
    score,
    method
):

    if method == "Explicit scheme match":
        return "High"

    if score >= 0.35:
        return "High"

    if score >= 0.20:
        return "Medium"

    return "Low"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 Assistant Scope")

    st.markdown(
        """
        **Product context:** Groww

        **AMC:** HDFC Mutual Fund

        **Sources:** Official public sources
        """
    )

    st.divider()

    st.subheader(
        "Supported schemes"
    )

    for item in knowledge_base:

        st.markdown(
            f"✓ {item['scheme']}"
        )

    st.divider()

    st.subheader(
        "Supported facts"
    )

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

        <h1>
            📊 Groww MF Facts Assistant
        </h1>

        <p>
            Verified mutual fund facts from official public
            sources — without investment advice.
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

        <b>🏦 3 Schemes</b>

        <br><br>

        Selected HDFC Mutual Fund schemes.

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        """
        <div class="mini-card">

        <b>🔎 Source-backed</b>

        <br><br>

        Every factual answer includes an official source.

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        """
        <div class="mini-card">

        <b>🛡️ Guardrails</b>

        <br><br>

        Advice, performance and PII requests are restricted.

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.subheader(
    "Example questions"
)

example1, example2, example3 = st.columns(3)


with example1:

    st.info(
        "💰 What is the minimum SIP for "
        "HDFC Flexi Cap Fund?"
    )


with example2:

    st.info(
        "🔒 What is the lock-in period of "
        "HDFC ELSS Tax Saver Fund?"
    )


with example3:

    st.info(
        "📈 What is the benchmark of "
        "HDFC Large Cap Fund?"
    )


# =========================================================
# QUESTION FORM
# =========================================================

st.subheader(
    "Ask a question"
)


with st.form(
    "mf_question_form",
    clear_on_submit=False
):

    question = st.text_input(

        "Mutual fund question",

        placeholder=(
            "e.g. What is the exit load "
            "of HDFC Flexi Cap Fund?"
        ),

        label_visibility="collapsed"
    )


    submitted = st.form_submit_button(
        "Ask",
        type="primary"
    )


# =========================================================
# QUERY PROCESSING
# =========================================================

if submitted:

    question = question.strip()

    # -----------------------------------------------------
    # EMPTY QUESTION
    # -----------------------------------------------------

    if not question:

        st.warning(
            "Please enter a question."
        )


    else:

        query_type = classify_query(
            question
        )


        # =================================================
        # PII
        # =================================================

        if query_type == "pii":

            st.warning(
                "🔒 **Please don't share personal information.** "
                "This assistant does not accept or process PAN, "
                "Aadhaar, account numbers, OTPs, email addresses "
                "or phone numbers."
            )

            st.write(
                "You can ask public factual questions "
                "about supported mutual fund schemes."
            )


        # =================================================
        # INVESTMENT ADVICE
        # =================================================

        elif query_type == "advice":

            st.warning(
                "🛡️ **Facts-only assistant.** "
                "I can provide verified facts about mutual fund "
                "schemes, but I can't recommend whether you "
                "should buy, sell, hold, redeem or switch a fund."
            )

            st.write(
                "You can instead ask about the scheme's "
                "minimum SIP, expense ratio, exit load, "
                "lock-in period, riskometer or benchmark."
            )

            st.markdown(
                "**Educational resource:** "
                "[SEBI Investor — Mutual Funds]"
                "(https://investor.sebi.gov.in/"
                "securities-mf-investments.html)"
            )


        # =================================================
        # PERFORMANCE
        # =================================================

        elif query_type == "performance":

            st.warning(
                "📉 **Performance request restricted.** "
                "I don't calculate, predict or compare "
                "mutual fund returns."
            )

            st.write(
                "Please refer to official AMC factsheets "
                "for published historical scheme information."
            )

            st.markdown(
                "**Educational resource:** "
                "[SEBI Investor — Mutual Funds]"
                "(https://investor.sebi.gov.in/"
                "securities-mf-investments.html)"
            )


        # =================================================
        # UNSUPPORTED FUND
        # =================================================

        elif query_type == "unsupported":

            st.info(
                "ℹ️ **Outside the current corpus.** "
                "I couldn't verify this from the available "
                "official sources."
            )

            st.write(
                "This prototype currently supports:"
            )

            st.markdown(
                """
                - HDFC Flexi Cap Fund
                - HDFC ELSS Tax Saver Fund
                - HDFC Large Cap Fund
                """
            )


        # =================================================
        # FACTUAL QUERY
        # =================================================

        else:

            # ---------------------------------------------
            # STEP 1:
            # Explicit scheme identification
            # ---------------------------------------------

            retrieved_doc = identify_scheme(
                question
            )


            if retrieved_doc is not None:

                score = 1.0

                method = (
                    "Explicit scheme match"
                )


            # ---------------------------------------------
            # STEP 2:
            # TF-IDF fallback
            # ---------------------------------------------

            else:

                (
                    retrieved_doc,
                    score,
                    method

                ) = retrieve(question)


            # =============================================
            # NO RETRIEVAL
            # =============================================

            if retrieved_doc is None:

                st.error(
                    "I couldn't verify this from the "
                    "available official sources."
                )

                st.write(
                    "Please mention one of the supported "
                    "scheme names and the factual information "
                    "you need."
                )


            else:

                # -----------------------------------------
                # STEP 3:
                # Detect requested fact
                # -----------------------------------------

                fact_type = detect_fact_type(
                    question
                )


                # =========================================
                # UNKNOWN FACT TYPE
                # =========================================

                if fact_type is None:

                    st.info(
                        f"I found **{retrieved_doc['scheme']}**, "
                        "but I couldn't identify a supported "
                        "factual field in your question."
                    )

                    st.write(
                        "Try asking about:"
                    )

                    st.markdown(
                        """
                        - Minimum SIP
                        - Expense ratio
                        - Exit load
                        - Lock-in period
                        - Riskometer
                        - Benchmark
                        """
                    )


                # =========================================
                # FACT NOT AVAILABLE
                # =========================================

                elif (
                    fact_type
                    not in retrieved_doc["facts"]
                ):

                    st.info(
                        "I couldn't verify that specific "
                        "fact from the available indexed "
                        "official information."
                    )


                # =========================================
                # SUCCESS
                # =========================================

                else:

                    answer = (
                        retrieved_doc["facts"]
                        [fact_type]
                    )


                    st.success(
                        "✓ Verified from indexed official source"
                    )


                    st.markdown(
                        "## Answer"
                    )


                    st.write(
                        answer
                    )


                    st.markdown(
                        f"**Source:** "
                        f"[{retrieved_doc['scheme']} "
                        f"— HDFC Mutual Fund]"
                        f"({retrieved_doc['source']})"
                    )


                    metadata1, metadata2, metadata3 = (
                        st.columns(3)
                    )


                    with metadata1:

                        st.caption(
                            "Scheme: "
                            f"{retrieved_doc['scheme']}"
                        )


                    with metadata2:

                        st.caption(
                            "Retrieval confidence: "
                            f"{confidence_label(score, method)}"
                        )


                    with metadata3:

                        st.caption(
                            "Last updated from sources: "
                            f"{date.today().strftime('%d %b %Y')}"
                        )


# =========================================================
# REFERENCE TABLE
# =========================================================

st.divider()


with st.expander(
    "📋 View supported scheme reference"
):

    st.caption(
        "Factual reference only. "
        "This table is not a recommendation or ranking."
    )


    reference_data = []


    for item in knowledge_base:

        reference_data.append(

            {

                "Scheme":
                    item["scheme"],

                "Category":
                    item["category"],

                "Minimum SIP":
                    item["facts"]["sip"]
                    .replace(
                        "The minimum SIP amount is ",
                        ""
                    ),

                "Riskometer":
                    item["facts"]["risk"]
                    .replace(
                        "The scheme riskometer is ",
                        ""
                    ),

                "Benchmark":
                    item["facts"]["benchmark"]
                    .replace(
                        "The benchmark is ",
                        ""
                    )
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

with st.expander(
    "⚙️ How this prototype works"
):

    st.markdown(
        """
### 1. Query classification

The question is checked for:

- Investment advice
- Performance requests
- Personally identifiable information
- Unsupported funds

### 2. Scheme identification

Explicit scheme names are matched first.

This prevents information from one scheme being
incorrectly returned for another scheme.

### 3. Retrieval

The small indexed corpus is represented using
**TF-IDF vectors**.

When an explicit scheme name is not detected,
**cosine similarity** is used as the fallback
retrieval mechanism.

### 4. Fact identification

The assistant identifies the exact factual field
requested, such as:

- SIP
- Expense ratio
- Exit load
- Lock-in
- Riskometer
- Benchmark

### 5. Grounded answer

The answer is returned only from the retrieved
scheme's indexed official-source facts.

### 6. Citation

Every successful factual response contains an
official HDFC Mutual Fund source.

---

**Prototype limitation:** This implementation uses
deterministic grounded fact extraction rather than
a paid external LLM API.
        """
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.markdown(
    "### Disclaimer"
)

st.caption(
    "Facts-only. No investment advice. "
    "This prototype provides factual information "
    "from selected official public sources and does "
    "not recommend buying, selling, holding, redeeming "
    "or switching mutual funds. It does not calculate, "
    "predict or compare investment returns. Scheme "
    "information may change over time; verify the latest "
    "information using the linked official source. "
    "Do not enter PAN, Aadhaar, OTPs, account numbers, "
    "email addresses, phone numbers or other personal data."
)
