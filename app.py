import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import date
import re

st.set_page_config(
    page_title="Groww MF Facts Assistant",
    page_icon="📊",
    layout="centered"
)

# -----------------------------
# VERIFIED KNOWLEDGE BASE
# -----------------------------

knowledge_base = [
    {
        "text": """HDFC Flexi Cap Fund is an open-ended dynamic equity scheme
        investing across large cap, mid cap and small cap stocks.
        The minimum SIP amount is ₹100.
        The scheme riskometer is Very High.
        The benchmark is NIFTY 500 Total Returns Index.
        The Total Expense Ratio (TER) for the Direct Plan is 0.77.
        There is no lock-in period.
        Exit load is 1.00% if units are redeemed or switched out within
        1 year from the date of allotment. No exit load is payable after 1 year.""",
        "source": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct",
        "title": "HDFC Flexi Cap Fund"
    },

    {
        "text": """HDFC ELSS Tax Saver Fund is an open-ended Equity Linked
        Savings Scheme with a statutory lock-in period of 3 years.
        The minimum SIP amount is ₹500.
        The minimum lump sum application amount is ₹500.
        The riskometer is Very High.
        The benchmark is NIFTY 500 Total Returns Index.
        The Total Expense Ratio (TER) for the Direct Plan is 1.21.
        Exit load is NIL.""",
        "source": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct",
        "title": "HDFC ELSS Tax Saver Fund"
    },

    {
        "text": """HDFC Large Cap Fund is an open-ended equity scheme
        predominantly investing in large cap stocks.
        The minimum SIP amount is ₹100.
        The riskometer is Very High.
        The benchmark is NIFTY 100 Total Return Index.
        The Total Expense Ratio (TER) for the Direct Plan is 1.03.
        There is no lock-in period.
        Exit load is 1.00% if units are redeemed or switched out within
        1 year from the date of allotment. No exit load is payable after 1 year.""",
        "source": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct",
        "title": "HDFC Large Cap Fund"
    }
]


# -----------------------------
# GUARDRAILS
# -----------------------------

ADVICE_WORDS = [
    "should i invest", "should i buy", "should i sell",
    "should i redeem", "should i switch", "good investment",
    "best fund", "better fund", "recommend", "worth investing",
    "which fund should", "where should i invest"
]

PERFORMANCE_WORDS = [
    "future return", "future returns", "how much return",
    "expected return", "highest return", "will it grow",
    "return next year", "predict return", "better returns"
]

PII_PATTERNS = [
    r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",       # PAN-like
    r"\b\d{12}\b",                      # Aadhaar-like
    r"\b\d{10}\b",                      # phone-like
    r"\b\d{6}\b",                       # OTP-like
    r"[\w\.-]+@[\w\.-]+\.\w+"           # email-like
]

PII_WORDS = [
    "my pan", "my aadhaar", "my aadhar", "my otp",
    "account number", "my email", "my phone number"
]


def contains_pii(query):
    lower_query = query.lower()

    if any(word in lower_query for word in PII_WORDS):
        return True

    return any(
        re.search(pattern, query, re.IGNORECASE)
        for pattern in PII_PATTERNS
    )


def classify_query(query):
    q = query.lower()

    if contains_pii(query):
        return "pii"

    if any(word in q for word in ADVICE_WORDS):
        return "advice"

    if any(word in q for word in PERFORMANCE_WORDS):
        return "performance"

    return "factual"


# -----------------------------
# RETRIEVAL
# -----------------------------

documents = [item["text"] for item in knowledge_base]

vectorizer = TfidfVectorizer(stop_words="english")
document_vectors = vectorizer.fit_transform(documents)


def retrieve(query):
    q = query.lower()

    # First identify the scheme explicitly mentioned by the user.
    # This prevents similar scheme documents from being confused.
    if "flexi cap" in q:
        return knowledge_base[0]

    if "elss" in q or "tax saver" in q:
        return knowledge_base[1]

    if "large cap" in q:
        return knowledge_base[2]

    # If no supported scheme is explicitly identified,
    # fall back to vector similarity retrieval.
    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    best_index = similarities.argmax()
    score = similarities[best_index]

    if score < 0.08:
        return None

    return knowledge_base[best_index]


# -----------------------------
# FACT EXTRACTION
# -----------------------------

def build_answer(query, doc):
    q = query.lower()
    text = doc["text"]

    if "sip" in q:
        match = re.search(r"minimum SIP amount is ₹[\d,.]+", text, re.I)

    elif "expense" in q or "ter" in q:
        match = re.search(
            r"Total Expense Ratio \(TER\) for the Direct Plan is [\d.]+",
            text,
            re.I
        )

    elif "exit" in q:
        if "Exit load is NIL" in text:
            return "The exit load is NIL."
        match = re.search(
            r"Exit load is .*?(?:after 1 year\.|allotment\.)",
            text,
            re.I
        )

    elif "lock" in q:
        if "statutory lock-in period of 3 years" in text:
            return "The scheme has a statutory lock-in period of 3 years."
        if "no lock-in period" in text.lower():
            return "The scheme does not have a lock-in period."
        match = None

    elif "risk" in q:
        match = re.search(r"riskometer is [^.]+", text, re.I)

    elif "benchmark" in q:
        match = re.search(r"benchmark is [^.]+", text, re.I)

    elif "minimum" in q and ("lump" in q or "investment" in q):
        match = re.search(
            r"minimum lump sum application amount is ₹[\d,.]+",
            text,
            re.I
        )

    elif "what is" in q or "about" in q:
        return text.split(".")[0].strip() + "."

    else:
        return (
            "I found the relevant official scheme source, but I couldn't "
            "verify the exact requested fact from the available indexed information."
        )

    if match:
        sentence = match.group(0).strip()
        return sentence[0].upper() + sentence[1:].rstrip(".") + "."

    return (
        "I couldn't verify this fact from the available indexed official sources."
    )


# -----------------------------
# UI
# -----------------------------

st.title("📊 Groww MF Facts Assistant")

st.write(
    "Get concise, verified facts about selected HDFC Mutual Fund schemes "
    "using official public sources."
)

st.info(
    "🔎 Facts-only. No investment advice. "
    "Please do not share PAN, Aadhaar, OTP, account numbers, "
    "email addresses or phone numbers."
)

st.subheader("Try asking")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Minimum SIP?"):
        st.session_state["question"] = (
            "What is the minimum SIP for HDFC Flexi Cap Fund?"
        )

with col2:
    if st.button("ELSS lock-in?"):
        st.session_state["question"] = (
            "What is the lock-in period of HDFC ELSS Tax Saver Fund?"
        )

with col3:
    if st.button("Large Cap benchmark?"):
        st.session_state["question"] = (
            "What is the benchmark of HDFC Large Cap Fund?"
        )

question = st.text_input(
    "Ask a mutual fund question",
    value=st.session_state.get("question", ""),
    placeholder="e.g. What is the exit load of HDFC Flexi Cap Fund?"
)

if st.button("Ask", type="primary") and question.strip():

    query_type = classify_query(question)

    if query_type == "pii":

        st.warning(
            "Please don't share personal information such as PAN, Aadhaar, "
            "account numbers, OTPs, email addresses or phone numbers. "
            "This assistant only answers public factual questions about "
            "supported mutual fund schemes."
        )

    elif query_type == "advice":

        st.warning(
            "I can provide verified facts about mutual fund schemes, "
            "but I can't recommend whether you should buy, sell, hold or "
            "switch a fund. You can ask about the scheme's expense ratio, "
            "exit load, SIP amount, lock-in, riskometer or benchmark."
        )

    elif query_type == "performance":

        st.warning(
            "I don't predict, calculate or compare investment returns. "
            "Please refer to the official AMC factsheet for published "
            "scheme information and historical performance."
        )

    else:

        result = retrieve(question)

        if result is None:

            st.error(
                "I couldn't verify this from the available official sources. "
                "Try asking about HDFC Flexi Cap Fund, HDFC ELSS Tax Saver Fund "
                "or HDFC Large Cap Fund."
            )

        else:

            answer = build_answer(question, result)

            st.subheader("Answer")
            st.write(answer)

            st.markdown(
                f"**Source:** [{result['title']}]({result['source']})"
            )

            st.caption(
                f"Last updated from sources: {date.today().strftime('%d %b %Y')}"
            )


st.divider()

st.caption(
    "Supported schemes: HDFC Flexi Cap Fund • "
    "HDFC ELSS Tax Saver Fund • HDFC Large Cap Fund"
)

st.caption(
    "This prototype provides factual information only and does not "
    "provide investment advice or recommendations."
)
