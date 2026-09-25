# 📊 Groww Facts-Only Mutual Fund Assistant

A small retrieval-based FAQ assistant that answers factual questions about
selected HDFC Mutual Fund schemes using official public sources.

The prototype is designed in the context of **Groww** and demonstrates how a
facts-only assistant could help retail investors quickly find scheme information
without providing investment advice.

## 🔗 Links

**Live Prototype:** <https://facts-only-mf-assistant6commits-kwbex8uiprzbb2uspkwxxm.streamlit.app/>

**GitHub Repository:** [facts-only-mf-assistant](https://github.com/aabha4747-art/facts-only-mf-assistant)

---

## 🎯 Problem Statement

Mutual fund information such as expense ratios, exit loads, minimum SIP amounts,
lock-in periods, benchmarks and risk levels is often distributed across scheme
pages and regulatory documents.

This prototype provides a simple interface for retrieving these facts while
restricting responses to factual information only.

---

## 🏦 Scope

**Product:** Groww

**AMC:** HDFC Mutual Fund

### Supported Schemes

1. HDFC Flexi Cap Fund
2. HDFC ELSS Tax Saver Fund
3. HDFC Large Cap Fund

### Supported factual queries

- Minimum SIP
- Expense ratio / TER
- Exit load
- Lock-in period
- Riskometer
- Benchmark
- Basic scheme information

---

## 🧠 How It Works

The prototype follows this pipeline:

```text
User Question
      ↓
Query Classification
      ↓
PII / Advice / Performance / Unsupported Fund?
      ↓
Refuse or redirect when required
      ↓
Explicit Scheme Identification
      ↓
If no explicit scheme match:
TF-IDF + Cosine Similarity Retrieval
      ↓
Fact Type Identification
      ↓
Grounded Fact Extraction
      ↓
Answer + Official Source Citation

---

## 🔎 Retrieval Approach

The prototype uses a small curated corpus of verified facts from official
HDFC Mutual Fund sources.

Documents are represented using **TF-IDF vectors**. The user's question is
vectorized using the same representation, and **cosine similarity** is used
to retrieve the most relevant scheme information.

The retrieved information is then used to produce a concise factual response
with its corresponding official source.

This lightweight approach was selected for the small corpus and prototype scope.

---

## 🛡️ Guardrails

The assistant classifies incoming questions before retrieval.

### Factual Question

Example:

> What is the minimum SIP for HDFC Flexi Cap Fund?

Action: Retrieve the relevant information and provide the fact with its source.

### Investment Advice

Example:

> Should I invest in HDFC Flexi Cap Fund?

Action: Refuse to recommend buying, selling, holding or switching investments
and redirect the user toward factual scheme information.

### Performance Prediction

Example:

> Which fund will give me the highest return?

Action: Refuse to predict or compare future investment returns.

### Personally Identifiable Information (PII)

Example:

> My PAN is ABCDE1234F. Show my investments.

Action: Do not process the information and remind the user not to share PAN,
Aadhaar, OTPs, account numbers, emails or phone numbers.

---

# 📚 Source List

Only official public sources from HDFC Mutual Fund, SEBI and related regulatory
resources are used. No third-party blogs are used as factual sources.

| # | Source | Type |
|---|---|---|
| 1 | https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct | Scheme Page |
| 2 | https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct | Scheme Page |
| 3 | https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct | Scheme Page |
| 4 | https://www.hdfcfund.com/mutual-funds/fund-documents/kim | KIM Repository |
| 5 | https://www.hdfcfund.com/mutual-funds/fund-documents/sid | SID Repository |
| 6 | https://www.hdfcfund.com/mutual-funds/fund-documents/scheme-summary | Scheme Documents |
| 7 | https://www.hdfcfund.com/services/forms | Forms & Downloads |
| 8 | https://www.hdfcfund.com/services/faqs/subscription-related-faqs | Official FAQ |
| 9 | https://www.hdfcfund.com/statutory-disclosure | Statutory Disclosure |
| 10 | https://www.hdfcfund.com/statutory-disclosure/offer-document-disclosures | Offer Documents |
| 11 | https://www.hdfcfund.com/investor-services/form-disclosures/addenda-notices | Addenda & Notices |
| 12 | https://investor.sebi.gov.in/regular_and_direct_mutual_funds.html | SEBI Investor Education |
| 13 | https://investor.sebi.gov.in/securities-mf-investments.html | SEBI Investor Education |
| 14 | https://www.sebi.gov.in/sebi_data/commondocs/siep_h.html | SEBI Mutual Fund Education |
| 15 | https://www.hdfcfund.com/statutory-disclosure | HDFC Statutory Information |

A machine-readable version of the source list is also available in
`sources.csv`.

---

# 🧪 Sample Q&A

## 1. Minimum SIP

**Question:**  
What is the minimum SIP for HDFC Flexi Cap Fund?

**Answer:**  
The minimum SIP amount is ₹100.

**Source:**  
https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct

---

## 2. ELSS Lock-in

**Question:**  
What is the lock-in period of HDFC ELSS Tax Saver Fund?

**Answer:**  
The scheme has a statutory lock-in period of 3 years.

**Source:**  
https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct

---

## 3. Large Cap Benchmark

**Question:**  
What is the benchmark of HDFC Large Cap Fund?

**Answer:**  
The benchmark is NIFTY 100 Total Return Index.

**Source:**  
https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct

---

## 4. Flexi Cap Riskometer

**Question:**  
What is the riskometer of HDFC Flexi Cap Fund?

**Answer:**  
The scheme riskometer is Very High.

**Source:**  
https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct

---

## 5. ELSS Exit Load

**Question:**  
What is the exit load of HDFC ELSS Tax Saver Fund?

**Answer:**  
The exit load is NIL.

**Source:**  
https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct

---

## 6. Advice Guardrail

**Question:**  
Should I invest in HDFC Flexi Cap Fund?

**Answer:**  
I can provide verified facts about mutual fund schemes, but I cannot recommend
whether you should buy, sell, hold or switch a fund. You can ask about the
scheme's expense ratio, exit load, SIP amount, lock-in, riskometer or benchmark.

---

## 7. Performance Guardrail

**Question:**  
Which fund will give me the highest return?

**Answer:**  
I don't predict, calculate or compare investment returns. Please refer to
official AMC factsheets for published scheme information and historical
performance.

---

## 8. PII Guardrail

**Question:**  
My PAN is ABCDE1234F. Show my investments.

**Answer:**  
Please don't share personal information such as PAN, Aadhaar, account numbers,
OTPs, email addresses or phone numbers. This assistant only answers public
factual questions about supported mutual fund schemes.

---

# ⚠️ Disclaimer

**Facts-only. No investment advice.**

This prototype provides factual information retrieved from selected official
public sources. It does not recommend mutual funds or provide buy, sell, hold,
switch or portfolio-allocation advice.

The assistant does not predict or calculate future investment returns.

Users should not provide personally identifiable information such as PAN,
Aadhaar, account numbers, OTPs, email addresses or phone numbers.

Mutual fund information may change over time. Users should verify the latest
information from the linked official source before making financial decisions.

---

## 💻 Tech Stack

- Python
- Streamlit
- scikit-learn
- TF-IDF vectorization
- Cosine similarity retrieval
- GitHub
- Streamlit Community Cloud

---

## 🚀 Run Locally

Clone the repository:

    git clone https://github.com/aabha4747-art/facts-only-mf-assistant.git

Install dependencies:

    pip install -r requirements.txt

Run the application:

    streamlit run app.py

---

## ⚠️ Known Limitations

- The prototype supports only three selected HDFC Mutual Fund schemes.
- The knowledge corpus is intentionally small.
- Retrieval uses TF-IDF rather than semantic embedding models.
- Scheme information can change after the corpus is updated.
- The prototype does not access investor accounts or personal portfolios.
- It does not provide investment advice or future-return predictions.

---

## 📌 Assignment Focus

This prototype demonstrates:

**W1 — Thinking Like a Model:** deciding whether a query should be answered or
refused.

**W2 — Prompting / Guardrails:** concise facts-only behaviour, privacy handling
and safe refusals.

**W3 — Retrieval:** retrieving relevant information from a small corpus and
returning source-backed responses.
