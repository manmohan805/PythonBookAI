from rag import answer_question


# ============================================================
# ASK QUESTION
# ============================================================

question = input(
    "Ask a question about the Python book: "
).strip()


# ============================================================
# VALIDATE QUESTION
# ============================================================

if not question:
    print("❌ Question cannot be empty.")
    exit()


# ============================================================
# SEARCH
# ============================================================

print("\n" + "=" * 80)
print("SEARCHING THE BOOK...")
print("=" * 80)


result = answer_question(question)


# ============================================================
# AI ANSWER
# ============================================================

print("\n" + "=" * 80)
print("AI ANSWER")
print("=" * 80)

print(result["answer"])
print("\n" + "=" * 80)
print("CODE VALIDATION")
print("=" * 80)

validation = result.get("code_validation", {})

print("Has code:")
print(validation.get("has_code"))

print("\nValid:")
print(validation.get("valid"))

print("\nErrors:")
for error in validation.get("errors", []):
    print("-", error)

print("\nWarnings:")
for warning in validation.get("warnings", []):
    print("-", warning)

# ============================================================
# RETRIEVED SOURCES
# ============================================================

print("\n" + "=" * 80)
print("RETRIEVED SOURCES")
print("=" * 80)


for i, source in enumerate(result["sources"], start=1):

    print("\n" + "-" * 80)

    print(f"Result #{i}")

    # --------------------------------------------------------
    # Source information
    # --------------------------------------------------------

    print(f"Book: {source['source']}")

    print(f"Page: {source['page']}")

    # --------------------------------------------------------
    # Search scores
    # --------------------------------------------------------

    print(
        f"Hybrid score: "
        f"{source.get('score', 0):.4f}"
    )

    print(
        f"Semantic score: "
        f"{source.get('semantic_score', 0):.4f}"
    )

    print(
        f"Keyword score: "
        f"{source.get('keyword_score', 0):.4f}"
    )

    print(
        f"Reranker score: "
        f"{source.get('reranker_score', 0):.4f}"
    )

    # --------------------------------------------------------
    # Content preview
    # --------------------------------------------------------

    print("\nContent preview:")

    content = source.get("text", "")

    if len(content) > 500:
        print(content[:500] + "...")
    else:
        print(content)


# ============================================================
# END
# ============================================================

print("\n" + "=" * 80)
print("SEARCH COMPLETE")
print("=" * 80)