def build_llm_prompt(context_chunks, questions):
    context = "\n\n".join(chunk.get("text", "") for chunk in context_chunks)
    numbered_questions = "\n".join(
        f"{index + 1}. {question}" for index, question in enumerate(questions)
    )

    return f"""
IMPORTANT: You must paraphrase all answers. Do not extract or copy raw text from the excerpts.

You are a helpful and precise document analyst. Answer questions strictly from the provided document excerpts below.

Your job is to write short, rephrased, human-sounding one-line answers for each question. Do not copy or splice raw text from the excerpts.

If the context does not clearly contain an answer, reply with:
"I could not find this information in the document."

Instructions:
- Do not copy exact phrases or sentences from the excerpts.
- Do not include explanations, assumptions, or reasoning.
- Do paraphrase into clear, natural language.
- For direct questions, answer in one or two sentences.
- For broad questions asking what the document contains, provide a concise overview of the main subject and purpose visible in the excerpts.

Example Question:
1. What is the waiting period for pre-existing conditions?

Example Context:
Pre-existing diseases shall be covered after a waiting period of 48 months from the date of commencement of the policy.

Expected Answer Format:
{{
  "answers": [
    "Pre-existing conditions are covered after 48 months."
  ]
}}

Now answer the following questions based only on the context.

Questions:
{numbered_questions}

Document Excerpts:
{context}

Return valid JSON only, with no extra text or explanation.
""".strip()
