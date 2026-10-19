import json
import sys
from pathlib import Path

# Allow importing project modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from vector_store import search
from reranker import rerank


QUESTIONS_FILE = Path(__file__).parent / "questions.json"

TOP_K_CANDIDATES = 30
K_VALUES = [1, 3, 5]


def load_questions():
    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def evaluate_question(question):

    candidates = search(
        question,
        top_k=TOP_K_CANDIDATES
    )

    results = rerank(
        question,
        candidates,
        top_k=5
    )

    return results


def main():

    questions = load_questions()

    print("=" * 80)
    print("PYTHON BOOK AI - RETRIEVAL BASELINE")
    print("=" * 80)

    print(f"\nQuestions: {len(questions)}")

    all_results = []

    for number, question in enumerate(
        questions,
        start=1
    ):

        print("\n" + "-" * 80)
        print(
            f"{number}/{len(questions)}: "
            f"{question}"
        )

        try:

            results = evaluate_question(question)

            pages = [
                result["page"]
                for result in results
            ]

            print("Retrieved pages:", pages)

            all_results.append({
                "question": question,
                "results": results,
                "status": "success"
            })

        except Exception as error:

            print("ERROR:", error)

            all_results.append({
                "question": question,
                "results": [],
                "status": "failed",
                "error": str(error)
            })

    output_file = (
        Path(__file__).parent /
        "retrieval_results.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_results,
            file,
            indent=2,
            ensure_ascii=False
        )

    successful = sum(
        result["status"] == "success"
        for result in all_results
    )

    print("\n" + "=" * 80)
    print("RETRIEVAL BASELINE COMPLETE")
    print("=" * 80)

    print(
        f"Successful: {successful}/"
        f"{len(questions)}"
    )

    print(
        f"\nResults saved to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":
    main()