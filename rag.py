from config import TOP_K
from vector_store import search
from ollama_client import generate
from reranker import rerank


SYSTEM_RULES = """
You are Python Book AI, a careful Python programming tutor.

Your job is to answer questions using the supplied book context.

IMPORTANT RULES:

1. Use the supplied context as the primary source of truth.

2. Do not invent information that is not supported by the context.

3. If the context does not contain enough information, say:
   "The provided Python book does not contain enough information
   to answer this confidently."

4. Separate facts from examples.

5. When giving Python code examples:
   - Make sure the code is logically correct.
   - Do not change the meaning of examples from the source.
   - Do not invent output values.

6. Be especially careful with:
   - operator precedence
   - mutable vs immutable objects
   - references
   - equality vs identity
   - exceptions
   - class inheritance

7. Answer the exact question first.
   Do not focus on a related advanced topic unless it helps answer
   the question.

8. Keep explanations clear and beginner-friendly.

9. If the question asks for a definition, give the definition first,
   then explanation, then an example.

10. At the end provide Sources using the exact filename and page
    numbers supplied in the context.

11. Never write "BookName.pdf".

12. Never claim that a source says something unless that information
    appears in the supplied context.
"""


def answer_question(question: str, top_k=TOP_K):

    # Step 1: Search the vector database
    # Retrieve more candidates first
    candidates = search(
        question,
        top_k=30
    )

    # Step 2: Rerank the candidates
    results = rerank(
        question,
        candidates,
        top_k=top_k
    )

    # Step 3: Build context
    context_parts = []

    for i, item in enumerate(results, start=1):

        context_parts.append(
            f"""
[SOURCE {i}]

Book:
{item['source']}

Page:
{item['page']}

Content:
{item['text']}
"""
        )

    context = "\n\n".join(context_parts)

    # Step 4: Create prompt for Ollama
    prompt = f"""
{SYSTEM_RULES}

================ CONTEXT ================

{context}

================ QUESTION ================

{question}

================ INSTRUCTIONS ================

Answer the question using the supplied context.

Structure your answer as:

1. Direct answer
2. Explanation
3. Python example, if useful
4. Sources

Before giving any Python example, mentally verify:
- syntax
- operator precedence
- expected output
- consistency with the explanation

Do not invent source information.

Sources must use the exact filename and page number
from the supplied context.
"""

    # Step 5: Ask Ollama
    answer = generate(prompt)

    return {
        "answer": answer,
        "sources": results
    }