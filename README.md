# Research Paper Summarizer

A web application that allows users to search for research papers based on semantic similarity, retrieve papers from multiple sources, and generate concise summaries using AI.

## Features

- Search for research papers using keywords or natural language queries
- Retrieve papers from multiple sources (Semantic Scholar, arXiv, Google Scholar)
- Rank papers based on semantic similarity to the query
- Generate concise 1-2 paragraph summaries using Google's Gemini API
- Display results with relevance scores and links to original papers

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

You can get a free Gemini API key from [Google AI Studio](https://ai.google.dev/).

## Usage

1. Run the application:

```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter your search query and select the number of results you want to see

4. Click "Search" to find and summarize relevant research papers

## Technologies Used

- Backend: Python, Flask
- Semantic Search: Sentence Transformers (all-MiniLM-L6-v2)
- Paper APIs: Semantic Scholar API, arXiv API, Google Scholar (via scholarly)
- Summarization: Google's Gemini API
- Frontend: HTML, CSS, JavaScript, Bootstrap

## Notes

- Google Scholar searches may occasionally fail due to rate limiting/blocking
- For best results, use specific queries related to your research topic
- The summarization quality depends on the Gemini API model and the quality of the paper abstracts