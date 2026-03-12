import streamlit as st

from scraper import extract_website_data
from analyzer import analyze_content
from rag_engine import split_text, create_vector_db, retrieve_chunks
from llm_engine import analyze_with_llm


st.set_page_config(page_title="LLM SEO Analyzer", layout="wide")

st.title("🤖 LLM SEO Optimization Analyzer")

st.write(
"""
Analyze how well a website is optimized for **AI-powered search engines and LLMs**.
"""
)

url = st.text_input("Enter Website URL")

if st.button("Analyze Website"):

    if url == "":
        st.warning("Please enter a valid URL")
        st.stop()

    # -------------------
    # Step 1: Scrape Website
    # -------------------
    with st.spinner("Scraping website..."):

        data = extract_website_data(url)

        if "error" in data:
            st.error(data["error"])
            st.stop()

    st.success("Website scraped successfully!")

    # -------------------
    # Step 2: Content Analysis
    # -------------------
    st.subheader("📊 LLM SEO Scores")

    scores = analyze_content(data)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="LLM Optimization Score",
            value=scores["llm_optimization_score"]
        )

    with col2:
        st.metric(
            label="AI Search Visibility",
            value=scores["ai_visibility_score"]
        )

    with col3:
        st.metric(
            label="Citation Probability",
            value=str(scores["citation_probability"]) + "%"
        )

    # -------------------
    # Step 3: RAG Retrieval
    # -------------------
    with st.spinner("Running RAG retrieval..."):

        chunks = split_text(data["text"])

        if len(chunks) == 0:
          st.error("No usable content found on this page.")
          st.stop()

        index, embeddings = create_vector_db(chunks)

        query = "LLM SEO optimization issues"

        relevant_chunks = retrieve_chunks(query, chunks, index)

    st.subheader("🔎 Retrieved Website Content")

    for chunk in relevant_chunks:
        st.write(chunk[:300] + "...")

    # -------------------
    # Step 4: LLM Analysis
    # -------------------
    with st.spinner("Generating AI SEO report..."):

        combined_text = " ".join(relevant_chunks)

        report = analyze_with_llm(combined_text)

    st.subheader("🧠 AI SEO Report")

    st.write(report)

st.write("---")
st.write("Built using Streamlit + RAG + Open Source LLM")