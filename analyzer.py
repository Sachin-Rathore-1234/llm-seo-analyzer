import textstat


def analyze_content(data):

    text = data["text"]
    headings = data["headings"]
    paragraphs = data["paragraphs"]

    # 1️⃣ Readability score
    readability = textstat.flesch_reading_ease(text)

    # normalize readability
    readability_score = max(min(readability / 10, 10), 0)

    # 2️⃣ Structure score
    heading_count = len(headings)

    if heading_count >= 10:
        structure_score = 10
    elif heading_count >= 5:
        structure_score = 7
    elif heading_count >= 2:
        structure_score = 5
    else:
        structure_score = 2

    # 3️⃣ Content score
    word_count = len(text.split())

    if word_count > 2000:
        content_score = 10
    elif word_count > 1000:
        content_score = 8
    elif word_count > 500:
        content_score = 6
    else:
        content_score = 3

    # 4️⃣ FAQ bonus
    faq_bonus = 1 if data["faq_detected"] else 0

    # 5️⃣ LLM optimization score
    llm_score = (
        readability_score * 0.3 +
        structure_score * 0.3 +
        content_score * 0.3 +
        faq_bonus * 0.1
    )

    # 6️⃣ AI visibility score
    visibility_score = min(
        int((heading_count * 5) + (content_score * 5)), 100
    )

    # 7️⃣ Citation probability
    citation_probability = min(
        int(llm_score * 10), 100
    )

    return {
        "readability_score": round(readability_score,2),
        "structure_score": structure_score,
        "content_score": content_score,
        "llm_optimization_score": round(llm_score,2),
        "ai_visibility_score": visibility_score,
        "citation_probability": citation_probability
    }