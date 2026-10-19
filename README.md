@'
# PythonBookAI 📚

PythonBookAI is a Retrieval-Augmented Generation (RAG) application that helps users ask questions about Python books and receive answers based on the book content.

## Features

- Extract text from PDF books.
- Split extracted text into manageable chunks.
- Generate embeddings for semantic search.
- Retrieve relevant information using hybrid search.
- Rerank retrieved results.
- Generate answers using a local LLM through Ollama.
- Display source references to help users verify answers.

## Technology Stack

- Python
- Flask
- PyMuPDF
- NumPy
- Sentence Transformers
- PyTorch
- Ollama
- HTML, CSS, and JavaScript

## Prerequisites

Install Python and Ollama before running the application.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/manmohan805/PythonBookAI.git
cd PythonBookAI