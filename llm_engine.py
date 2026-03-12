
import os
os.environ["OMP_NUM_THREADS"] = "1"

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def analyze_with_llm(text):

    text = text[:1000]

    prompt = f"""
You are an expert in AI SEO and LLM optimization.

Analyze the following website content.

CONTENT:
{text}

Respond in this format:

Summary:
Problems for AI search engines:
Suggestions for improvement:
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return result