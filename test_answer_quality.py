from rag import answer_question


QUESTIONS = [
    "What is a tuple?",
    "What is the difference between a list and a tuple?",
    "What are operators?",
    "What is the difference between == and is?",
]


for question in QUESTIONS:

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)

    print(question)

    result = answer_question(question)

    print("\nANSWER")
    print("-" * 80)

    print(result["answer"])