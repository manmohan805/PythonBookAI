from rag import answer_question


QUESTIONS = [
    "What is a list?",
    "Give an example of a Python list.",
    "What is a tuple?",
    "What is the difference between a list and a tuple?",
    "What is a function?",
    "What is inheritance?",
    "What are operators?",
    "What is exception handling?",
    "What is the difference between == and is?",
    "What is a dictionary?",
]


def main():

    print("=" * 80)
    print("PYTHON BOOK AI - ANSWER QUALITY EVALUATION")
    print("=" * 80)

    for number, question in enumerate(QUESTIONS, start=1):

        print("\n" + "=" * 80)
        print(f"QUESTION {number}/{len(QUESTIONS)}")
        print("=" * 80)

        print(f"\nQuestion: {question}")

        try:

            result = answer_question(question)

            print("\nANSWER")
            print("-" * 80)
            print(result["answer"])

            print("\nSOURCES USED BY RAG")
            print("-" * 80)

            for rank, source in enumerate(
                result["sources"],
                start=1
            ):

                print(
                    f"{rank}. "
                    f"{source['source']} "
                    f"| Page {source['page']} "
                    f"| Reranker: "
                    f"{source.get('reranker_score', 0):.4f}"
                )

        except Exception as error:

            print("\n❌ ERROR")
            print(error)

    print("\n" + "=" * 80)
    print("ANSWER EVALUATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()