from evaluation_questions import QUESTIONS
from rag import answer_question


# ============================================================
# EVALUATION SETTINGS
# ============================================================

TOP_K = 5


# ============================================================
# RUN EVALUATION
# ============================================================

def run_evaluation():

    print("=" * 80)
    print("PYTHON BOOK AI - RAG EVALUATION")
    print("=" * 80)

    print(f"\nTotal questions: {len(QUESTIONS)}")
    print(f"Top-K retrieval: {TOP_K}")

    results = []

    for number, question in enumerate(QUESTIONS, start=1):

        print("\n" + "=" * 80)
        print(f"QUESTION {number}/{len(QUESTIONS)}")
        print("=" * 80)

        print(f"\nQuestion: {question}")

        try:

            result = answer_question(
                question,
                top_k=TOP_K
            )

            answer = result["answer"]
            sources = result["sources"]

            print("\nANSWER")
            print("-" * 80)
            print(answer)

            print("\nRETRIEVED SOURCES")
            print("-" * 80)

            for rank, source in enumerate(sources, start=1):

                print(
                    f"{rank}. "
                    f"{source['source']} "
                    f"(Page {source['page']}) "
                    f"| "
                    f"Reranker: "
                    f"{source.get('reranker_score', 0):.4f}"
                )

            results.append({
                "question": question,
                "answer": answer,
                "sources": sources
            })

        except Exception as error:

            print("\n❌ ERROR")
            print(error)

            results.append({
                "question": question,
                "answer": None,
                "sources": [],
                "error": str(error)
            })

    return results


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    results = run_evaluation()

    print("\n\n" + "=" * 80)
    print("EVALUATION FINISHED")
    print("=" * 80)

    successful = sum(
        1
        for result in results
        if result.get("answer")
    )

    failed = len(results) - successful

    print(f"\nSuccessful: {successful}")
    print(f"Failed:     {failed}")