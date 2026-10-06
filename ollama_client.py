import requests

from config import OLLAMA_BASE_URL, OLLAMA_MODEL


def generate(prompt: str, temperature=0.2):
    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    response = requests.post(
        url,
        json=payload,
        timeout=600
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()


def check_ollama():
    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=10
        )

        response.raise_for_status()

        models = [
            model["name"]
            for model in response.json().get("models", [])
        ]

        return True, models

    except requests.RequestException as error:
        return False, str(error)